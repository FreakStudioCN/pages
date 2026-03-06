import inspect
import os
import sys
import typing
import importlib.util
from typing import Dict, List, Any, Optional, Type
from jinja2 import Template

# ======================== 核心通用配置 ========================
FIXED_HELP_URL = "https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2"

TYPE_ANNOTATION_MAP = {
    int: "Number",
    float: "Number",
    str: "String",
    bool: "Boolean",
    tuple: "Array",
    typing.List: "Array",
    typing.Tuple: "Array",
    None: None
}
MACHINE_HW_TYPES = ["I2C", "Pin", "UART", "Timer", "ADC", "PWM", "SPI", "I2S", "CAN", "RTC"]

COMPLEX_TYPE_MAP = {
    "I2C": {
        "split_params": ["i2c_id", "scl_pin", "sda_pin"],
        "param_types": ["Number", "pinout", "pinout"],
        "friendly_names": ["I2C Bus ID", "SCL Pin", "SDA Pin"],
        "defaults": [0, 5, 4]
    },
    "UART": {
        "split_params": ["uart_port", "tx_pin", "rx_pin", "baudrate"],
        "param_types": ["Number", "pinout", "pinout", "Number"],
        "friendly_names": ["UART Port", "TX Pin", "RX Pin", "Baudrate"],
        "defaults": [0, 0, 1, 9600]
    },
    "ADC": {
        "split_params": ["adc_pin"],
        "param_types": ["pinout"],
        "friendly_names": ["ADC Pin"],
        "defaults": [26]
    },
    "Pin": {
        "split_params": ["digital_pin", "trigger_mode"],
        "param_types": ["pinout", "Dropdown"],
        "friendly_names": ["Digital Pin", "Interrupt Trigger"],
        "defaults": [16, 3],
        "dropdown_options": [
            ["Pin.IRQ_FALLING | Pin.IRQ_RISING", 3],
            ["Pin.IRQ_RISING", 1],
            ["Pin.IRQ_FALLING", 2]
        ]
    }
}

BLOCK_CONFIG = {
    "init_block_color": 230,
    "func_block_color": 230,
    "icon_size": [300, 300],
    "icon_base_path": "media/"
}

# ======================== 修复后的Jinja2模板（统一2空格缩进） ========================
BLOCK_TEMPLATE = """
// 自动生成的{{ class_info.class_name_original }}积木定义
// PY文件路径：{{ py_file_path }}
// 原始类：{{ class_info.module_name }}.{{ class_info.class_name_original }}

// 1. 初始化积木
Blockly.Blocks['{{ class_info.class_name_lower }}_init'] = {
  init: function() {
    // 基础输入（图标+标题）
    this.appendDummyInput()
        .appendField("{{ class_info.class_name_original }} Init")
        .appendField(new Blockly.FieldImage(
          "{{ BLOCK_CONFIG.icon_base_path }}{{ file_name }}.png", 
          {{ BLOCK_CONFIG.icon_size[0] }}, {{ BLOCK_CONFIG.icon_size[1] }}, 
          "*" 
        ));

    // 初始化参数
    {% for param in class_info.init_params %}
    this.appendValueInput("{{ param.name }}")
      .setCheck("{{ param.blockly_type }}")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("{{ param.friendly_name }}")
      {% if param.default_value is not none and param.default_value != 0 %}
      .appendField(new Blockly.FieldNumber({{ param.default_value }}), "{{ param.name | upper }}");
      {% else %};
      {% endif %}
    {% endfor %}

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour({{ BLOCK_CONFIG.init_block_color }});
    this.setTooltip("{{ class_info.init_doc | replace('\\n', ' ') }}");
    this.setHelpUrl("{{ FIXED_HELP_URL }}");
  }
};

// 2. 功能方法积木
{% for method in class_info.methods %}
{% if method.has_return %}
// 输出型积木（有返回值）
Blockly.Blocks['{{ class_info.class_name_lower }}_{{ method.name }}'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("{{ class_info.class_name_original }} {{ method.name }}");
    {% for param in method.params %}
    this.appendValueInput("{{ param.name }}")
      .setCheck("{{ param.blockly_type }}")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("{{ param.name }}");
    {% endfor %}
    this.setOutput(true, "{{ method.return_blockly_type }}");
    this.setColour({{ BLOCK_CONFIG.func_block_color }});
    this.setTooltip("{{ method.doc | replace('\\n', ' ') }}");
    this.setHelpUrl("{{ FIXED_HELP_URL }}");
  }
};
{% else %}
// 执行型积木（无返回值）
Blockly.Blocks['{{ class_info.class_name_lower }}_{{ method.name }}'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("{{ class_info.class_name_original }} {{ method.name }}");
    {% for param in method.params %}
    this.appendValueInput("{{ param.name }}")
      .setCheck("{{ param.blockly_type }}")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("{{ param.name }}");
    {% endfor %}
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour({{ BLOCK_CONFIG.func_block_color }});
    this.setTooltip("{{ method.doc | replace('\\n', ' ') }}");
    this.setHelpUrl("{{ FIXED_HELP_URL }}");
  }
};
{% endif %}
{% endfor %}
"""


# ======================== 工具函数（修复默认值+缩进） ========================
def get_type_basename(annotation: Any) -> str:
    if annotation is None or annotation == inspect.Parameter.empty:
        return ""
    if hasattr(annotation, "__origin__"):
        return annotation.__origin__.__name__
    if hasattr(annotation, "__qualname__"):
        return annotation.__qualname__.split(".")[-1]
    try:
        if isinstance(annotation, str):
            return annotation.split(".")[-1]
        return annotation.__name__
    except:
        return ""


def get_blockly_type_from_annotation(annotation: Any) -> Optional[str]:
    if annotation is None or annotation == inspect.Parameter.empty:
        return None
    type_basename = get_type_basename(annotation).strip()
    if type_basename in TYPE_ANNOTATION_MAP:
        return TYPE_ANNOTATION_MAP[type_basename]
    for py_type, blockly_type in TYPE_ANNOTATION_MAP.items():
        if hasattr(py_type, "__name__") and py_type.__name__ == type_basename:
            return blockly_type
    if type_basename in MACHINE_HW_TYPES:
        return "Number"
    if isinstance(annotation, str):
        if type_basename in ["int", "float"]:
            return "Number"
        elif type_basename == "str":
            return "String"
        elif type_basename == "bool":
            return "Boolean"
        elif type_basename == "tuple":
            return "Array"
    return None


def extract_class_info(cls: Any) -> Dict[str, Any]:
    class_info = {
        "class_name_original": cls.__name__,
        "class_name_lower": cls.__name__.lower(),
        "module_name": cls.__module__,
        "init_params": [],
        "methods": [],
        "init_doc": inspect.getdoc(cls.__init__) or "",
    }

    init_sig = inspect.signature(cls.__init__)
    for param_name, param in init_sig.parameters.items():
        if param_name == "self":
            continue

        param_anno = param.annotation
        blockly_type = get_blockly_type_from_annotation(param_anno)

        complex_type = None
        type_basename = get_type_basename(param_anno)
        for ct in COMPLEX_TYPE_MAP.keys():
            if type_basename == ct or (ct.lower() in param_name and "id" in param_name):
                complex_type = ct
                break

        if complex_type:
            split_config = COMPLEX_TYPE_MAP[complex_type]
            for i, sp in enumerate(split_config["split_params"]):
                split_blockly_type = split_config["param_types"][i]
                if split_blockly_type not in ["Number", "String", "Boolean"]:
                    split_blockly_type = None

                # 修复默认值：None替换为0，DS1307 addr默认0x68
                default_val = split_config["defaults"][i] if "defaults" in split_config else 0
                if sp == "addr":
                    default_val = 0x68 if default_val is None else default_val

                split_param = {
                    "name": sp,
                    "param_type": split_config["param_types"][i],
                    "blockly_type": split_blockly_type or blockly_type,
                    "friendly_name": split_config["friendly_names"][i],
                    "default_value": default_val,
                    "dropdown_options": split_config.get("dropdown_options", [])
                }
                class_info["init_params"].append(split_param)
        else:
            # 修复默认值：None→0，addr→0x68
            default_val = param.default if param.default != inspect.Parameter.empty else 0
            if param_name == "addr" and default_val is None:
                default_val = 0x68

            class_info["init_params"].append({
                "name": param_name,
                "param_type": blockly_type or "Number",
                "blockly_type": blockly_type,
                "friendly_name": param_name.replace("_", " ").title(),
                "default_value": default_val,
                "dropdown_options": []
            })

    for name, obj in inspect.getmembers(cls):
        if name.startswith("_") or name == "__init__":
            continue

        if isinstance(obj, property):
            getter = obj.fget
            if getter is not None:
                getter_sig = inspect.signature(getter)
                return_anno = getter_sig.return_annotation
                return_blockly_type = get_blockly_type_from_annotation(return_anno) or None

                method_info = {
                    "name": name,
                    "params": [],
                    "has_return": return_anno != inspect.Parameter.empty and return_anno != type(None),
                    "return_type": get_type_basename(return_anno) or "Any",
                    "return_blockly_type": return_blockly_type,
                    "doc": inspect.getdoc(getter) or f"Get {name} from {cls.__name__}"
                }
                class_info["methods"].append(method_info)

            setter = obj.fset
            if setter is not None:
                setter_sig = inspect.signature(setter)
                setter_params = []
                for p_name, p in setter_sig.parameters.items():
                    if p_name == "self":
                        continue
                    p_blockly_type = get_blockly_type_from_annotation(p.annotation) or "Number"
                    setter_params.append({
                        "name": p_name,
                        "type": get_type_basename(p.annotation) or "Any",
                        "blockly_type": p_blockly_type
                    })

                setter_info = {
                    "name": f"set_{name}",
                    "params": setter_params,
                    "has_return": False,
                    "return_type": "None",
                    "return_blockly_type": None,
                    "doc": inspect.getdoc(setter) or f"Set {name} for {cls.__name__}"
                }
                class_info["methods"].append(setter_info)

        elif inspect.isfunction(obj):
            method_sig = inspect.signature(obj)
            return_anno = method_sig.return_annotation
            return_blockly_type = get_blockly_type_from_annotation(return_anno) or None

            method_info = {
                "name": name,
                "params": [],
                "has_return": return_anno != inspect.Parameter.empty and return_anno != type(None),
                "return_type": get_type_basename(return_anno) or "Any",
                "return_blockly_type": return_blockly_type,
                "doc": inspect.getdoc(obj) or ""
            }

            for param_name, param in method_sig.parameters.items():
                if param_name == "self":
                    continue

                param_anno = param.annotation
                blockly_type = get_blockly_type_from_annotation(param_anno)

                method_info["params"].append({
                    "name": param_name,
                    "type": get_type_basename(param_anno) or "Any",
                    "blockly_type": blockly_type or "Number"
                })

            class_info["methods"].append(method_info)

    return class_info


def generate_block_js(cls: Any, py_file_path: str, output_path: str = None) -> None:
    file_basename = os.path.basename(py_file_path)
    file_name = os.path.splitext(file_basename)[0]

    if output_path is None:
        py_dir = os.path.dirname(py_file_path)
        output_path = os.path.join(py_dir, f"{file_name}_blocks.js")

    class_info = extract_class_info(cls)

    template = Template(BLOCK_TEMPLATE)
    js_code = template.render(
        class_info=class_info,
        BLOCK_CONFIG=BLOCK_CONFIG,
        FIXED_HELP_URL=FIXED_HELP_URL,
        py_file_path=py_file_path,
        file_name=file_name,
        enumerate=enumerate
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_code)

    print("=" * 50)
    print("✅ 转换成功！")
    print(f"📄 源PY文件：{py_file_path}")
    print(f"📄 生成JS文件：{output_path}")
    print(f"🖼️  图片路径：{BLOCK_CONFIG['icon_base_path']}{file_name}.png")
    print(f"🔗 HelpUrl：{FIXED_HELP_URL}")
    print(f"🧱 生成积木数：{len(class_info['methods']) + 1}")
    print("=" * 50)


def load_class_from_file(file_path: str) -> Type:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")

    # 模拟MicroPython模块
    if "micropython" not in sys.modules:
        mock_micropython = type("micropython", (object,), {"const": lambda x: x})
        sys.modules["micropython"] = mock_micropython

    if "machine" not in sys.modules:
        mock_I2C = type("I2C", (object,), {})
        mock_Pin = type("Pin", (object,), {})
        mock_UART = type("UART", (object,), {})
        mock_Timer = type("Timer", (object,), {})
        mock_ADC = type("ADC", (object,), {})
        mock_machine = type("machine", (object,), {
            "I2C": mock_I2C,
            "Pin": mock_Pin,
            "UART": mock_UART,
            "Timer": mock_Timer,
            "ADC": mock_ADC
        })
        sys.modules["machine"] = mock_machine

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        if "No module named" not in str(e):
            raise

    classes = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if (not name.startswith("_") and
                obj.__module__ == module_name and
                not name in ["typing", "Type", "List", "Tuple"]):
            classes.append(obj)

    if not classes:
        raise ValueError(f"文件{file_path}中未找到可转换的类")

    return classes[0]


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("=" * 50)
        print("Python硬件类 → Blockly积木定义转换工具（通用版）")
        print("=" * 50)
        print("使用方法：")
        print(f"  python {sys.argv[0]} <PY文件路径> [输出JS文件路径]")
        print("示例：")
        print(f"  python {sys.argv[0]} G:\\BIPES\\ui\\pylibs\\xxx.py")
        print(f"  python {sys.argv[0]} G:\\BIPES\\ui\\pylibs\\xxx.py G:\\output\\xxx_blocks.js")
        print("=" * 50)
        return

    py_file_path = os.path.abspath(sys.argv[1])
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        cls = load_class_from_file(py_file_path)
        generate_block_js(cls, py_file_path, output_path)
    except Exception as e:
        print(f"❌ 转换失败：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()