from enum import Enum
from bridger.utils.enum import ChoiceEnum

class WBColor(Enum):
    GREEN_LIGHT = 'rgb(214, 229, 145)'
    GREEN = 'rgb(182, 223, 18)'
    GREEN_DARK = 'rgb(111, 181, 68)'
    RED_LIGHT = 'rgb(244, 132, 116)'
    RED = 'rgb(250, 84, 62)'
    RED_DARK = 'rgb(224, 57, 49)'
    YELLOW_LIGHT = 'rgb(247, 232, 113)'
    YELLOW = 'rgb(247, 207, 77)'
    YELLOW_DARK = 'rgb(247, 190, 47)'
    GREY = 'rgb(133, 144, 162)'
    BLUE_LIGHT = 'rgb(104, 198, 224)'
    BLUE = 'rgb(69, 112, 224)'
    BLUE_DARK = 'rgb(33, 26, 233)'

class ColorProduct(ChoiceEnum):
    BLACK_1="#3C4859"
    BLACK_2="#6D7683"
    BLACK_3="#9EA3AC"
    BLACK_4="#CED1D5"
    DARK_BLUE_1="#0585FF"
    DARK_BLUE_2="#69B6FF"
    DARK_BLUE_3="#B4DAFF"
    LIGHT_BLUE_1="#70D6FF"
    LIGHT_BLUE_2="#A9E7FF"
    LIGHT_BLUE_3="#D4F3FF"
    TURQUOISE_DARK_1="#01ABAA"
    TURQUOISE_DARK_2="#67CDCC"
    TURQUOISE_DARK_3="#B3E6E5"
    TURQUOISE_LIGHT_1="#05D6A1"
    TURQUOISE_LIGHT_2="#69E7C6"
    TURQUOISE_LIGHT_3="#ADF1E0"
    GREEN_1="#8CD867"
    GREEN_2="#BAE8A4"
    GREEN_3="#DDF3D1"
    PURPLE_DARK_1="#5624DA"
    PURPLE_DARK_2="#9A7CE9"
    PURPLE_DARK_3="#CCBDF4"
    PURPLE_LIGHT_1="#A258E5"
    PURPLE_LIGHT_2="#C79BEF"
    PURPLE_LIGHT_3="#E3CDF7"
    PINK_1="#EF476F"
    PINK_2="#F591A9"
    PINK_3="#FAC8D4"
    YELLOW_1="#FFD166"
    YELLOW_2="#FFE8B2" 

    @classmethod
    def get_gradient(cls, color):
        colors = cls.values()
        color_value = cls[color].value
        index = colors.index(color_value)
        if index == -1:
            return colors
        else:
            return colors[index:] + colors[:index]

class TransparencyMixin:

    def get_cell_formatting(self, request):
        return [
            {
                'column': None,
                'conditions': [
                    {
                        'condition': None,
                        'style': {
                            'backgroundColor': f'rgba(255, 255, 255, {getattr(self, "TRANSPARENCY", 0.4)})'
                        }
                    },
                ]
            }
        ]
