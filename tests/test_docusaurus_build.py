import os
import subprocess
import pytest
import tempfile
import shutil
import re

def run_command(cmd, cwd=None):
    """Run a shell command and return the output and exit code."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=cwd
    )
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

def fix_mdx_issues(docs_dir):
    """Apply common MDX fixes to problematic files."""
    # Find all Markdown files
    markdown_files = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    # Patterns to fix
    fixes_applied = 0
    
    for md_file in markdown_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store original content to check if changes were made
        original_content = content
        
        # Fix 1: Escape curly braces in code blocks
        code_block_pattern = r'```(?P<lang>[^\n]*)\n(?P<code>.*?)```'
        
        def fix_code_block(match):
            lang = match.group('lang').strip()
            code = match.group('code')
            
            # If no language specified, add 'text'
            if not lang:
                lang = 'text'
                
            # Escape curly braces in code blocks
            code = code.replace('{', '\\{').replace('}', '\\}')
            
            # Fix Windows command prompt % signs
            if lang.lower() in ['bash', 'cmd', 'powershell', 'shell', 'bat', 'console', 'sh', 'zsh']:
                code = code.replace('%', '\\%')
                
            return f'```{lang}\n{code}```'
        
        content = re.sub(code_block_pattern, fix_code_block, content, flags=re.DOTALL)
        
        # Fix 2: Escape inline code with curly braces
        inline_code_pattern = r'`([^`]*?(\{|\})[^`]*?)`'
        
        def fix_inline_code(match):
            code = match.group(1)
            fixed_code = code.replace('{', '\\{').replace('}', '\\}')
            return f"`{fixed_code}`"
        
        content = re.sub(inline_code_pattern, fix_inline_code, content)
        
        # Fix 3: Fix HTML-like tags in text that MDX interprets as JSX
        jsx_pattern = r'(?<!\`|```)((<[a-zA-Z][^<>]*>[^<>]*<\/[a-zA-Z][^<>]*>)|(<[a-zA-Z][^<>]*\/>))(?!\`|```)'
        
        def fix_potential_jsx(match):
            jsx = match.group(0)
            return f'`{jsx}`'
        
        content = re.sub(jsx_pattern, fix_potential_jsx, content)
        
        # Fix 4: Fix malformed URLs
        malformed_url_pattern = r'(\[\w+\]\()(\w+://[^)]+\))\.(\w+)(\))'
        content = re.sub(malformed_url_pattern, r'\1\2\4', content)
        
        # Only write back if changes were made
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            fixes_applied += 1
    
    return fixes_applied

def _get_option(config, name, default=None):
    """Safely get a pytest command line option if declared."""
    try:
        return config.getoption(name)
    except ValueError:
        return default


@pytest.fixture
def docusaurus_dir(request):
    """Fixture that returns the Docusaurus directory path."""
    # Default to a parent directory of the workspace
    docusaurus_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_website",
    )

    # Allow overriding the docusaurus directory using a command line option
    override = _get_option(request.config, "--docusaurus-dir")
    if override:
        docusaurus_dir = override
    
    # Verify the directory exists and has package.json
    package_json = os.path.join(docusaurus_dir, 'package.json')
    assert os.path.exists(package_json), f"No package.json found in {docusaurus_dir}"
    
    return docusaurus_dir

def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--docusaurus-dir", 
        default=None,
        help="Path to Docusaurus directory for build testing"
    )
    parser.addoption(
        "--fix-mdx",
        action="store_true",
        help="Attempt to fix MDX issues before testing"
    )
    parser.addoption(
        "--full-build",
        action="store_true",
        help="Perform a full build (default is production build)"
    )

def test_docusaurus_build(docusaurus_dir, request):
    """Test that Docusaurus can build without MDX errors."""
    # Apply MDX fixes if requested
    if _get_option(request.config, "--fix-mdx"):
        docs_dir = os.path.join(docusaurus_dir, 'docs')
        fixes_applied = fix_mdx_issues(docs_dir)
        print(f"\nApplied MDX fixes to {fixes_applied} files")
    
    # Determine build command
    full_build = bool(_get_option(request.config, "--full-build"))
    build_cmd = "npm run build" if full_build else "npm run build -- --no-minify"
    
    # Run the build
    print(f"\nRunning '{build_cmd}' in {docusaurus_dir}")
    stdout, stderr, exit_code = run_command(build_cmd, cwd=docusaurus_dir)
    
    # Check for compile errors in output
    mdx_errors = re.findall(r'MDX compilation failed for file "([^"]+)"', stderr)
    
    # Print diagnostic info on failure
    if exit_code != 0 or mdx_errors:
        print("\n=== BUILD FAILED ===")
        print("\nSTDOUT:")
        print(stdout)
        print("\nSTDERR:")
        print(stderr)
        
        if mdx_errors:
            print("\n=== MDX ERRORS ===")
            print(f"Found {len(mdx_errors)} files with MDX compilation errors:")
            for i, error_file in enumerate(mdx_errors[:10], 1):
                print(f"{i}. {os.path.basename(error_file)}")
            
            if len(mdx_errors) > 10:
                print(f"... and {len(mdx_errors) - 10} more files")
            
            print("\nTo fix these errors automatically, run:")
            print(f"pytest {__file__} --docusaurus-dir={docusaurus_dir} --fix-mdx")
    
    # Assert build succeeded
    assert exit_code == 0, f"Docusaurus build failed with exit code {exit_code}"
    assert not mdx_errors, f"Found {len(mdx_errors)} files with MDX compilation errors"
    
    print("\n=== BUILD SUCCEEDED ===")

if __name__ == "__main__":
    # Allow running directly with python -m
    pytest.main() 