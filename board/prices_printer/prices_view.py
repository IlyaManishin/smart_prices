import framebuf

from .e_paper import epdif
from .e_paper import epd2in13b
from .e_paper.config import EPD_HEIGHT, EPD_WIDTH
from . import fb_helper


class DiscountData:
    sale_price: int = None
    discount: int = None

    def __init__(self, sale_price=None, discount=None):
        self.sale_price = sale_price
        self.discount = discount


class PriceData:
    name: str
    base_price: int
    discount_data: DiscountData

    def __init__(self, name, base_price, discount_data: DiscountData = None):
        self.name = name
        self.base_price = base_price
        self.discount_data = discount_data


BASE_X_OFF = 10

CH_SIZE_X = 8
CH_SIZE_Y = 8

MAX_TITLE_LINES = 2
TITLE_SCALE = 1.7
TITLE_MAX_LINES = 2
TITLE_Y_OFF = 10


def _display_rotated(epd, fb_b_rot, fb_r_rot):
    epd.display(fb_helper.frame_buf_rot90(fb_b_rot, EPD_HEIGHT, EPD_WIDTH),
                fb_helper.frame_buf_rot90(fb_r_rot, EPD_HEIGHT, EPD_WIDTH))


def _show_discounted_data(price_data: PriceData, fb_b_rot, fb_r_rot):
    fb_helper.draw_board(fb_r_rot, EPD_HEIGHT, EPD_WIDTH, 2)


def _title_to_lines(title: str, scale: float):
    max_text_width = EPD_HEIGHT - 2 * BASE_X_OFF
    ch_size_x = round(CH_SIZE_X * scale)
    ch_in_line = max_text_width // ch_size_x

    words = title.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= ch_in_line:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)
    return lines


def _write_title(fb_rot, title):
    scale = TITLE_SCALE
    lines = _title_to_lines(title, scale)
    if len(lines) > MAX_TITLE_LINES:
        scale = 1
        lines = _title_to_lines(title, scale)

    y_cur = TITLE_Y_OFF
    ch_size_y = round(CH_SIZE_Y * scale)
    for line in lines:
        fb_helper.draw_text_scaled(fb_rot, line, BASE_X_OFF, y_cur, 0, scale)
        y_cur += ch_size_y + 2


def _show_base_data(price_data: PriceData, fb_b_rot, fb_r_rot):
    pass


def _show_price_data(price_data: PriceData, fb_b_rot, fb_r_rot):
    _write_title(fb_b_rot, price_data.name)

    if not price_data.discount_data:
        _show_base_data(price_data, fb_b_rot, fb_r_rot)
    else:
        _show_discounted_data(price_data, fb_b_rot, fb_r_rot)


def write_price_data(price_data: PriceData):
    epd = epd2in13b.EPD(epdif.spi, epdif.cs, epdif.dc, epdif.rst, epdif.busy)
    epd.init()

    buf_size = (EPD_WIDTH + 7) // 8 * EPD_HEIGHT
    black_buf = bytearray(buf_size)
    red_buf = bytearray(buf_size)

    fb_b_rot = framebuf.FrameBuffer(
        black_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)
    fb_r_rot = framebuf.FrameBuffer(
        red_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)

    fb_b_rot.fill(1)
    fb_r_rot.fill(1)

    _show_price_data(price_data, fb_b_rot, fb_r_rot)
    _display_rotated(epd, fb_b_rot, fb_r_rot)
