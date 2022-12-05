from datetime import datetime

import pytest

from src.filters import FilterDataHandleBase
from src.models import FilterMessagesModel, MessageModel


@pytest.mark.FilterDataHandleBase
class TestFilterDataHandle:
    def setup_method(self):
        self.file = 'tests/test_file_folder/test_group.txt'
        self.filter_data = FilterDataHandleBase(self.file)

    def test_list_numbers(self):
        assert len(self.filter_data.get_list_of_numbers()) == 4

    def test_list_numbers_with_dates(self):
        start_date = datetime(2022, 6, 22)
        end_date = datetime(2022, 6, 23)
        assert len(self.filter_data.get_list_of_numbers(start_date, end_date)) == 2

    def test_count_messages(self):
        assert len(self.filter_data.get_message_count_by_phone()) == 4

    def test_extract_links(self):
        assert len(self.filter_data.extract_links()) == 1

    def test_group(self):
        assert self.filter_data.group_or_privaty == 'group' or 'private'


@pytest.mark.FilterMessagesModel
class TestFilterMessagesModel:
    def setup_method(self):
        self.file = 'tests/test_file_folder/test_group.txt'
        self.filter_data = FilterDataHandleBase(self.file)

    def test_filter_with_phone(self):
        filter_message = FilterMessagesModel(phone='Paulo Cruz')
        assert len(filter_message(self.filter_data.messages)) == 4

    def test_filter_with_message(self):
        filter_message = FilterMessagesModel(message='olá')
        assert len(filter_message(self.filter_data.messages)) == 3

    def test_filter_with_dates(self):
        start_date = datetime(2022, 6, 22)
        end_date = datetime(2022, 6, 23)
        filter_message = FilterMessagesModel(start_date=start_date, end_date=end_date)
        assert len(filter_message(self.filter_data.messages)) == 4

    def test_filter_with_list_phone(self):
        filter_message = FilterMessagesModel(list_phone=['@erickson', 'Paulo Cruz'])
        assert len(filter_message(self.filter_data.messages)) == 8

    def test_filter_with_all(self):
        start_date = datetime(2022, 6, 22)
        end_date = datetime(2022, 6, 23)
        filter_message = FilterMessagesModel(
            phone='@erickson',
            message='olá', start_date=start_date,
            end_date=end_date,
            list_phone=['@erickson'])
        assert isinstance(*filter_message(self.filter_data.messages), MessageModel)
        assert len(filter_message(self.filter_data.messages)) == 1
