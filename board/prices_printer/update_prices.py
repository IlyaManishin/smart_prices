from e_paper import epdif
import framebuf

from e_paper import epd2in13b
from e_paper.config import EPD_HEIGHT, EPD_WIDTH
import fr_buf_helper as buf_helper

COLORED = 1
UNCOLORED = 0


class PricesData:
    name: str

    base_price: int
    sale_price: int
    discount: int

    def __init__(self, base_price, sale_price=None, discount=None):
        self.base_price = base_price
        self.sale_price = sale_price
        self.discount = discount


def display_rotated(epd, fb_black_rot, fb_red_rot, x_size, y_size):
    epd.display(buf_helper.frame_buf_rot90(fb_black_rot, x_size, y_size),
                buf_helper.frame_buf_rot90(fb_red_rot, x_size, y_size))


def main():
    epd = epd2in13b.EPD(epdif.spi, epdif.cs, epdif.dc, epdif.rst, epdif.busy)
    epd.init()
    buf_size = (EPD_WIDTH + 7) // 8 * EPD_HEIGHT
    black_buf = bytearray(buf_size)
    red_buf = bytearray(buf_size)

    fb_black_rot = framebuf.FrameBuffer(
        black_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)
    fb_red_rot = framebuf.FrameBuffer(
        red_buf, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_HLSB)

    fb_black_rot.fill(1)  
    fb_red_rot.fill(1)


    buf_helper.draw_text_scaled(fb_red_rot, "2 000", 20, 20, 0, 3)
    display_rotated(epd, fb_black_rot, fb_red_rot, EPD_HEIGHT, EPD_WIDTH)

    


if __name__ == '__main__':
    main()
