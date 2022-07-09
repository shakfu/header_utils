import os
import shutil

import pytest

from header_utils import HeaderProcessor

@pytest.fixture
def app():
    target = 'tests/include'
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree('tests/include-before', target)
    return HeaderProcessor(path=target)

def test_application(app):
    print(os.getcwd())
    assert not app.dry_run
    app.process_headers()

