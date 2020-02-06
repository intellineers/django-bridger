import pytest

from bridger.enums import Button, Unit


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


class TestButton:
    @pytest.mark.parametrize(
        "method, buttons",
        [
            (
                "buttons",
                [
                    Button.REFRESH.value,
                    Button.NEW.value,
                    Button.DELETE.value,
                    Button.SAVE.value,
                    Button.SAVE_AND_CLOSE.value,
                    Button.SAVE_AND_NEW.value,
                ],
            ),
            (
                "create_buttons",
                [
                    Button.SAVE.value,
                    Button.SAVE_AND_CLOSE.value,
                    Button.SAVE_AND_NEW.value,
                    Button.RESET.value,
                ],
            ),
            (
                "custom_buttons",
                [
                    Button.DROPDOWN.value,
                    Button.HYPERLINK.value,
                    Button.WIDGET.value,
                    Button.ACTION.value,
                ],
            ),
        ],
    )
    def test_methods(self, method, buttons):
        assert getattr(Button, method)() == buttons

