from machine import Pin, SPI
import time

RST_PIN  = 26
DC_PIN   = 4
CS_PIN   = 22
BUSY_PIN = 25

rst = Pin(RST_PIN, Pin.OUT)
dc  = Pin(DC_PIN, Pin.OUT)
cs  = Pin(CS_PIN, Pin.OUT)
busy = Pin(BUSY_PIN, Pin.IN)

spi = SPI(2, baudrate=2_000_000, sck=Pin(18), mosi=Pin(23))


def epd_digital_write(pin, value):
    pin.value(value)

def epd_digital_read(pin):
    return pin.value()

def epd_delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def spi_transfer(data):
    spi.write(bytearray(data))

def epd_init():
    rst.value(0)
    epd_delay_ms(200)
    rst.value(1)
    epd_delay_ms(200)
    return 0

