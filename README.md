# Flarewell - MadCap Flare to Docusaurus Converter

A Python tool to convert MadCap Flare HTML exports to Docusaurus-compatible Markdown.

## New: Improved Link Mapping

This version includes a robust link mapping system that:

1. **Automatically transforms links** from .htm/.html to their Markdown equivalents
2. **Preserves relative paths** correctly between files
3. **Handles case sensitivity** and path variations
4. **Preserves link titles** and attributes
5. **Supports absolute paths** (/path/to/file.htm) and relative paths (../path/to/file.htm)

The link mapper is integrated into the main conversion workflow and uses a two-step process:
1. First, all files are registered in a master link map
2. Then, during conversion, all links in each file are transformed using this map

## New: Image Relocation

Images are now automatically moved to a `static` directory located next to the
output docs. All references inside Markdown files are updated, preserving
relative paths and directory structure. No additional flags are required.
Missing image references are removed during a post-conversion scan of the generated Markdown.

## Features

- Convert Flare HTML output to Markdown
- Preserve the original folder structure and automatically generate `sidebars.js`
- Convert Flare-specific UI elements to Docusaurus equivalents (admonitions, expandable sections, etc.)
- Generate Docusaurus sidebar configuration
- Automatically relocate images to a `static` directory next to your docs
- Remove references to images that are missing after conversion

## Installation

```bash
pip install flarewell
```

Or for development:

```bash
git clone https://github.com/yourusername/flarewell.git
cd flarewell
pip install -e .
```

## Usage

Flarewell provides a single command:
- `convert`: Transform Flare content to Docusaurus Markdown. Links are automatically fixed during conversion.

### Convert Command

Convert HTML output from Flare:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs
```

Convert HTML to generic Markdown without Docusaurus front matter:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir ./docs --markdown-style markdown
```

Converted images will be moved to a `static` directory next to your output docs automatically.

#### Convert Options

- `--input-dir, -i`: Directory containing Flare HTML output
- `--output-dir, -o`: Directory to output Docusaurus-compatible Markdown files
- `--preserve-structure`: Preserve the original folder/file structure (default: `True`)
- `--exclude-dir`: Directory patterns to exclude from conversion (can be used multiple times)
- `--debug`: Enable debug mode for detailed logging
- `--no-sidebars`: Skip generating `sidebars.js`
- `--verbose-image-cleanup`: Print each removed image reference
- 
## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/flarewell.git
cd flarewell

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

## License

MIT 