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
from flarewell.link_mapper import LinkMapper
from flarewell.markdown_image_cleaner import MarkdownImageCleaner


@click.group()
def cli():
    """Flarewell: Convert MadCap Flare HTML output to Docusaurus-compatible Markdown."""
    pass


@cli.command()
@click.option(
    "--input-dir", "-i",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory containing Flare HTML output."
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help="Directory to output Docusaurus-compatible Markdown files."
)
@click.option(
    "--preserve-structure",
    is_flag=True,
    default=True,
    help="Preserve the original folder/file structure."
)
@click.option(
    "--no-sidebars",
    is_flag=True,
    help="Skip sidebar.js generation."
)
@click.option(
    "--exclude-dir",
    multiple=True,
    help="Directory patterns to exclude from conversion (can be used multiple times)."
)
@click.option(
    "--verbose-image-cleanup",
    is_flag=True,
    help="Print each removed image reference and deleted file."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode for detailed logging."
)
def convert(
    input_dir: str,
    output_dir: str,
    preserve_structure: bool,
    exclude_dir: List[str],
    verbose_image_cleanup: bool,
    debug: bool,
    no_sidebars: bool
):
    """Convert MadCap Flare HTML output to Docusaurus-compatible Markdown."""
    click.echo(f"Converting HTML from {input_dir} to {output_dir}")
    
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create converter
    start_time = time.time()
    converter = FlareConverter(
        input_dir=input_dir,
        output_dir=output_dir,
        preserve_structure=preserve_structure,
        generate_sidebars=not no_sidebars,
        exclude_dirs=exclude_dir,
        debug=debug
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
    
    # Fix links in output directory
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
    

    # Images are relocated during conversion; report destination directory
    static_dir = Path(output_dir).parent / "static"
    click.echo(f"\nImages copied to: {static_dir}")

    # Remove references to images that do not exist
    click.echo("\nCleaning up references to missing images...")
    cleanup_start = time.time()
    cleaner = MarkdownImageCleaner(output_dir, static_dir=str(static_dir), debug=verbose_image_cleanup)
    cleanup_stats = cleaner.clean()
    cleanup_time = time.time() - cleanup_start
    click.echo(f"✅ Image cleanup completed in {cleanup_time:.2f} seconds.")
    click.echo(f"References removed: {cleanup_stats['references_removed']}")
    
    # Print total time
    total_time = time.time() - start_time
    click.echo(f"\n✅ Total process completed in {total_time:.2f} seconds.")






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
