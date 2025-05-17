# Link Mapping System Guide

## Overview

The link mapping system in Flarewell solves the problem of broken references during conversion from MadCap Flare to Docusaurus. It handles the transformation of links from `.htm`/`.html` format to the appropriate Markdown paths.

## How It Works

The system consists of two main phases:

### 1. Registration Phase

Before any files are converted, the converter:

1. Scans all topics in the project
2. Creates a master registry that maps original file paths to their Markdown equivalents
3. Handles variations like case differences and different file extensions

```python
# The link mapper builds a comprehensive registry
link_mapper = LinkMapper(preserve_structure=True)
link_mapper.register_files(all_topics)
```

### 2. Transformation Phase

During conversion of each file, the system:

1. Parses the content to find all links (both Markdown `[text](link)` and HTML `<a href="link">text</a>`)
2. For each link, resolves its location relative to the current file
3. Transforms it to point to the appropriate Markdown file
4. Preserves link titles, attributes, and anchors

```python
# The link mapper transforms all links in the content
content = link_mapper.transform_links(content, current_file_path)
```

## Key Features

### Path Resolution

The system handles various path types:

- **Relative paths**: `../../path/to/file.htm` → `../../path/to/file`
- **Same-directory paths**: `file.htm` → `file`
- **Absolute paths**: `/path/to/file.htm` → `path/to/file`
- **Paths with anchors**: `file.htm#section` → `file#section`

### Link Preservation

The system carefully preserves:

- Link text: `[Link Text](path)` maintains the same text
- Title attributes: `[Text](path "Title")` keeps the title attribute
- Anchors: `[Text](path#anchor)` maintains the anchor reference

### Case Insensitivity

Links are matched case-insensitively to handle variations in path casing:

```
../../EnterpriseAuditor/file.htm
../../enterpriseauditor/file.htm
```

Both resolve to the same target file.

## Using the Link Mapper Directly

If you need to use the link mapper in your own code:

```python
from flarewell import LinkMapper

# Create a link mapper
mapper = LinkMapper(preserve_structure=True)

# Register files
files = [
    {"rel_path": "path/to/file1.htm", "title": "File 1"},
    {"rel_path": "path/to/file2.htm", "title": "File 2"}
]
mapper.register_files(files)

# Transform links in content
content = """
See [this page](path/to/file1.htm) for more information.
"""
current_file = "index.md"
transformed = mapper.transform_links(content, current_file)
```

## Debug Mode

For troubleshooting, you can enable debug mode:

```python
mapper = LinkMapper(preserve_structure=True, debug=True)
```

This will output detailed logging about:
- Files being registered
- Links being transformed
- Path resolution steps

## Advanced Configuration

### Structure Preservation

By default, the link mapper preserves the original file structure:

```python
mapper = LinkMapper(preserve_structure=True)
```

If you're using a custom structure (e.g., with the LLM reorganization feature), set:

```python
mapper = LinkMapper(preserve_structure=False)
```

This will use the new paths provided in the file information.

## Handling Special Cases

### External Links

External links (http://, https://, mailto:) are preserved as-is:

```
[External Link](https://example.com) → [External Link](https://example.com)
```

### Broken Links

For links to files not in the registry:
1. The extension is removed
2. The path is otherwise maintained

This ensures the link doesn't break completely even if the target file wasn't converted.

## Implementation Notes

The link mapper uses several strategies to ensure reliable link transformation:

1. **Path normalization**: All paths are normalized to use forward slashes and remove duplicates
2. **Multiple registration approaches**: Files are registered with and without extensions
3. **Relative path calculation**: For structure-preserved mode, proper relative paths are calculated
4. **Fallbacks**: If a link can't be resolved, it falls back to a simpler transformation 