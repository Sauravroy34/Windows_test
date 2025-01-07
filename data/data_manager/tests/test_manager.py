import os
import re
from pathlib import Path,PurePosixPath
import pytest

from sunpy.data.data_manager.tests.mocks import MOCK_HASH, write_to_test_file


def test_override_file(manager, data_function, tmpdir):
    """
    Test the override_file functionality.
    """


    def override_file_tester(manager):
        """
        Function to test whether the file is /tmp/another_file.
        """
        print(manager.get("test_file"))
        assert 0
        assert (manager.get('test_file')) == Path(f"{folder}/another_file")


    # Outside the context manager file is default
    folder = (tmpdir.strpath)
    write_to_test_file(str(Path(f'{folder}/another_file')), 'a')

    with manager.override_file('test_file', f'file://{folder}/another_file'):
        # Inside the file is replaced
        data_function(override_file_tester)

    with manager.override_file('test_file', f'{folder}/another_file'):
        # Inside the file is replaced
        data_function(override_file_tester)

    # check the function works with hash provided
    with manager.override_file('test_file', f'file://{folder}/another_file', MOCK_HASH):
        data_function(override_file_tester)

    with pytest.raises(ValueError, match="Hash provided to override_file does not match hash of the file."):
        # check if functions errors with the wrong hash
        with manager.override_file('test_file', f'file://{folder}/another_file', 'wrong_hash'):
            # Inside the file is replaced
            data_function(override_file_tester)

    # Even after context manager call outside the file is default
    # data_function(default_tester)


