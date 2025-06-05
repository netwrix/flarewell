# HTML to Markdown Converter

A Python tool that converts HTML documentation (particularly from MadCap Flare) to Markdown format while preserving folder structure and centralizing images. Includes an MDX validation test suite to ensure the converted files are compatible with MDX processors.

## Features

### HTML to Markdown Conversion (app.py)
- Converts HTML files (`.html`, `.htm`, `.xhtml`) to Markdown (`.md`)
- Preserves directory structure with optional flattening
- Centralizes all images in a `static/img` directory
- **Intelligent image deduplication** - detects identical images and stores only one copy
- Updates all internal links to reference the new `.md` files
- Handles MadCap Flare specific elements (breadcrumbs, dropdowns, etc.)
- **Cross-reference resolution** - maintains anchor links between documents
- **Heading ID preservation** - converts MadCap anchors to Docusaurus-compatible IDs
- Validates converted files for MDX compatibility
- Supports dry-run mode for previewing changes
- Creates an `image-manifest.json` file tracking all image usage

### MDX Validation Suite (mdx-test-suite.js)
- Tests if markdown files can compile as MDX
- Recursively scans directories for `.md` and `.mdx` files
- Supports single files, directories, or glob patterns
- Provides error reporting with line/column numbers
- Automatically excludes `node_modules` and `.git` directories
- Generates JSON test reports
- Returns appropriate exit codes for CI/CD integration

## Installation

1. Clone this repository
2. Set up Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install beautifulsoup4 markdownify
   ```
4. Install Node.js dependencies (for MDX testing):
   ```bash
   npm install @mdx-js/mdx fast-glob chalk
   ```

## Usage

### Basic Conversion

Convert HTML documentation to Markdown:

```bash
python app.py /path/to/html/docs /path/to/output
```

### Common Options

- **Verbose output** - See detailed conversion progress:
  ```bash
  python app.py /path/to/html/docs /path/to/output --verbose
  ```

- **Flatten directories** - Remove redundant nested directories (e.g., `Product/Product/docs` → `Product/docs`):
  ```bash
  python app.py /path/to/html/docs /path/to/output --flatten
  ```

- **Add Docusaurus frontmatter** - Add YAML frontmatter for Docusaurus compatibility:
  ```bash
  python app.py /path/to/html/docs /path/to/output --docusaurus
  ```

- **Lowercase filenames** - Convert all filenames and directories to lowercase:
  ```bash
  python app.py /path/to/html/docs /path/to/output --lowercase-filenames
  ```

- **Dry run** - Preview what would be converted without creating files:
  ```bash
  python app.py /path/to/html/docs /path/to/output --dry-run
  ```

- **Find image references** - Locate where a specific image is used:
  ```bash
  python app.py /path/to/html/docs /path/to/output --find-image "logo.png"
  ```

- **List files** - Show all files that will be processed before converting:
  ```bash
  python app.py /path/to/html/docs /path/to/output --list-files
  ```

### Testing Converted Files

After conversion, validate that the Markdown files are MDX-compatible:

```bash
# Test entire output directory
node mdx-test-suite.js /path/to/output

# Test specific subdirectory
node mdx-test-suite.js /path/to/output/ProductName

# Test single file
node mdx-test-suite.js /path/to/output/guide/intro.md

# Save test report with custom name
node mdx-test-suite.js /path/to/output --output=validation-report.json
```

## Output Structure

After conversion, your files will be organized as follows:

```
output/                    # Your specified output directory
├── Product1/             # Converted markdown files maintain structure
│   ├── guide/
│   │   └── intro.md
│   └── api/
│       └── reference.md
└── Product2/
    └── docs/
        └── overview.md

static/                   # Parallel to output directory
└── img/                 # All images centralized here (note: 'img' not 'images')
    ├── image-manifest.json  # Tracks all images, their usage, and deduplication
    ├── Product1/        # Images maintain source structure
    │   ├── guide/
    │   │   └── screenshot.png
    │   └── api/
    │       └── diagram.png
    └── Product2/
        └── docs/
            └── logo.png
```

## Advanced Features

### Image Deduplication
The converter automatically detects duplicate images (based on content hash) and stores only one copy. The `image-manifest.json` file tracks:
- Original image paths
- Which documents use each image
- Deduplication statistics

### Cross-Reference Resolution
The converter maintains links between documents by:
- Building anchor mappings during the first pass
- Converting MadCap-style anchors to Docusaurus-compatible heading IDs
- Resolving cross-file references automatically

### MDX Compatibility Fixes
The converter automatically handles common MDX issues:
- Escapes curly braces in code blocks
- Wraps HTML-like tags to prevent JSX interpretation
- Fixes comparison operators in tables
- Handles solo backticks and other edge cases

## Example Workflow

1. **Convert documentation with all features:**
   ```bash
   python app.py /Users/jordan.violet/documents/product_docs ./docs_output \
     --flatten --verbose --docusaurus --lowercase-filenames
   ```

2. **Validate the converted files with verbose output:**
   ```bash
   node mdx-test-suite.js ./docs_output --verbose --output=mdx-test-report.json
   ```

3. **Review the validation report:**
   ```bash
   cat mdx-test-report.json | grep -A 5 '"summary"'
   ```

4. **Check image deduplication results:**
   ```bash
   cat static/img/image-manifest.json | jq '.[] | select(.reference_count > 1)'
   ```

5. **Clean up (if this was just a test):**
   ```bash
   rm -rf docs_output static mdx-test-report.json
   ```

## Important Notes

- **Source files are never modified** - The tool only reads from the input directory
- **Images are copied, not moved** - Original images remain in the source directory
- **Only referenced images are copied** - Unreferenced images are skipped to save space
- **Links are automatically updated** - All `.html` references become `.md` references
- **Static directory location** - The `static/img` directory is created parallel to your output directory
- **Image deduplication** - Identical images are stored only once, saving disk space

## Troubleshooting

### MDX Validation Failures

If some files fail MDX validation, the test report will show:
- File path
- Error message
- Line and column number (when available)

Common issues:
- HTML entities in script tags (`&lt;`, `&gt;`, `&amp;`)
- Unclosed HTML/JSX tags
- Invalid JavaScript in MDX context
- Curly braces in code blocks (automatically fixed by converter)

### Missing Images

If images appear broken after conversion:
1. Check if the image was referenced in the HTML
2. Use `--find-image` to locate references
3. Verify the image exists in the source directory
4. Check the `static/img` directory structure
5. Review `image-manifest.json` for deduplication info

### Performance

For large documentation sets:
- The tool processes files in two passes:
  1. First pass: Scans for images and builds anchor mappings (faster)
  2. Second pass: Converts files and processes content (slower)
- Expect ~1-2 seconds per file depending on complexity
- Image deduplication saves both time and disk space

## Command Reference

### app.py Options

| Option | Description |
|--------|-------------|
| `input_dir` | Source directory containing HTML files |
| `output_dir` | Destination directory for Markdown files |
| `--verbose, -v` | Show detailed progress information |
| `--flatten` | Remove redundant nested directories |
| `--docusaurus` | Add Docusaurus-compatible frontmatter |
| `--lowercase-filenames` | Convert all filenames to lowercase |
| `--dry-run` | Preview without creating files |
| `--find-image IMAGE` | Find where an image is referenced |
| `--list-files` | List all files before converting |

### mdx-test-suite.js Options

| Option | Description |
|--------|-------------|
| `path` | File, directory, or glob pattern to test |
| `--output=FILE` | Save test report to JSON file (default: mdx-test-report.json) |
| `--help, -h` | Show help message |

## License

[Your license here]

## Contributing

[Your contributing guidelines here]