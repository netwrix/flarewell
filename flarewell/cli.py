"""
Command-line interface for Flarewell.
"""

import os
import sys
import json
import time
import re
import click
from pathlib import Path
from typing import Optional, List

from flarewell.converter import FlareConverter
from flarewell.flare_analyzer import analyze_flare_project, list_project_targets, list_project_tocs, get_folder_statistics
from flarewell.link_mapper import LinkMapper
from flarewell.image_relocator import ImageRelocator


@click.group()
def cli():
    """Flarewell: Convert MadCap Flare projects to Docusaurus-compatible Markdown."""
    pass


@cli.command()
@click.option(
    "--input-dir", "-i",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory containing Flare project or HTML output."
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory to output Docusaurus-compatible Markdown files."
)
@click.option(
    "--use-llm",
    is_flag=True,
    help="Use LLM to suggest an improved folder/file structure."
)
@click.option(
    "--llm-api-key",
    envvar="FLAREWELL_LLM_API_KEY",
    help="API key for the LLM service (can also be set via FLAREWELL_LLM_API_KEY environment variable)."
)
@click.option(
    "--llm-provider",
    type=click.Choice(["openai", "anthropic"]),
    default="openai",
    help="LLM provider to use when --use-llm is specified."
)
@click.option(
    "--input-type",
    type=click.Choice(["project", "html"]),
    default="project",
    help="Type of input. 'project' for Flare project files, 'html' for Flare HTML output."
)
@click.option(
    "--preserve-structure",
    is_flag=True,
    default=True,
    help="Preserve the original folder/file structure."
)
@click.option(
    "--target",
    help="Specify a specific target to convert (use the analyze command to list available targets)."
)
@click.option(
    "--exclude-dir",
    multiple=True,
    help="Directory patterns to exclude from conversion (can be used multiple times)."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for detailed logging."
)
@click.option(
    "--fix-links",
    is_flag=True,
    help="Fix links in converted Markdown files after conversion."
)
@click.option(
    "--relocate-images",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Relocate images to the specified directory and update references."
)
def convert(
    input_dir: str,
    output_dir: str,
    use_llm: bool,
    llm_api_key: Optional[str],
    llm_provider: str,
    input_type: str,
    preserve_structure: bool,
    target: Optional[str],
    exclude_dir: List[str],
    debug: bool,
    fix_links: bool,
    relocate_images: Optional[str],
):
    """Convert MadCap Flare documentation to Docusaurus-compatible Markdown."""
    click.echo(f"Converting {input_type} from {input_dir} to {output_dir}")
    
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create converter
    start_time = time.time()
    converter = FlareConverter(
        input_dir=input_dir,
        output_dir=output_dir,
        input_type=input_type,
        preserve_structure=preserve_structure,
        use_llm=use_llm,
        llm_api_key=llm_api_key,
        llm_provider=llm_provider,
        target=target,
        exclude_dirs=exclude_dir,
        debug=debug,
    )
    
    # Run conversion
    stats = converter.convert()
    
    # Print completion message
    conversion_time = time.time() - start_time
    click.echo(f"✅ Conversion completed in {conversion_time:.2f} seconds. {stats['converted']} files converted.")
    
    if stats['skipped'] > 0:
        click.echo(f"⚠️ {stats['skipped']} files skipped.")
    
    if stats['errors'] > 0:
        click.echo(f"❌ {stats['errors']} errors encountered.")
    
    # Fix links in output directory if requested
    if fix_links:
        click.echo("\nFixing links in converted Markdown files...")
        fix_links_start = time.time()
        
        # Create directory path
        md_dir = Path(output_dir)
        
        # Find all Markdown files
        md_files = list(md_dir.glob("**/*.md"))
        total_files = len(md_files)
        click.echo(f"Found {total_files} Markdown files")
        
        # Create link mapper with debug mode if requested
        link_mapper = LinkMapper(preserve_structure=preserve_structure, debug=debug)
        
        # Register all files in the mapper
        click.echo("Building link registry...")
        
        registry = []
        for file_path in md_files:
            # Get path relative to the base directory
            rel_path = file_path.relative_to(md_dir)
            # Convert to .htm for registration
            htm_path = rel_path.with_suffix(".htm")
            
            registry.append({
                "rel_path": str(htm_path),
                "title": file_path.stem
            })
        
        # Register files with link mapper
        link_mapper.register_files(registry)
        click.echo(f"Registered {len(registry)} files in link map")
        
        # Process files
        files_processed = 0
        files_changed = 0
        errors = 0
        
        for i, file_path in enumerate(md_files):
            if debug or (i % 100 == 0 and i > 0):
                click.echo(f"Processing file {i+1}/{total_files} ({(i+1)/total_files*100:.1f}%)")
            
            try:
                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Get path relative to base dir for context
                rel_path = str(file_path.relative_to(md_dir))
                
                # Check for links requiring transformation
                if re.search(r'\]\([^)]*\.(htm|html)', content):
                    # Transform links
                    transformed = link_mapper.transform_links(content, rel_path)
                    
                    # Only write back if changes were made
                    if transformed != content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(transformed)
                        files_changed += 1
                
                files_processed += 1
                
            except Exception as e:
                click.echo(f"Error processing {file_path}: {str(e)}")
                errors += 1
        
        # Print completion message
        fix_links_time = time.time() - fix_links_start
        click.echo(f"✅ Link fixing completed in {fix_links_time:.2f} seconds.")
        click.echo(f"Files processed: {files_processed}")
        click.echo(f"Files modified: {files_changed}")
        
        if errors > 0:
            click.echo(f"❌ {errors} errors encountered during link fixing.")
    
    # Relocate images if requested
    if relocate_images:
        click.echo("\nRelocating images to specified directory...")
        relocate_start = time.time()
        
        # Create image relocator
        image_relocator = ImageRelocator(
            source_dir=output_dir,
            target_dir=relocate_images,
            preserve_structure=preserve_structure,
            debug=debug
        )
        
        # Run image relocation
        relocation_stats = image_relocator.relocate()
        
        # Print completion message
        relocate_time = time.time() - relocate_start
        click.echo(f"✅ Image relocation completed in {relocate_time:.2f} seconds.")
        click.echo(f"Images relocated: {relocation_stats['images_relocated']}")
        click.echo(f"Files updated: {relocation_stats['files_updated']}")
        
        if relocation_stats['errors'] > 0:
            click.echo(f"❌ {relocation_stats['errors']} errors encountered during image relocation.")
    
    # Print total time
    total_time = time.time() - start_time
    click.echo(f"\n✅ Total process completed in {total_time:.2f} seconds.")


@cli.command()
@click.option(
    "--dir", "-d",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory containing already-converted Markdown files."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for detailed logging."
)
def fix_links(dir: str, debug: bool):
    """Fix links in already-converted Markdown files to point to .md files instead of .htm/.html files."""
    click.echo(f"Fixing links in Markdown files in: {dir}")
    start_time = time.time()
    
    # Create directory path
    md_dir = Path(dir)
    
    # Find all Markdown files
    md_files = list(md_dir.glob("**/*.md"))
    total_files = len(md_files)
    click.echo(f"Found {total_files} Markdown files")
    
    # Create link mapper with debug mode if requested
    link_mapper = LinkMapper(preserve_structure=True, debug=debug)
    
    # Register all files in the mapper
    click.echo("Building link registry...")
    
    registry = []
    for file_path in md_files:
        # Get path relative to the base directory
        rel_path = file_path.relative_to(md_dir)
        # Convert to .htm for registration
        htm_path = rel_path.with_suffix(".htm")
        
        registry.append({
            "rel_path": str(htm_path),
            "title": file_path.stem
        })
    
    # Register files with link mapper
    link_mapper.register_files(registry)
    click.echo(f"Registered {len(registry)} files in link map")
    
    # Process files
    files_processed = 0
    files_changed = 0
    errors = 0
    
    for i, file_path in enumerate(md_files):
        if debug or (i % 100 == 0):
            click.echo(f"Processing file {i+1}/{total_files} ({(i+1)/total_files*100:.1f}%)")
        
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Get path relative to base dir for context
            rel_path = str(file_path.relative_to(md_dir))
            
            # Check for links requiring transformation
            if re.search(r'\]\([^)]*\.(htm|html)', content):
                # Transform links
                transformed = link_mapper.transform_links(content, rel_path)
                
                # Only write back if changes were made
                if transformed != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(transformed)
                    files_changed += 1
            
            files_processed += 1
            
        except Exception as e:
            click.echo(f"Error processing {file_path}: {str(e)}")
            errors += 1
    
    # Print completion message
    elapsed_time = time.time() - start_time
    click.echo(f"✅ Link fixing completed in {elapsed_time:.2f} seconds.")
    click.echo(f"Files processed: {files_processed}")
    click.echo(f"Files modified: {files_changed}")
    
    if errors > 0:
        click.echo(f"❌ {errors} errors encountered.")


@cli.command()
@click.option(
    "--dir", "-d",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory containing already-converted Markdown files."
)
@click.option(
    "--target-dir", "-t",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Target directory for relocated images."
)
@click.option(
    "--preserve-structure",
    is_flag=True,
    default=True,
    help="Preserve subdirectory structure within target directory."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for detailed logging."
)
def relocate_images(dir: str, target_dir: str, preserve_structure: bool, debug: bool):
    """Relocate images to a specified directory and update all references in Markdown files."""
    click.echo(f"Relocating images from {dir} to {target_dir}")
    start_time = time.time()
    
    # Create image relocator
    image_relocator = ImageRelocator(
        source_dir=dir,
        target_dir=target_dir,
        preserve_structure=preserve_structure,
        debug=debug
    )
    
    # Run image relocation
    stats = image_relocator.relocate()
    
    # Print completion message
    elapsed_time = time.time() - start_time
    click.echo(f"✅ Image relocation completed in {elapsed_time:.2f} seconds.")
    click.echo(f"Images relocated: {stats['images_relocated']}")
    click.echo(f"Files updated: {stats['files_updated']}")
    
    if stats['errors'] > 0:
        click.echo(f"❌ {stats['errors']} errors encountered.")


@cli.command()
@click.option(
    "--input-dir", "-i",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory containing Flare project."
)
@click.option(
    "--output-file", "-o",
    type=click.Path(file_okay=True, dir_okay=False),
    help="Output file for analysis results (JSON format)."
)
@click.option(
    "--list-targets",
    is_flag=True,
    help="List all targets in the project."
)
@click.option(
    "--list-tocs",
    is_flag=True,
    help="List all TOCs in the project."
)
@click.option(
    "--folder-stats",
    is_flag=True,
    help="Show statistics about folders in the project."
)
def analyze(
    input_dir: str,
    output_file: Optional[str],
    list_targets: bool,
    list_tocs: bool,
    folder_stats: bool,
):
    """Analyze a Flare project to determine which content is actively used."""
    # Analyze project
    if list_targets:
        targets = list_project_targets(input_dir)
        click.echo("\nTargets:")
        for target in targets:
            click.echo(f"  - {target.get('name')}: {target.get('type', 'Unknown')}")
        return
    
    if list_tocs:
        tocs = list_project_tocs(input_dir)
        click.echo("\nTOCs:")
        for toc in tocs:
            click.echo(f"  - {toc.get('name')}: {toc.get('title', '')}")
        return
    
    if folder_stats:
        folders = get_folder_statistics(input_dir)
        click.echo("\nFolder Statistics:")
        for folder, stats in folders.items():
            click.echo(f"  - {folder}: {stats.get('files', 0)} files, {stats.get('referenced', 0)} referenced")
        return
    
    # If no specific option was chosen, show a general summary
    result = analyze_flare_project(input_dir)
    
    click.echo("\nProject Summary:")
    click.echo(f"  - {len(result.get('targets', []))} targets")
    click.echo(f"  - {len(result.get('tocs', []))} TOCs")
    click.echo(f"  - {result.get('total_files', 0)} total files")
    click.echo(f"  - {result.get('referenced_files', 0)} referenced files")
    
    # Show top folders
    click.echo("\nTop 5 Folders by Files:")
    folders = result.get('folder_stats', {})
    sorted_folders = sorted(
        folders.items(), 
        key=lambda x: x[1].get('files', 0) if isinstance(x[1], dict) else 0, 
        reverse=True
    )
    for folder, stats in sorted_folders[:5]:
        if isinstance(stats, dict):
            click.echo(f"  - {folder}: {stats.get('files', 0)} files, {stats.get('referenced', 0)} referenced")
    
    # Write to output file if specified
    if output_file:
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        click.echo(f"\nAnalysis results written to {output_file}")


def main():
    """
    Main entry point for the CLI.
    """
    # For backward compatibility, if no command is specified, default to 'convert'
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and sys.argv[1] not in cli.commands:
        # Insert the default command
        sys.argv.insert(1, 'convert')
    
    cli()


if __name__ == "__main__":
    main() 