

import ustruct

import time

from machine import I2C


class PCA9685:

    def __init__(self, i2c: I2C, address: int = 0x40):

        if not 0x40 <= address <= 0x4F:
            raise ValueError(
                "Invalid address: %d (must be 0x40-0x4F)" % address)

        self.i2c = i2c
        self.address = address
        self.reset()

    def _write(self, address: int, value: int) -> None:
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address: int) -> int:
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self) -> None:

        self._write(0x00, 0x00)

    def freq(self, freq: float) -> None:

        prescale = int(25000000.0 / 4096.0 / freq + 0.5)

        old_mode = self._read(0x00)

        self._write(0x00, (old_mode & 0x7F) | 0x10)

        self._write(0xfe, prescale)

        self._write(0x00, old_mode)
        time.sleep_us(5)

        self._write(0x00, old_mode | 0xa1)

    def pwm(self, index: int, on: int, off: int) -> None:
        data = ustruct.pack('<HH', on, off)

        self.i2c.writeto_mem(self.address, 0x06 + 4 * index, data)

    def duty(self, index: int, value: int, invert: bool = False) -> int:
        if not 0 <= value <= 4095:
            raise ValueError("Invalid value: %d (must be 0-4095)" % value)

        if invert:
            value = 4095 - value

        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)

        return value
