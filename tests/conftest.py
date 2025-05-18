import shutil
from pathlib import Path
import pytest

@pytest.fixture
def clean_output_dir():
    output_dir = Path('tests/test_website/docs')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    yield output_dir
    # clean up after test
    if output_dir.exists():
        shutil.rmtree(output_dir)
