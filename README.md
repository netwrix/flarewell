# HTML to Markdown Converter - Claude Instructions

<project_overview>
A Python tool that converts HTML documentation (particularly from MadCap Flare) to Markdown format while preserving folder structure and centralizing images with intelligent deduplication.
</project_overview>

## Core Functionality

<conversion_rules>
- **Input**: HTML files (`.html`, `.htm`, `.xhtml`)
- **Output**: Markdown files (`.md`)
- **Directory Structure**: Preserved except for images
- **Image Handling**: Centralized in `static/img/{productname}` directory
- **Filename Convention**: All lowercase with underscores replacing spaces
- **Path References**: Absolute paths from parent output directory
</conversion_rules>

## Key Features

<features>
<feature name="intelligent_deduplication">
- Detects identical images using content hashing
- Stores only one copy of duplicate images
- Tracks usage in `image-manifest.json`
</feature>

<feature name="link_preservation">
- Updates all internal `.html` links to `.md`
- Maintains anchor links between documents
- Resolves cross-file references automatically
</feature>

<feature name="image_centralization">
- All images stored in `/static/img/{mirror_doc_directory}`
- One image folder per product
- Only referenced images are copied
</feature>
</features>

## Installation & Setup

<setup_instructions>
```bash
# 1. Clone repository
git clone [repository_url]

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install beautifulsoup4 markdownify
```
</setup_instructions>

## Usage

<usage_examples>
<example name="basic">
```bash
python app.py /path/to/html/docs /path/to/output
```
</example>

<example name="verbose">
```bash
python app.py /path/to/html/docs /path/to/output --verbose
```
</example>
</usage_examples>

## Output Structure

<output_structure>
```
output/                    # Specified output directory
├── Product1/             # Markdown files (structure preserved)
│   ├── guide/
│   │   └── intro.md
│   └── api/
│       └── reference.md
└── Product2/
    └── docs/
        └── overview.md

static/                   # Parallel to output directory
└── img/                 # Centralized images (not 'images')
    ├── image-manifest.json  # Deduplication tracking
    ├── Product1/
    │   ├── guide/
    │   │   └── screenshot.png
    │   └── api/
    │       └── diagram.png
    └── Product2/
        └── docs/
            └── logo.png
```
</output_structure>

## Implementation Details

<processing_phases>
<phase number="1" name="scanning">
- Scan for images and build reference map
- Create anchor mappings for cross-references
- Build deduplication hash table
</phase>

<phase number="2" name="conversion">
- Convert HTML to Markdown
- Update all link references
- Copy unique images to static directory
- Generate image-manifest.json
</phase>
</processing_phases>

## Critical Requirements

<requirements>
<requirement priority="high">
- Never modify source files
- Preserve all internal links
- Handle MadCap Flare-specific HTML structures
</requirement>

<requirement priority="medium">
- Maintain readable Markdown output
- Optimize image storage through deduplication
- Generate comprehensive image manifest
</requirement>
</requirements>

## Error Handling

<error_scenarios>
<scenario name="missing_images">
- Log warning but continue processing
- Record in image-manifest.json
- Preserve image reference in Markdown
</scenario>

<scenario name="invalid_html">
- Attempt best-effort conversion
- Log parsing errors with file path
- Continue with next file
</scenario>

<scenario name="duplicate_output">
- Check for existing files
- Option to overwrite or skip
- Log conflicts
</scenario>
</error_scenarios>

## Performance Considerations

<performance>
- **Expected Speed**: ~1-2 seconds per file
- **Memory Usage**: Scales with image deduplication table
- **Disk Usage**: Reduced through image deduplication
- **Large Documentation Sets**: Two-pass processing for efficiency
</performance>

## Troubleshooting Guide

<troubleshooting>
<issue name="broken_images">
<cause>Image not referenced in HTML or missing from source</cause>
<solution>
1. Verify image exists in source
2. Check if referenced in HTML
3. Review image-manifest.json
4. Confirm static/img structure
</solution>
</issue>

<issue name="broken_links">
<cause>Cross-reference anchors not found</cause>
<solution>
1. Check anchor mappings in verbose output
2. Verify target document exists
3. Confirm anchor ID consistency
</solution>
</issue>
</troubleshooting>

## Command Reference

<cli_options>
| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `input_dir` | Required | Source HTML directory | - |
| `output_dir` | Required | Destination for Markdown | - |
| `--verbose, -v` | Flag | Show detailed progress | False |
| `--overwrite` | Flag | Overwrite existing files | False |
| `--skip-images` | Flag | Convert without copying images | False |
</cli_options>

## Testing Checklist

<testing>
- [ ] Basic HTML to Markdown conversion
- [ ] Image deduplication across multiple files
- [ ] Cross-file link resolution
- [ ] MadCap Flare specific elements
- [ ] Large documentation set performance
- [ ] Edge cases (empty files, broken HTML)
</testing>

## Future Enhancements

<enhancements>
- Support for custom CSS preservation
- Batch processing with progress bar
- Configuration file support
- Plugin system for custom transformations
</enhancements>