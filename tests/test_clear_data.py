import pytest

from src.clear_file import BaseClearDataFile


@pytest.mark.BaseClearDataFile
class TestClearDataFiles:
    def setup_method(self):
        self.file = '../tests/test_file_folder/test_group.txt'
        self.clear_data = BaseClearDataFile(self.file)

    def test_check_if_the_file_exists(self):
        with pytest.raises(FileNotFoundError):
            BaseClearDataFile('tests/test_group2.txt')

    def test_get_messages_ans_info_messages(self):
        assert len(self.clear_data.messages) == 10
        assert len(self.clear_data.info_messages) == 2

    def test_get_file(self):
        assert self.clear_data.path_file == self.file


