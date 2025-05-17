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

This version adds a powerful image relocation feature that:

1. **Moves images to a specified directory** while preserving subdirectory structure
2. **Updates all references** to those images in Markdown files
3. **Preserves relative paths** between Markdown files and images
4. **Handles both absolute and relative paths** in image references

The image relocator can be used:
- As part of the conversion process with the `--relocate-images` flag
- As a standalone command for already-converted content with `relocate-images`

> **Important Path Note:** When specifying the target directory for relocated images, use a *relative* path from your current directory. For example, use `./static/img` rather than an absolute path. This ensures proper path resolution when updating image references.

## Features

- Convert Flare HTML output to Markdown
- Maintain folder/file structure or suggest an improved structure using LLM
- Convert Flare-specific UI elements to Docusaurus equivalents (admonitions, expandable sections, etc.)
- Generate Docusaurus sidebar configuration
- Fix references in already-converted Markdown files
- Relocate images to a centralized directory and update all references

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

Flarewell offers three main commands:
- `convert`: Transform Flare HTML output to Docusaurus Markdown
- `fix-links`: Update internal links in already-converted Markdown files
- `relocate-images`: Move images to a specified directory and update references

### Convert Command

Convert HTML output from Flare:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs
```

Convert HTML to generic Markdown without Docusaurus front matter:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir ./docs --markdown-style markdown
```

Convert HTML to generic Markdown without Docusaurus front matter:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir ./docs --input-type html --markdown-style markdown
```

Convert and automatically fix links in one step:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --fix-links
```

Convert and relocate images to a specific directory:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --relocate-images ./static/img
```

#### Using LLM for Structure Suggestions

To use an LLM to suggest an improved folder/file structure:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --use-llm --llm-api-key YOUR_API_KEY
```

You can also set your API key via environment variable:

```bash
export FLAREWELL_LLM_API_KEY=YOUR_API_KEY
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --use-llm
```

#### Convert Options

- `--input-dir, -i`: Directory containing Flare HTML output
- `--output-dir, -o`: Directory to output Docusaurus-compatible Markdown files
- `--preserve-structure`: Preserve the original folder/file structure (default: `True`)
- `--use-llm`: Use LLM to suggest an improved folder/file structure
- `--llm-api-key`: API key for the LLM service (or set via `FLAREWELL_LLM_API_KEY` environment variable)
- `--llm-provider`: LLM provider to use (`openai` or `anthropic`), default is `openai`
- `--exclude-dir`: Directory patterns to exclude from conversion (can be used multiple times)
- `--debug`: Enable debug mode for detailed logging
- `--fix-links`: Fix links in converted Markdown files after conversion
- `--relocate-images`: Relocate images to the specified directory and update references (use relative paths like `./static/img`)

### Fix Links Command

The fix-links command updates all internal references in already-converted Markdown files to point to `.md` files instead of `.htm/.html` files. This is particularly useful when you've already converted your content but links still reference the original HTML files.

Fix links in a directory of Markdown files:

```bash
flarewell fix-links --dir /path/to/markdown/files
```

Enable debug mode for more detailed logging:

```bash
flarewell fix-links --dir /path/to/markdown/files --debug
```

#### Fix Links Options

- `--dir, -d`: Directory containing already-converted Markdown files
- `--debug`: Enable debug mode for detailed logging

### Relocate Images Command

The relocate-images command moves all images to a specified directory and updates all references in Markdown files. This is useful for centralizing images in a structure that works well with Docusaurus.

Relocate images from converted Markdown directory to a target directory:

```bash
flarewell relocate-images --dir /path/to/markdown/files --target-dir ./static/img
```

Flatten the directory structure (don't preserve subdirectories):

```bash
flarewell relocate-images --dir /path/to/markdown/files --target-dir ./static/img --no-preserve-structure
```

Enable debug mode for more detailed logging:

```bash
flarewell relocate-images --dir /path/to/markdown/files --target-dir ./static/img --debug
```

#### Relocate Images Options

- `--dir, -d`: Directory containing already-converted Markdown files
- `--target-dir, -t`: Target directory for relocated images (use relative paths like `./static/img`)
- `--preserve-structure`: Preserve subdirectory structure within target directory (default: `True`)
- `--debug`: Enable debug mode for detailed logging

#### Conversion Workflow

A typical workflow for converting Flare content might include:

1. Option 1: One-step conversion with link fixing and image relocation:
   ```bash
   flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --fix-links --relocate-images ./static/img
   ```

2. Option 2: Multi-step process:
   ```bash
   # First convert the files
   flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs
   
   # Then fix the links in a separate step
   flarewell fix-links --dir /path/to/docusaurus/docs

   # Finally relocate images to a centralized location
   flarewell relocate-images --dir /path/to/docusaurus/docs --target-dir ./static/img
   ```
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