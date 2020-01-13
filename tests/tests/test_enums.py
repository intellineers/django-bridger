import pytest

from bridger.enums import Unit


class TestUnit:
    @pytest.mark.parametrize("unit", [Unit.FRACTION, Unit.REM, Unit.PIXEL])
    @pytest.mark.parametrize("value", ["1.0", 1.0, 1])
    def test_unit(self, unit, value):
        assert unit.unit(value) == f"{float(value)}{unit.value}"

    @pytest.mark.parametrize("unit", [Unit.FRACTION, Unit.REM, Unit.PIXEL])
    @pytest.mark.parametrize(
        "value, exception", [("a", ValueError), (None, AssertionError)]
    )
    def test_unit_fail(self, unit, value, exception):
        with pytest.raises(exception):
            unit.unit(value)
