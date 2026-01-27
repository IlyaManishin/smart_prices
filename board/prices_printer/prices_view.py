import framebuf

from .base_config import *
from .e_paper import epdif
from .e_paper.epd2in13b import EPD
from .e_paper.config import EPD_HEIGHT, EPD_WIDTH
from . import fb_helper


class PriceVal:
    rubs: int
    kopecks: int

    def __init__(self, rubs, kopecks):
        self.rubs = rubs % MAX_PRICE
        self.kopecks = kopecks % MAX_KOPECKS


class DiscountData:
    sale_price: PriceVal
    discount: int

    def __init__(self, sale_price: PriceVal, discount):
        self.sale_price = sale_price
        self.discount = discount % MAX_DISCOUNT


class PriceData:
    name: str
    base_price: PriceVal
    discount_data: DiscountData

    def __init__(self, name, base_price: PriceVal, discount_data: DiscountData = None):
        self.name = name
        self.base_price = base_price
        self.discount_data = discount_data


class ElemPos:
    x_st: int
    y_st: int
    x_end: int
    y_end: int

    def __init__(self, x_st, y_st, x_end, y_end):
        self.x_st = x_st
        self.y_st = y_st
        self.x_end = x_end
        self.y_end = y_end


MAX_TITLE_LINES = 2
TITLE_SCALES = [1.7, 1.5, 1]
TITLE_MAX_LINES = 2
TITLE_Y_OFF = 5

PRICES_BLK_X = 120
CROSS_DEPTH = 1
CROSSED_PRICE_OFF_Y = 6
CROSSED_PRICE_SCALE = 1.7

RES_PRICE_SCALES = [3, 2.5, 2]
RES_PRICE_OFF_Y_DOWN = 10


def _display_rotated(epd, fb_b_rot, fb_r_rot):
    epd.display(fb_helper.frame_buf_rot90(fb_b_rot, EPD_HEIGHT, EPD_WIDTH),
                fb_helper.frame_buf_rot90(fb_r_rot, EPD_HEIGHT, EPD_WIDTH))


def _title_to_lines(title: str, scale: float):
    max_text_width = EPD_HEIGHT - 2 * EDGE_X_OFF
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


def _view_title(fb_rot, title) -> ElemPos:
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
            fb_rot, line, EDGE_X_OFF, y_cur, 0, scale, EPD_HEIGHT)
        y_cur += ch_size_y + LINE_OFF

    border = 1
    fb_rot.fill_rect(EDGE_X_OFF, y_cur, EPD_HEIGHT - 2 * EDGE_X_OFF, border, 0)

    return ElemPos(0, 0, EPD_HEIGHT, y_cur + 1)


def _view_crossed_price(price_data: PriceVal, fb_rot, res_pr_pos: ElemPos) -> ElemPos:
    ch_w = int(round(CH_SZ_X * CROSSED_PRICE_SCALE))
    ch_h = int(round(CH_SZ_Y * CROSSED_PRICE_SCALE))

    x_st = res_pr_pos.x_st
    
    y_end = res_pr_pos.y_st - CROSSED_PRICE_OFF_Y
    y_st = y_end - ch_h
    
    x_cur = fb_helper.draw_text_scaled(
        fb_rot, str(price_data.rubs), x_st, y_st, 0, CROSSED_PRICE_SCALE, EPD_HEIGHT)
    x_end = fb_helper.draw_text_scaled(
        fb_rot, str(price_data.kopecks), x_cur, y_st, 0, 1, EPD_HEIGHT)
    
    y_line = y_st + int(ch_h // 2)
    fb_rot.fill_rect(x_st, y_line, x_end - x_st, CROSS_DEPTH, 0)

    return ElemPos(x_st, y_st, x_end, y_end)
    

def _view_base_price(price: PriceVal, fb_rot) -> ElemPos:
    base_price = price.rubs
    scale = RES_PRICE_SCALES[0]
    if len(str(base_price)) >= 7:
        scale = RES_PRICE_SCALES[2]
    elif len(str(base_price)) >= 5:
        scale = RES_PRICE_SCALES[1]

    rubs_str = str(price.rubs)
    kopecks_str = "." + str(price.kopecks)
    str_size = len(rubs_str) * CH_SZ_X * scale + len(kopecks_str) * CH_SZ_X

    x_end = EPD_HEIGHT - EDGE_X_OFF
    y_end = EPD_WIDTH - RES_PRICE_OFF_Y_DOWN
    x_st = int(x_end - str_size)
    y_st = int(y_end - CH_SZ_Y * scale)

    x_cur = fb_helper.draw_text_scaled(
        fb_rot, rubs_str, x_st, y_st, 0, scale, EPD_HEIGHT)
    fb_helper.draw_text_scaled(
        fb_rot, kopecks_str, x_cur, y_st, 0, 1, EPD_HEIGHT)

    return ElemPos(x_st, y_st, x_end, y_end)


def _view_price_data_impl(price_data: PriceData, fb_b_rot, fb_r_rot):
    title_pos = _view_title(fb_b_rot, price_data.name)

    base_pr_pos = _view_base_price(price_data.base_price, fb_b_rot)
    if price_data.discount_data:
        fb_helper.draw_border(fb_r_rot, EPD_HEIGHT, EPD_WIDTH, 2)
        _view_crossed_price(price_data.discount_data.sale_price, fb_r_rot, base_pr_pos)
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
