"""
Command-line interface for Flarewell.
"""

import os
import sys
import json
import click

from flarewell.converter import FlareConverter
from flarewell.flare_analyzer import analyze_flare_project, list_project_targets, list_project_tocs, get_folder_statistics


@click.group()
def cli():
    """Flarewell: Convert MadCap Flare projects to Docusaurus-compatible Markdown."""
    pass


@cli.command('convert')
@click.option(
    "--input-dir",
    "-i",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory containing Flare project or HTML output.",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Directory to output Docusaurus-compatible Markdown files.",
)
@click.option(
    "--use-llm",
    is_flag=True,
    default=False,
    help="Use LLM to suggest an improved folder/file structure.",
)
@click.option(
    "--llm-api-key",
    envvar="FLAREWELL_LLM_API_KEY",
    help="API key for the LLM service (can also be set via FLAREWELL_LLM_API_KEY environment variable).",
)
@click.option(
    "--llm-provider",
    default="openai",
    type=click.Choice(["openai", "anthropic"]),
    help="LLM provider to use when --use-llm is specified.",
)
@click.option(
    "--input-type",
    type=click.Choice(["project", "html"]),
    default="project",
    help="Type of input. 'project' for Flare project files, 'html' for Flare HTML output.",
)
@click.option(
    "--preserve-structure",
    is_flag=True,
    default=True,
    help="Preserve the original folder/file structure.",
)
@click.option(
    "--target",
    help="Specify a specific target to convert (use the analyze command to list available targets).",
)
@click.option(
    "--exclude-dir",
    multiple=True,
    help="Directory patterns to exclude from conversion (can be used multiple times).",
)
def convert(
    input_dir,
    output_dir,
    use_llm,
    llm_api_key,
    llm_provider,
    input_type,
    preserve_structure,
    target,
    exclude_dir,
):
    """
    Convert MadCap Flare documentation to Docusaurus-compatible Markdown.
    """
    if use_llm and not llm_api_key:
        click.echo(
            "Error: --use-llm requires an API key. Provide it with --llm-api-key or set the FLAREWELL_LLM_API_KEY environment variable.",
            err=True,
        )
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    click.echo(f"Converting {input_type} from {input_dir} to {output_dir}")
    
    converter = FlareConverter(
        input_dir=input_dir,
        output_dir=output_dir,
        input_type=input_type,
        preserve_structure=preserve_structure,
        use_llm=use_llm,
        llm_api_key=llm_api_key,
        llm_provider=llm_provider,
        target=target,
        exclude_dirs=list(exclude_dir),
    )
    
    try:
        result = converter.convert()
        click.echo(f"✅ Conversion completed. {result['converted']} files converted.")
    except Exception as e:
        click.echo(f"❌ Error during conversion: {str(e)}", err=True)
        sys.exit(1)


@cli.command('analyze')
@click.option(
    "--input-dir",
    "-i",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory containing Flare project.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(file_okay=True, dir_okay=False),
    help="Output file for analysis results (JSON format). If not specified, results are printed to console.",
)
@click.option(
    "--list-targets",
    is_flag=True,
    help="List all targets in the project.",
)
@click.option(
    "--list-tocs",
    is_flag=True,
    help="List all TOCs in the project.",
)
@click.option(
    "--folder-stats",
    is_flag=True,
    help="Show statistics about folders in the project.",
)
def analyze(
    input_dir,
    output_file,
    list_targets,
    list_tocs,
    folder_stats,
):
    """
    Analyze a Flare project to determine which content is actively used in production.
    
    This command helps identify which parts of a Flare project are actively used in production
    and which parts might be test, draft, or deprecated content. This can help you decide which
    content to include in your Docusaurus conversion.
    """
    try:
        if list_targets:
            # Just list targets
            targets = list_project_targets(input_dir)
            click.echo("\nTargets in project:")
            click.echo("-----------------")
            for target in targets:
                test_marker = " [TEST]" if target["is_test"] else ""
                click.echo(f"{target['name']}{test_marker} - TOCs: {target['toc_count']}")
                if target["description"]:
                    click.echo(f"  Description: {target['description']}")
                click.echo(f"  Path: {target['path']}")
                click.echo("")
            return
        
        if list_tocs:
            # Just list TOCs
            tocs = list_project_tocs(input_dir)
            click.echo("\nTOCs in project:")
            click.echo("--------------")
            for toc in tocs:
                click.echo(f"{toc['name']} - Topics: {toc['topic_count']}")
                click.echo(f"  Path: {toc['path']}")
                click.echo("")
            return
        
        if folder_stats:
            # Show folder statistics
            stats = get_folder_statistics(input_dir)
            click.echo("\nFolder statistics:")
            click.echo("-----------------")
            for folder, count in stats.items():
                click.echo(f"{folder}: {count} topics")
            return
        
        # Full analysis
        click.echo(f"Analyzing Flare project in {input_dir}...")
        analysis = analyze_flare_project(input_dir)
        
        if output_file:
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
            click.echo(f"Analysis results written to {output_file}")
        else:
            # Print summary to console
            click.echo("\nAnalysis Summary:")
            click.echo("----------------")
            click.echo(f"Project: {analysis['project_name']}")
            click.echo(f"Targets found: {len(analysis['targets'])}")
            click.echo(f"TOCs found: {len(analysis['tocs'])}")
            click.echo(f"Likely production targets: {', '.join(analysis['active_targets'])}")
            click.echo(f"Used topics: {len(analysis['used_topics'])}")
            click.echo(f"Unused topics: {len(analysis['unused_topics'])}")
            
            # Print potential test content
            potential_test = analysis['potential_test_content']
            click.echo("\nPotential test/draft directories:")
            for cat, dirs in potential_test.items():
                if dirs:
                    click.echo(f"  {cat.replace('_', ' ').title()}: {len(dirs)}")
                    for d in dirs[:5]:  # Show at most 5 directories per category
                        click.echo(f"    - {d}")
                    if len(dirs) > 5:
                        click.echo(f"    - ... and {len(dirs) - 5} more")
            
            # Print recommendations
            recommendations = analysis['recommendations']
            click.echo("\nRecommendations for conversion:")
            click.echo(f"  Recommended target: {recommendations['recommended_targets'][0] if recommendations['recommended_targets'] else 'None'}")
            click.echo(f"  Directories to exclude: {len(recommendations['exclude_directories'])}")
            
            # Print example command
            if recommendations['recommended_targets']:
                target = recommendations['recommended_targets'][0]
                exclude_dirs = ' '.join([f'--exclude-dir "{d}"' for d in recommendations['exclude_directories'][:3]])
                if len(recommendations['exclude_directories']) > 3:
                    exclude_dirs += f" ... and {len(recommendations['exclude_directories']) - 3} more"
                
                click.echo("\nExample conversion command:")
                click.echo(f'  flarewell convert --input-dir "{input_dir}" --output-dir "docusaurus-output" --target "{target}" {exclude_dirs}')
    
    except Exception as e:
        click.echo(f"❌ Error during analysis: {str(e)}", err=True)
        sys.exit(1)


def main():
    """
    Main entry point.
    """
    # For backward compatibility, if no command is specified, default to 'convert'
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and sys.argv[1] not in cli.commands:
        # Insert the default command
        sys.argv.insert(1, 'convert')
    
    cli()


if __name__ == "__main__":
    main() 