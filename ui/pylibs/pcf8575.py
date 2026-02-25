

from machine import Pin, I2C


class PCF8575:

    def __init__(self, i2c: I2C, address: int = 0x20, interrupt_pin: Pin = None, callback: callable = None):

        self._i2c = i2c

        self._address = address

        self._port = bytearray(2)

        self.interrupt_pin = interrupt_pin
        self.callback = callback

        if self.interrupt_pin:
            self.interrupt_pin.init(Pin.IN, Pin.PULL_UP)
            self.interrupt_pin.irq(
                trigger=Pin.IRQ_FALLING, handler=self._interrupt_handler)

    def check(self) -> bool:

        if self._i2c.scan().count(self._address) == 0:

            raise OSError(
                f"PCF8575 not found at I2C address {self._address:#x}")
        return True

    @property
    def port(self) -> int:

        self._read()

        return self._port[0] | (self._port[1] << 8)

    @port.setter
    def port(self, value: int) -> None:

        self._port[0] = value & 0xFF

        self._port[1] = (value >> 8) & 0xFF

        self._write()

    def pin(self, pin: int, value: bool = None) -> int:

        pin = self._validate_pin(pin)

        if value is None:

            self._read()

            return (self._port[pin // 8] >> (pin % 8)) & 1

        if value:

            self._port[pin // 8] |= 1 << (pin % 8)
        else:

            self._port[pin // 8] &= ~(1 << (pin % 8))

        self._write()

    def toggle(self, pin: int) -> None:

        pin = self._validate_pin(pin)

        self._port[pin // 8] ^= 1 << (pin % 8)

        self._write()

    def _validate_pin(self, pin: int) -> int:

        if not 0 <= pin <= 7 and not 10 <= pin <= 17:

            raise ValueError(f"Invalid pin {pin}. Use 0-7 or 10-17.")

        if pin >= 10:
            pin -= 2

        return pin

    def _read(self) -> None:

        self._i2c.readfrom_into(self._address, self._port)

    def _write(self) -> None:

        self._i2c.writeto(self._address, self._port)

    def _interrupt_handler(self, pin: Pin) -> None:
        if self.callback:
            self.callback(pin)
