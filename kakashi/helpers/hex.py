from hikari.colors import Color, Colorish


class ColorImpl:
    @property
    def blue(self) -> Colorish:
        return Color(0x0000FF)

    @property
    def red(self) -> Colorish:
        return Color(0xFF0000)

    @property
    def cyan(self) -> Colorish:
        return Color(0x00FFFF)

    @property
    def green(self) -> Colorish:
        return Color(0x00FF00)

    @property
    def purple(self) -> Colorish:
        return Color(0x800080)

    @property
    def yellow(self) -> Colorish:
        return Color(0xFFFF00)

    @property
    def pink(self) -> Colorish:
        return Color(0xFFC0CB)


ColorHelper = ColorImpl()
