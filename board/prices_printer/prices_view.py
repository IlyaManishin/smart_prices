import framebuf

from .base_config import *
from .e_paper import epdif
from .e_paper.epd2in13b import EPD
from .e_paper.config import EPD_HEIGHT, EPD_WIDTH
from . import fb_helper


class PriceVal:
    price: int
    kopecks: int

    def __init__(self, price, kopecks):
        self.price = price
        self.kopecks = kopecks


class DiscountData:
    sale_price: PriceVal
    discount: int

    def __init__(self, sale_price: PriceVal, discount):
        self.sale_price = sale_price
        self.discount = discount


class PriceData:
    name: str
    base_price: PriceVal
    discount_data: DiscountData

    def __init__(self, name, base_price: PriceVal, discount_data: DiscountData = None):
        self.name = name
        self.base_price = base_price
        self.discount_data = discount_data


MAX_TITLE_LINES = 2
TITLE_SCALES = [1.7, 1.5, 1]
TITLE_MAX_LINES = 2
TITLE_Y_OFF = 5

PRICES_BLK_X = 120


def _display_rotated(epd, fb_b_rot, fb_r_rot):
    epd.display(fb_helper.frame_buf_rot90(fb_b_rot, EPD_HEIGHT, EPD_WIDTH),
                fb_helper.frame_buf_rot90(fb_r_rot, EPD_HEIGHT, EPD_WIDTH))


def _title_to_lines(title: str, scale: float):
    max_text_width = EPD_HEIGHT - 2 * BASE_X_OFF
    ch_size_x = round(CH_SZ_X * scale)
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


def _write_title(fb_rot, title) -> int:
    scale = None
    lines = []
    for scale in TITLE_SCALES:
        lines = _title_to_lines(title, scale)
        if len(lines) <= MAX_TITLE_LINES:
            break

    y_cur = TITLE_Y_OFF
    ch_size_y = round(CH_SZ_Y * scale)
    for line in lines:
        fb_helper.draw_text_scaled(
            fb_rot, line, BASE_X_OFF, y_cur, 0, scale, EPD_HEIGHT)
        y_cur += ch_size_y + 2

    border = 1
    fb_rot.fill_rect(BASE_X_OFF, y_cur, EPD_HEIGHT - 2 * BASE_X_OFF, border, 0)
    return y_cur + border


def _view_base_price(price_data: PriceData, fb_b_rot, fb_r_rot, y_min):
    pass


def _view_crossed_price(price_data: PriceData, fb_b_rot, fb_r_rot, y_min):
    pass


def _view_result_price(price_data: PriceData, fb_b_rot, fb_r_rot, y_min):
    pass


def _view_price_data_impl(price_data: PriceData, fb_b_rot, fb_r_rot):
    y_min = _write_title(fb_b_rot, price_data.name)

    if not price_data.discount_data:
        _view_base_price(price_data, fb_b_rot, fb_r_rot, y_min)
    else:
        fb_helper.draw_border(fb_r_rot, EPD_HEIGHT, EPD_WIDTH, 2)
        _view_result_price(price_data, fb_b_rot, fb_r_rot, y_min)

    fb_helper.write_logo(fb_b_rot, fb_r_rot, EPD_HEIGHT, EPD_WIDTH)


def view_price_data(price_data: PriceData):
    epd = EPD(epdif.spi, epdif.cs, epdif.dc, epdif.rst, epdif.busy)
    epd.init()

    buf_size = fb_helper.get_bytearr_size(EPD_HEIGHT, EPD_WIDTH)
    black_buf = bytearray(buf_size)
    red_buf = bytearray(buf_size)

    fb_b_rot = framebuf.FrameBuffer(
        black_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)
    fb_r_rot = framebuf.FrameBuffer(
        red_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)

    fb_b_rot.fill(1)
    fb_r_rot.fill(1)

    _view_price_data_impl(price_data, fb_b_rot, fb_r_rot)
    _display_rotated(epd, fb_b_rot, fb_r_rot)
