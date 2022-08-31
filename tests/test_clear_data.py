import pytest

from src.clear_file import ClearDataFiles


@pytest.mark.clear_data
class TestClearDataFiles:
    def setup(self):
        self.file = 'tests/test_file_folder/test_group.txt'

    def test_check_if_the_file_exists(self):
        with pytest.raises(FileNotFoundError):
            ClearDataFiles('tests/test_group2.txt')

    def test_get_messages_ans_info_messages(self):
        group = ClearDataFiles(self.file)

        assert len(group.messages) == 10
        assert len(group.info_messages) == 2

    def test_get_file(self):
        group = ClearDataFiles(self.file)

        assert group.file == self.file
