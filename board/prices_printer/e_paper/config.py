from machine import Pin, SPI


EPD_WIDTH = 122
EPD_HEIGHT = 250

RST_PIN = 26
DC_PIN = 4
CS_PIN = 22
BUSY_PIN = 25

rst = Pin(RST_PIN, Pin.OUT)
dc = Pin(DC_PIN, Pin.OUT)
cs = Pin(CS_PIN, Pin.OUT)
busy = Pin(BUSY_PIN, Pin.IN)

spi = SPI(2, baudrate=2_000_000, sck=Pin(18), mosi=Pin(23))
