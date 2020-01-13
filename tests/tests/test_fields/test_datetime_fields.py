from datetime import date, datetime, time

import pytest
import pytz
from django.test import override_settings
from rest_framework.exceptions import ValidationError

from bridger.serializers import DateField, DateTimeField, TimeField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestDateTimeField:
    def setup_method(self):
        self.field = DateTimeField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [
            ("2019-01-01T10:00", datetime(2019, 1, 1, 11, 0)),
            ("2019-01-01T10:00Z", datetime(2019, 1, 1, 11, 0)),
            ("2019-01-01T10:00+01:00", datetime(2019, 1, 1, 10, 0)),
            ("2019-01-01T10:00:00Z", datetime(2019, 1, 1, 11, 0)),
            ("2019-01-01T10:00:00+00:00", datetime(2019, 1, 1, 11, 0)),
            ("2019-01-01T10:00:00+01:00", datetime(2019, 1, 1, 10, 0)),
            ("2019-01-01T10:00:00.0000Z", datetime(2019, 1, 1, 11, 0)),
            ("2019-01-01T10:00:00.0000+01:00", datetime(2019, 1, 1, 10, 0)),
        ],
    )
    @override_settings(TIME_ZONE="UCT", USE_TZ=True)
    def test_to_internal_value(self, input, expected):
        expected = pytz.timezone("Europe/Berlin").localize(expected)
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", ["", "200-00-10", [], {}, None])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    @override_settings(TIME_ZONE="Europe/Berlin")
    def test_to_representation_non_utc(self):
        localized_dt = pytz.timezone("Europe/Berlin").localize(
            datetime(2019, 1, 1, 10, 0)
        )
        assert self.field.to_representation(localized_dt) == "2019-01-01T10:00:00+01:00"

    @override_settings(TIME_ZONE="UCT", USE_TZ=True)
    def test_to_representation_non_utc(self):
        localized_dt = pytz.timezone("UCT").localize(datetime(2019, 1, 1, 10, 0))
        assert self.field.to_representation(localized_dt) == "2019-01-01T10:00:00Z"

    def test_field_type(self):
        assert self.field.field_type == BridgerType.DATETIME.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "decorators": [],
        }


class TestDateField:
    def setup_method(self):
        self.field = DateField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [(date(2019, 1, 1), date(2019, 1, 1)), ("2019-01-01", date(2019, 1, 1))],
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", ["", "200-00-10", [], {}, None])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_to_representation(self):
        assert self.field.to_representation(date(2019, 1, 1)) == "2019-01-01"

    def test_field_type(self):
        assert self.field.field_type == BridgerType.DATE.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "decorators": [],
        }


class TestTimeField:
    def setup_method(self):
        self.field = TimeField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [
            (time(10, 0), time(10, 0)),
            ("10:00", time(10, 0)),
            ("10:00:00", time(10, 0)),
            ("10:00:00.0000", time(10, 0)),
        ],
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", ["", "111", [], {}, None])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_to_representation(self):
        assert self.field.to_representation(time(10, 0, 0, 0)) == "10:00:00"

    def test_field_type(self):
        assert self.field.field_type == BridgerType.TIME.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "decorators": [],
        }
