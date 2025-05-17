# Flarewell - MadCap Flare to Docusaurus Converter

A Python tool to convert MadCap Flare projects or HTML exports to Docusaurus-compatible Markdown.

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

## Features

- Convert Flare project files (`.flprj`, `.fltoc`, etc.) to Markdown with proper frontmatter
- Convert Flare HTML output to Markdown
- Maintain folder/file structure or suggest an improved structure using LLM
- Process Flare variables, snippets, and conditions
- Convert Flare-specific UI elements to Docusaurus equivalents (admonitions, expandable sections, etc.)
- Generate Docusaurus sidebar configuration
- Analyze Flare projects to identify production vs test/draft content
- Fix references in already-converted Markdown files
- Automatically relocate images to a `static` directory next to your docs

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
- `convert`: Transform Flare content to Docusaurus Markdown
- `fix-links`: Update internal links in already-converted Markdown files
- `analyze`: Examine a Flare project to identify production content

### Convert Command

Convert a Flare project to Docusaurus Markdown:

```bash
flarewell convert --input-dir /path/to/flare/project --output-dir /path/to/docusaurus/docs
```

Convert HTML output from Flare:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --input-type html
```

Convert HTML to generic Markdown without Docusaurus front matter:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir ./docs --input-type html --markdown-style markdown
```

Convert and automatically fix links in one step:

```bash
flarewell convert --input-dir /path/to/flare/html --output-dir /path/to/docusaurus/docs --input-type html --fix-links
```

Converted images will be moved to a `static` directory next to your output docs automatically.


#### Using LLM for Structure Suggestions

To use an LLM to suggest an improved folder/file structure:

```bash
flarewell convert --input-dir /path/to/flare/project --output-dir /path/to/docusaurus/docs --use-llm --llm-api-key YOUR_API_KEY
```

You can also set your API key via environment variable:

```bash
export FLAREWELL_LLM_API_KEY=YOUR_API_KEY
flarewell convert --input-dir /path/to/flare/project --output-dir /path/to/docusaurus/docs --use-llm
```

#### Convert Options

- `--input-dir, -i`: Directory containing Flare project or HTML output
- `--output-dir, -o`: Directory to output Docusaurus-compatible Markdown files
- `--input-type`: Type of input (`project` or `html`), default is `project`
- `--preserve-structure`: Preserve the original folder/file structure (default: `True`)
- `--use-llm`: Use LLM to suggest an improved folder/file structure
- `--llm-api-key`: API key for the LLM service (or set via `FLAREWELL_LLM_API_KEY` environment variable)
- `--llm-provider`: LLM provider to use (`openai` or `anthropic`), default is `openai`
- `--target`: Specify a specific target to convert
- `--exclude-dir`: Directory patterns to exclude from conversion (can be used multiple times)
- `--debug`: Enable debug mode for detailed logging
- `--fix-links`: Fix links in converted Markdown files after conversion

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


### Analyze Command

The analyze command helps identify which parts of a Flare project are actively used in production and which might be test, draft, or deprecated content.

Get a full analysis of a Flare project:

```bash
flarewell analyze --input-dir /path/to/flare/project
```

List all targets in a project:

```bash
flarewell analyze --input-dir /path/to/flare/project --list-targets
```

Get folder statistics:

```bash
flarewell analyze --input-dir /path/to/flare/project --folder-stats
```

Output analysis to a JSON file:

```bash
flarewell analyze --input-dir /path/to/flare/project --output-file analysis.json
```

#### Analyze Options

- `--input-dir, -i`: Directory containing Flare project
- `--output-file, -o`: Output file for analysis results (JSON format)
- `--list-targets`: List all targets in the project
- `--list-tocs`: List all TOCs in the project
- `--folder-stats`: Show statistics about folders in the project

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