__version__ = "0.1.0"
__author__ = "李清水"
__license__ = "MIT"
__platform__ = "MicroPython v1.23"

# 导入硬件相关模块
from machine import Pin, Timer

class RelayController:
    RELAY_TYPES = {
        "normal": "Standard single-coil relay",
        "latching": "Bistable latching relay (requires H-bridge)",
    }

    def __init__(self, relay_type: str, pin1: int, pin2: int = None) -> None:
        if not isinstance(pin1, int) or (pin2 is not None and not isinstance(pin2, int)):
            raise TypeError("pin1 and pin2 must be integers")

        self.relay_type = relay_type.lower()

        # 验证继电器类型
        if self.relay_type not in self.RELAY_TYPES:
            raise ValueError(f"Invalid relay type. Must be one of: {list(self.RELAY_TYPES.keys())}")

        # 初始化控制引脚
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin1.value(0)

        # 创建虚拟定时器用于非阻塞脉冲
        self._pulse_timer = Timer(-1)

        # 磁保持继电器需要两个引脚
        if self.relay_type == "latching":
            if pin2 is None:
                raise ValueError("Latching relay requires both pin1 and pin2 for H-bridge control")
            self.pin2 = Pin(pin2, Pin.OUT)
            self.pin2.value(0)
            self.off()

        # 添加状态跟踪属性
        self._last_state = False

    def get_state(self) -> bool:
        if self.relay_type == "normal":
            return bool(self.pin1.value())
        else:
            return self._last_state

    def _reset_pins(self, timer: Timer = None) -> None:
        self.pin1.value(0)
        if hasattr(self, "pin2"):
            self.pin2.value(0)

    def on(self) -> None:
        if self.relay_type == "normal":
            # 普通继电器直接给高电平
            self.pin1.value(1)
        else:
            # 磁保持继电器需要短脉冲
            # 取消已有定时器
            self._pulse_timer.deinit()
            # 先设置方向
            self.pin2.value(0)
            # 开始正向脉冲
            self.pin1.value(1)
            # 设置50ms后自动复位（非阻塞）
            self._pulse_timer.init(mode=Timer.ONE_SHOT, period=50, callback=self._reset_pins)
        self._last_state = True

    def off(self) -> None:
        if self.relay_type == "normal":
            # 普通继电器直接给低电平
            self.pin1.value(0)
        else:
            # 磁保持需要反向脉冲
            self._pulse_timer.deinit()
            # 先设置方向
            self.pin1.value(0)
            # 开始反向脉冲
            self.pin2.value(1)
            self._pulse_timer.init(mode=Timer.ONE_SHOT, period=50, callback=self._reset_pins)
        self._last_state = False

    def toggle(self) -> None:
        if self.relay_type == "normal":
            # 普通继电器直接取反
            self.pin1.value(not self.pin1.value())
            self._last_state = bool(self.pin1.value())
        else:
            # 磁保持继电器根据记录状态切换脉冲
            if self._last_state:
                self.off()
            else:
                self.on()

    def deinit(self)-> None:
        self._pulse_timer.deinit()
        # 确保继电器处于安全状态
        self.off()