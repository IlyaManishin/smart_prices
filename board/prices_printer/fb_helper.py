import framebuf

from .base_config import *


def get_bytearr_size(w, h):
    return (w + 7) // 8 * h


def draw_text_scaled(fb, text, x, y, color, scale, max_x):
    w = int(CH_SZ_X * scale)
    h = int(CH_SZ_Y * scale)
    glyph_buf = bytearray(get_bytearr_size(w, h))
    ch_temp = framebuf.FrameBuffer(glyph_buf, w, h, framebuf.MONO_HLSB)

    cx = x
    cy = y

    for ch in text:
        ch_temp.fill(0)
        ch_temp.text(ch, 0, 0, 1)

        for py in range(h):
            for px in range(w):
                if ch_temp.pixel(px, py):
                    px_scaled = int(round(px * scale))
                    py_scaled = int(round(py * scale))
                    size_scaled = max(1, int(round(scale)))

                    fb.fill_rect(
                        cx + px_scaled,
                        cy + py_scaled,
                        size_scaled,
                        size_scaled,
                        color
                    )
        cx += w
        if cx + w > max_x:
            break
    return cx, cy


def draw_border(fb, w, h, depth):
    fb.fill_rect(0, 0, w, depth, 0)
    fb.fill_rect(0, h - depth, w, depth, 0)
    fb.fill_rect(0, 0, depth, h, 0)
    fb.fill_rect(w - depth, 0, depth, h, 0)


def frame_buf_rot90(src, w, h) -> bytearray:
    buf = bytearray(get_bytearr_size(h, w))
    dst_fb = framebuf.FrameBuffer(buf, h, w, framebuf.MONO_HLSB)
    dst_fb.fill(1)

    for px in range(w):
        for py in range(h):
            dst_fb.pixel(h - py - 1, px, src.pixel(px, py))

    return buf


def write_logo(fb_b, fb_r, w, h):
    pass
