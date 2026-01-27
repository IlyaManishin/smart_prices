import epd2in13b
from epd2in13b import EPD_HEIGHT, EPD_WIDTH
import epdif
import framebuf

COLORED = 1
UNCOLORED = 0


def draw_text_scaled(fb, text, x, y, color, scale):
    glyph_buf = bytearray(8)
    glyph = framebuf.FrameBuffer(glyph_buf, 8, 8, framebuf.MONO_HLSB)

    cx = x
    for ch in text:
        glyph.fill(0)
        glyph.text(ch, 0, 0, 1)

        for py in range(8):
            for px in range(8):
                if glyph.pixel(px, py):
                    fb.fill_rect(
                        cx + px * scale,
                        y + py * scale,
                        scale,
                        scale,
                        color
                    )
        cx += 8 * scale
        
def main():
    epd = epd2in13b.EPD(epdif.spi, epdif.cs, epdif.dc, epdif.rst, epdif.busy)
    epd.init()
    buf_size = (EPD_WIDTH + 7) // 8 * EPD_HEIGHT
    black_buf = bytearray(buf_size)
    red_buf   = bytearray(buf_size)

    fb_black = framebuf.FrameBuffer(black_buf, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
    fb_red   = framebuf.FrameBuffer(red_buf,   EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)

    fb_black.fill(1)   # 1 = белый фон, 0 = чёрный
    fb_red.fill(1)

    # fb_red.text("2 000 000", 20, 20, 0)   
    draw_text_scaled(fb_red, "2 000", 20, 20, 0, 2)


    epd.display(black_buf, red_buf)
    
if __name__ == '__main__':
    main()

