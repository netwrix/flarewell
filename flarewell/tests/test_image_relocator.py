"""
Tests for the image relocator functionality.
"""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from flarewell.image_relocator import ImageRelocator


def create_test_structure(base_dir):
    """Create a test directory structure with Markdown files and images."""
    # Create main content file
    content_dir = base_dir / "content"
    content_dir.mkdir(exist_ok=True)
    
    # Create subfolders for content
    docs_dir = content_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Create subfolder for images
    images_dir = content_dir / "Resources" / "Images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Create images subfolder
    product_images = images_dir / "product"
    product_images.mkdir(exist_ok=True)
    
    # Create test images (just empty files)
    (images_dir / "logo.png").touch()
    (images_dir / "banner.jpg").touch()
    (product_images / "screenshot1.png").touch()
    (product_images / "screenshot2.png").touch()
    
    # Create markdown files with image references
    with open(docs_dir / "index.md", "w") as f:
        f.write("""# Main Page
        
![Logo](../Resources/Images/logo.png)

Check out our product:

![Screenshot](../Resources/Images/product/screenshot1.png)
""")
    
    with open(docs_dir / "product.md", "w") as f:
        f.write("""# Product Page
        
![Banner](../Resources/Images/banner.jpg)

Features:

![Feature Screenshot](../Resources/Images/product/screenshot2.png)
""")
    
    return content_dir


class TestImageRelocator:
    """Test suite for the ImageRelocator class."""
    
    @pytest.fixture
    def test_setup(self):
        """Set up a temporary directory with test files."""
        # Create a temporary directory
        base_dir = Path(tempfile.mkdtemp())
        
        try:
            # Create test structure
            content_dir = create_test_structure(base_dir)
            
            # Create target directory for relocated images
            target_dir = base_dir / "static" / "img"
            target_dir.mkdir(parents=True, exist_ok=True)
            
            yield {
                "base_dir": base_dir,
                "content_dir": content_dir,
                "target_dir": target_dir
            }
            
        finally:
            # Clean up the temporary directory
            shutil.rmtree(base_dir)
    
    def test_image_relocation_with_structure_preserved(self, test_setup):
        """Test relocating images while preserving directory structure."""
        content_dir = test_setup["content_dir"]
        target_dir = test_setup["target_dir"]
        
        # Create the relocator
        relocator = ImageRelocator(
            source_dir=content_dir,
            target_dir=target_dir,
            preserve_structure=True,
            debug=True
        )
        
        # Run relocation
        stats = relocator.relocate()
        
        # Check that all images were relocated
        assert stats["images_relocated"] == 4
        
        # Check that all MD files were updated
        assert stats["files_updated"] == 2
        
        # Check that the images exist in the target directory
        assert (target_dir / "Resources" / "Images" / "logo.png").exists()
        assert (target_dir / "Resources" / "Images" / "banner.jpg").exists()
        assert (target_dir / "Resources" / "Images" / "product" / "screenshot1.png").exists()
        assert (target_dir / "Resources" / "Images" / "product" / "screenshot2.png").exists()
        
        # Check that the references in the markdown files were updated
        with open(content_dir / "docs" / "index.md", "r") as f:
            index_content = f.read()
            assert "../static/img/Resources/Images/logo.png" in index_content
            assert "../static/img/Resources/Images/product/screenshot1.png" in index_content
        
        with open(content_dir / "docs" / "product.md", "r") as f:
            product_content = f.read()
            assert "../static/img/Resources/Images/banner.jpg" in product_content
            assert "../static/img/Resources/Images/product/screenshot2.png" in product_content
    
    def test_image_relocation_without_structure(self, test_setup):
        """Test relocating images without preserving directory structure."""
        content_dir = test_setup["content_dir"]
        target_dir = test_setup["target_dir"]
        
        # Create the relocator
        relocator = ImageRelocator(
            source_dir=content_dir,
            target_dir=target_dir,
            preserve_structure=False,
            debug=True
        )
        
        # Run relocation
        stats = relocator.relocate()
        
        # Check that all images were relocated
        assert stats["images_relocated"] == 4
        
        # Check that all MD files were updated
        assert stats["files_updated"] == 2
        
        # Check that the images exist in the target directory at the flattened level
        assert (target_dir / "logo.png").exists()
        assert (target_dir / "banner.jpg").exists()
        assert (target_dir / "screenshot1.png").exists()
        assert (target_dir / "screenshot2.png").exists() 