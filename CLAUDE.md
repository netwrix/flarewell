# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two main tools for documentation processing:

1. **HTML to Markdown Converter (`app.py`)** - A Python tool that converts HTML documentation (particularly from MadCap Flare) to Markdown format while preserving folder structure and centralizing images.

2. **MDX Validation Test Suite (`mdx-test-suite.js`)** - A Node.js tool that validates MDX files and provides detailed error reporting with context.

## Important Directory Information

**Source Documentation Directory**: `/Users/jordan.violet/documents/product_docs`

This directory contains product documentation that needs to be converted from HTML to Markdown. You should:
- **NEVER modify any files in this directory** - only read them
- Test with the entire `product_docs` directory or any of its subdirectories
- Always treat this as a read-only source directory

## Testing Guidelines

- **Always cleanup test files after testing**: When you create test output directories or files during conversion/validation, remove them after testing is complete to keep the working directory clean
- Use temporary output directories like `test_output/` or `tmp_output/` for testing
- After validating the conversion works, delete the test output directory
- **Test after every change**: After making any modification to the application code, immediately run a test to confirm the changes work correctly. If the test fails, continue updating the code until the test passes

## Commands

### HTML to Markdown Conversion

```bash
# Convert entire product docs directory
python app.py /Users/jordan.violet/documents/product_docs output_dir

# Convert a specific product's documentation
python app.py /Users/jordan.violet/documents/product_docs/ProductName output_dir

# With verbose output
python app.py /Users/jordan.violet/documents/product_docs output_dir --verbose

# Flatten redundant nested directories
python app.py /Users/jordan.violet/documents/product_docs output_dir --flatten

# Add Docusaurus frontmatter
python app.py /Users/jordan.violet/documents/product_docs output_dir --docusaurus

# Find where an image is referenced
python app.py /Users/jordan.violet/documents/product_docs output_dir --find-image "image-name.png"

# Dry run (show what would be converted)
python app.py /Users/jordan.violet/documents/product_docs output_dir --dry-run
```

### MDX Validation

```bash
# Test all converted markdown files
node mdx-test-suite.js output_dir/

# Test a specific product's converted docs
node mdx-test-suite.js output_dir/ProductName/

# Test a single file
node mdx-test-suite.js output_dir/guide/intro.md

# Test using glob pattern
node mdx-test-suite.js "output_dir/**/*.md"

# Specify custom output report file
node mdx-test-suite.js output_dir/ --output=test.json
```

### Development Setup

```bash
# Activate Python virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install Python dependencies (if requirements.txt exists)
pip install beautifulsoup4 markdownify

# Install Node.js dependencies for MDX testing
npm install @mdx-js/mdx to-vfile fast-glob chalk ora table
```

## Architecture

### HTML to Markdown Converter (`app.py`)

The converter follows a two-pass approach:

1. **First Pass**: Scans all HTML files to identify referenced images, avoiding copying unreferenced images.

2. **Second Pass**: Processes HTML files:
   - Converts HTML to Markdown using BeautifulSoup and markdownify
   - Processes and relocates images to a centralized `static/images` directory
   - Updates internal document links from `.html` to `.md`
   - Cleans MadCap Flare-specific elements
   - Handles custom configuration tags by wrapping them in code blocks
   - Optionally flattens redundant directory structures
   - Optionally adds Docusaurus-compatible frontmatter

Key features:
- Preserves folder structure (with optional flattening)
- Centralizes images while maintaining correct relative paths
- Handles various HTML file extensions (html, htm, xhtml, etc.)
- Provides detailed verbose output for debugging
- Supports dry-run mode for preview

### MDX Validation Test Suite (`mdx-test-suite.js`)

A simple test suite that validates if markdown files can be successfully compiled as MDX.

Features:
- Test single files or entire directories
- Support for glob patterns
- Simple pass/fail validation
- Structured JSON report output

The test is straightforward: if a file can be compiled as MDX, it passes. If not, it fails with error details including line/column numbers when available.

## Key Implementation Details

### Image Path Resolution
The converter resolves image paths relative to the input directory and maintains the same structure in the output's static directory. When flattening is enabled, redundant nested directories are removed while preserving the logical structure.

**Important**: All image references in the converted markdown files use the full absolute path starting with `/static/`. For example:
- An image at `/static/img/1secure/admin/AlertsList.png` will be referenced as `/static/img/1secure/admin/AlertsList.png` (not `/img/1secure/admin/AlertsList.png`)
- The `/static` prefix is always included - never assume Docusaurus will add it automatically

### Link Processing
Internal document links are updated during conversion, accounting for:
- File extension changes (`.html` → `.md`)
- Directory structure changes when flattening is enabled
- URL fragments and query parameters preservation

### Error Handling
Both tools provide detailed error reporting:
- The converter logs warnings for missing images and failed conversions
- The MDX validator provides context-aware error messages with suggestions

### Custom Tag Handling
The converter detects configuration and custom XML tags (common in technical documentation) and wraps them appropriately in code blocks to prevent MDX parsing errors.