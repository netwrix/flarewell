# Flarewell

Convert MadCap Flare documentation projects to Docusaurus-compatible Markdown.

## Features

- Convert Flare project files (`.flprj`, `.fltoc`, etc.) to Markdown with proper frontmatter
- Convert Flare HTML output to Markdown
- Maintain folder/file structure or suggest an improved structure using LLM
- Process Flare variables, snippets, and conditions
- Convert Flare-specific UI elements to Docusaurus equivalents (admonitions, expandable sections, etc.)
- Generate Docusaurus sidebar configuration
- Analyze Flare projects to identify production vs test/draft content

## Installation

```bash
pip install flarewell
```

Or clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/flarewell.git
cd flarewell
pip install -e .
```

## Usage

Flarewell offers two main commands:
- `convert`: Transform Flare content to Docusaurus Markdown
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