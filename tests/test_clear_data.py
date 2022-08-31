import pytest

from src.clear_file import ClearDataFiles


class TestClearDataFiles:
    @pytest.mark.clear_data
    def test_check_if_the_file_exists(self):
        with pytest.raises(FileNotFoundError):
            ClearDataFiles('tests/test_group2.txt')

    @pytest.mark.clear_data
    def test_get_messages(self):
        group = ClearDataFiles('tests/test_file_folder/test_group.txt')

        assert len(group.messages) == 10

    @pytest.mark.clear_data
    def test_get_info_messages(self):
        group = ClearDataFiles('tests/test_file_folder/test_group.txt')

        assert len(group.info_messages) == 2

    @pytest.mark.clear_data
    def test_get_file(self):
        group = ClearDataFiles('tests/test_file_folder/test_group.txt')

        assert group.file == 'tests/test_file_folder/test_group.txt'
