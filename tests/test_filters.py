from datetime import datetime

import pytest

from src.filters import FilterDataHandle


@pytest.mark.filter_data
class TestFilterDataHandle:
    def setup(self):
        self.file = 'tests/test_file_folder/test_group.txt'
        self.filter_data = FilterDataHandle(self.file)

    def test_list_numbers(self):
        assert len(self.filter_data.get_list_of_numbers()) == 4

    def test_list_numbers_with_dates(self):
        start_date = datetime(2022, 6, 22)
        end_date = datetime(2022, 6, 23)
        assert len(self.filter_data.get_list_of_numbers(start_date, end_date)) == 2
