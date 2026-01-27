import framebuf
from e_paper.config import EPD_HEIGHT, EPD_WIDTH


def draw_text_scaled(fb, text, x, y, color, scale):
    glyph_buf = bytearray(8)
    ch_temp = framebuf.FrameBuffer(glyph_buf, 8, 8, framebuf.MONO_HLSB)

    cx = x
    for ch in text:
        ch_temp.fill(0)
        ch_temp.text(ch, 0, 0, 1)

        for py in range(8):
            for px in range(8):
                if ch_temp.pixel(px, py):
                    fb.fill_rect(
                        cx + px * scale,
                        y + py * scale,
                        scale,
                        scale,
                        color
                    )
        cx += 8 * scale

def draw_board(fb, w, h, depth):
    fb.fill_rect(0, 0, w, depth, 0)
    fb.fill_rect(0, h - depth, w, depth, 0)
    fb.fill_rect(0, 0, depth, h, 0)
    fb.fill_rect(w - depth, 0, depth, h, 0)

def frame_buf_rot90(src, w, h) -> bytearray:
    buf = bytearray((h + 7) // 8 * w)
    dst_fb = framebuf.FrameBuffer(buf, h, w, framebuf.MONO_HLSB)
    dst_fb.fill(1)

    for px in range(w):
        for py in range(h):
            dst_fb.pixel(h - py - 1, px, src.pixel(px, py))

    return buf

