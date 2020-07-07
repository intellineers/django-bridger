from datetime import date

import pytest
from rest_framework.test import APIRequestFactory

from bridger.utils.date import get_date_interval_from_get


class TestGetDateInterval:
    def setup_method(self):
        self.request_factory = APIRequestFactory()

    @pytest.mark.parametrize("start_key", ["start", "start_date", "from", "date_gte"])
    @pytest.mark.parametrize("start", [date(2010, 1, 1)])
    @pytest.mark.parametrize("end_key", ["end", "end_date", "to", "date_lte"])
    @pytest.mark.parametrize("end", [date(2010, 1, 1)])
    def test_get_date_interval_from_get(self, start_key, start, end_key, end):
        request = self.request_factory.get(
            path="", data={start_key: start.strftime("%Y-%m-%d"), end_key: end.strftime("%Y-%m-%d"),},
        )
        _start, _end = get_date_interval_from_get(request)

        assert _start == start
        assert _end == end

    def test_get_date_interval_from_get_none(self):
        request = self.request_factory.get(path="",)
        _start, _end = get_date_interval_from_get(request)

        assert _start is None
        assert _end is None

    def test_get_date_interval_from_get_wrong_date_format(self):
        request = self.request_factory.get(path="", data={"start": "abc", "end": "def"})
        _start, _end = get_date_interval_from_get(request)

        assert _start is None
        assert _end is None
