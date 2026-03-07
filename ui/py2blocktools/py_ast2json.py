# -*- coding: utf-8 -*-
import ast
import sys
import json
from pathlib import Path

# 通用类型映射规则（核心：tuple/list/array→Array，仅基于注解）
TYPE_MAPPING = {
    "tuple": "Array",
    "list": "Array",
    "array": "Array",
    "dict": "Array",  # MODIFY 1: 新增dict映射为Array，兼容BIPES
    "int": "Number",
    "float": "Number",
    "bool": "Boolean",
    "str": "String",
    "NoneType": "None",
    # 移除硬编码的 "int | None": "Number"，改为通用逻辑处理
    # 新增：补充Union/Optional基础映射（实际解析靠get_type_annotation）
    "Union": "Any",
    "Optional": "Any"
}

# 外设拆分规则（核心：移除所有中文，仅保留英文语义）
PERIPHERAL_RULES = {
    "I2C": {
        "keywords": ["i2c", "i2c_bus"],
        "params": ["I2C_BUS", "SDA_PIN", "SCL_PIN", "BAUDRATE"],
        "init_template": "{peri_lower} = {peri_type}({I2C_BUS}, scl=Pin({SCL_PIN}), sda=Pin({SDA_PIN}), freq={BAUDRATE})",
        "label_map": {  # 英文语义备注
            "I2C_BUS": "i2c_bus (I2C bus number)",
            "SDA_PIN": "sda_pin (SDA pin)",
            "SCL_PIN": "scl_pin (SCL pin)",
            "BAUDRATE": "baudrate (Baud rate)"
        }
    },
    "SoftI2C": {
        "keywords": ["i2c", "i2c_bus"],
        "params": ["SDA_PIN", "SCL_PIN", "BAUDRATE"],
        "init_template": "{peri_lower} = {peri_type}(scl=Pin({SCL_PIN}), sda=Pin({SDA_PIN}), freq={BAUDRATE})",
        "label_map": {
            "SDA_PIN": "sda_pin (SDA pin)",
            "SCL_PIN": "scl_pin (SCL pin)",
            "BAUDRATE": "baudrate (Baud rate)"
        }
    },
    "UART": {
        "keywords": ["uart", "uart_bus"],
        "params": ["UART_BUS", "TX_PIN", "RX_PIN", "BAUDRATE"],
        "init_template": "{peri_lower} = {peri_type}({UART_BUS}, tx=Pin({TX_PIN}), rx=Pin({RX_PIN}), baudrate={BAUDRATE})",
        "label_map": {
            "UART_BUS": "uart_bus (UART bus number)",
            "TX_PIN": "tx_pin (TX pin)",
            "RX_PIN": "rx_pin (RX pin)",
            "BAUDRATE": "baudrate (Baud rate)"
        }
    },
    "SPI": {
        "keywords": ["spi", "spi_bus"],
        "params": ["SPI_BUS", "CLK_PIN", "MOSI_PIN", "MISO_PIN", "BAUDRATE"],
        "init_template": "{peri_lower} = {peri_type}({SPI_BUS}, sck=Pin({CLK_PIN}), mosi=Pin({MOSI_PIN}), miso=Pin({MISO_PIN}), baudrate={BAUDRATE})",
        "label_map": {
            "SPI_BUS": "spi_bus (SPI bus number)",
            "CLK_PIN": "clk_pin (CLK pin)",
            "MOSI_PIN": "mosi_pin (MOSI pin)",
            "MISO_PIN": "miso_pin (MISO pin)",
            "BAUDRATE": "baudrate (Baud rate)"
        }
    },
    "ADC": {  # 简化为单参数，英文语义
        "keywords": ["adc"],
        "params": ["ADC_PIN"],
        "init_template": "{peri_lower} = {peri_type}(Pin({ADC_PIN}))",
        "label_map": {
            "ADC_PIN": "adc_pin (ADC input pin)"
        }
    },
    "Pin": {  # 动态保留原参数名，英文语义
        "keywords": ["pin"],
        "params": ["PIN"],
        # MODIFY 2: 可选参数处理 - 无值时返回None，添加Pin.OUT（硬件必需）
        "init_template": "{peri_lower} = {peri_type}({PIN}, Pin.OUT) if {PIN} is not None else None",
        "label_map": {
            "PIN": "{orig_param} ({semantic_note})"
        }
    }
}

# Field类型映射
FIELD_MAPPING = {
    "Number": "numeric",
    "Boolean": "checkbox",
    "String": "text_input",
    "Array": "dummy",
    "Any": "dummy",
    "Pin": "pinout"
}

# 地址类/引脚参数关键词
ADDR_KEYWORDS = ["addr", "address", "dev_addr", "device_addr", "addr7"]
PIN_KEYWORDS = ["pin", "pin1", "pin2", "sda", "scl", "tx", "rx", "clk"]

# 核心：Pin参数英文语义映射（移除所有中文）
PIN_SEMANTIC_MAP = {
    "gain_pin": "gain control pin, optional",
    "shdn_pin": "shutdown pin, optional",
    "adc_pin": "ADC input pin",
    "sda_pin": "I2C SDA pin",
    "scl_pin": "I2C SCL pin",
    "tx_pin": "UART TX pin",
    "rx_pin": "UART RX pin"
}


def analyze_dependencies(tree):
    """Analyze dependencies, convert to 'module.class' format"""
    dependencies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if module and alias.name:
                    dependencies.append(f"{module}.{alias.name}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.append(alias.name)
    return list(set(dependencies))


def get_type_annotation(node):
    """Extract type annotation and map to generic type
    核心优化：通用处理任意类型的 T | None（如 str | None → String，bool | None → Boolean）
    """
    if not node:
        return "Any"
    try:
        # 第一步：处理Optional/Union类型（如Optional[int]/Union[int, None]/str | None）
        # 1.1 处理Subscript类型（Optional[T]/Union[T, None]）
        if isinstance(node, ast.Subscript):
            # 提取基础类型（如Optional[int] → int，Union[str, None] → str）
            base_type = ast.unparse(node.value).strip()
            if base_type in ["Optional", "Union"]:
                # 遍历下标参数，排除NoneType，取核心类型
                for item in node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]:
                    item_str = ast.unparse(item).strip()
                    if item_str not in ["None", "NoneType"]:
                        return TYPE_MAPPING.get(item_str, item_str)
                return "Any"  # 仅None的情况

        # 1.2 处理 "|" 分隔的联合类型（如 int | None / str | None / bool | None）
        anno_str = ast.unparse(node).strip()
        if "|" in anno_str:
            # 拆分类型并过滤None，取核心类型
            type_parts = [part.strip() for part in anno_str.split("|") if part.strip() not in ["None", "NoneType"]]
            if len(type_parts) > 0:
                # 取第一个非None的类型（如 int | None → int，str | None → str）
                core_type = type_parts[0]
                return TYPE_MAPPING.get(core_type, core_type)
            return "Any"

        # 第二步：处理普通类型注解（无|/Optional/Union）
        core_type = anno_str.split("[")[0].replace("Optional[", "").replace("Literal[", "").replace("]", "")
        if "." in core_type:
            core_type = core_type.split(".")[-1]
        return TYPE_MAPPING.get(core_type, core_type)
    except Exception:
        return "Any"


def should_skip_method(method_node):
    """Determine if method should be skipped (keep __init__, skip callable/callback)"""
    if method_node.name == "__init__":
        return False
    for arg in method_node.args.args:
        if arg.arg == "self":
            continue
        if "callback" in arg.arg.lower() or get_type_annotation(arg.annotation).lower() == "callable":
            return True
    ret_type = get_type_annotation(method_node.returns)
    if ret_type.lower() == "callable":
        return True
    return False


def extract_class_constants(class_node):
    """Extract constants from single class"""
    constants = {}
    for item in class_node.body:
        if isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name) and isinstance(item.value, ast.Constant):
                    constants[target.id] = item.value.value
                elif isinstance(target, ast.Name) and isinstance(item.value, ast.Call):
                    if item.value.func.id == "const" and len(item.value.args) == 1:
                        const_arg = item.value.args[0]
                        if isinstance(const_arg, ast.Constant):
                            constants[target.id] = const_arg.value
        elif isinstance(item, ast.AnnAssign) and isinstance(item.value, ast.Constant):
            if isinstance(item.target, ast.Name):
                constants[item.target.id] = item.value.value
    return constants


def extract_all_class_constants(tree):
    """Extract all class constants, build global map"""
    all_constants = {}
    class_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    for cls_node in class_nodes:
        cls_name = cls_node.name
        all_constants[cls_name] = extract_class_constants(cls_node)
    return all_constants


def extract_param_default(param_node, class_constants=None, all_class_constants=None):
    """Extract parameter default value (support cross-class constant reference)"""
    if param_node is None:
        return None
    class_constants = class_constants or {}
    all_class_constants = all_class_constants or {}

    try:
        if isinstance(param_node, ast.Name):
            const_name = param_node.id
            if const_name in class_constants:
                return class_constants[const_name]
            for cls_const in all_class_constants.values():
                if const_name in cls_const:
                    return cls_const[const_name]
        elif isinstance(param_node, ast.Attribute):
            if isinstance(param_node.value, ast.Name):
                cls_name = param_node.value.id
                const_attr = param_node.attr
                if cls_name in all_class_constants and const_attr in all_class_constants[cls_name]:
                    return all_class_constants[cls_name][const_attr]
        default_str = ast.unparse(param_node).strip()
        if default_str.startswith("0x"):
            return int(default_str, 16)
        elif default_str == "True":
            return True
        elif default_str == "False":
            return False
        elif default_str == "None":
            return None
        try:
            return int(default_str)
        except ValueError:
            try:
                return float(default_str)
            except ValueError:
                return default_str.strip("'\"") if default_str.startswith(("'", '"')) else default_str
    except Exception:
        return None


def extract_param_min_max(method_node, param_name):
    """Extract param min/max (support >/<, fix samples>0 issue)"""
    min_val = None
    max_val = None
    # MODIFY 3: 修复samples>0的逻辑识别
    has_less_eq_zero = False
    for node in ast.walk(method_node):
        if not isinstance(node, ast.If):
            continue
        for cmp in ast.walk(node.test):
            if not isinstance(cmp, ast.Compare) or not (isinstance(cmp.left, ast.Name) and cmp.left.id == param_name):
                continue
            for op, val in zip(cmp.ops, cmp.comparators):
                if isinstance(val, ast.Constant) and isinstance(val.value, int):
                    num_val = val.value
                    # 识别 samples <=0 的判断，强制设置min=1
                    if (isinstance(op, ast.LtE) and num_val == 0) or (isinstance(op, ast.Lt) and num_val == 1):
                        has_less_eq_zero = True
                        min_val = 1
                        max_val = None
                    elif isinstance(op, ast.Gt):
                        min_val = num_val + 1
                    elif isinstance(op, ast.GtE):
                        min_val = num_val
                    elif isinstance(op, ast.Lt):
                        max_val = num_val - 1
                    elif isinstance(op, ast.LtE):
                        max_val = num_val
    # 兜底：确保samples参数min=1
    if param_name.lower() == "samples" and min_val is None:
        min_val = 1
        max_val = None
    return min_val, max_val


def identify_peripheral_type(param_name, param_type):
    """Identify peripheral type (priority: type annotation > param name)"""
    for peri_type in PERIPHERAL_RULES.keys():
        if param_type == peri_type:
            return peri_type
    for peri_type, rule in PERIPHERAL_RULES.items():
        if any(kw in param_name.lower() for kw in rule["keywords"]) and param_type == "Any":
            return peri_type
    return None


def build_peripheral_inputs(peri_type, param_name, orig_param_name):
    """Build peripheral inputs with semantic preservation (English only)"""
    inputs = []
    if peri_type not in PERIPHERAL_RULES:
        return inputs
    rule = PERIPHERAL_RULES[peri_type]

    for p_param in rule["params"]:
        if peri_type == "Pin":
            new_param_name = orig_param_name.upper()
            semantic_note = PIN_SEMANTIC_MAP.get(orig_param_name, "pin")
            label = rule["label_map"]["PIN"].format(
                orig_param=orig_param_name,
                semantic_note=semantic_note
            )
            # MODIFY 4: 给可选参数添加optional标记（JS层识别）
            is_optional = "optional" in semantic_note
        elif peri_type == "ADC":
            new_param_name = p_param
            label = rule["label_map"][p_param]
            is_optional = False
        else:
            new_param_name = p_param
            label = rule["label_map"].get(p_param, p_param.lower())
            is_optional = False

        field_type = FIELD_MAPPING["Pin"] if "PIN" in new_param_name else FIELD_MAPPING["Number"]

        input_obj = {
            "name": new_param_name,
            "input_type": "value",
            "check_type": "Number",
            "field": {
                "field_type": field_type,
                "default": None,
                "min": None,
                "max": None,
                "label": label
            }
        }
        # 添加optional标记
        if is_optional:
            input_obj["field"]["optional"] = True
        inputs.append(input_obj)
    return inputs


def build_block_inputs(method_node, class_constants=None, all_class_constants=None):
    """Build block inputs (preserve semantic, English only)
    核心优化：通用可选参数识别（有默认值→标记optional: true）
    """
    inputs = []
    class_constants = class_constants or {}
    all_class_constants = all_class_constants or {}

    args_count = len(method_node.args.args)
    defaults_count = len(method_node.args.defaults)
    default_start_idx = args_count - defaults_count if defaults_count > 0 else args_count

    for arg_idx, arg in enumerate(method_node.args.args):
        arg_name = arg.arg
        if arg_name == "self":
            continue

        if "callback" in arg_name.lower() or get_type_annotation(arg.annotation).lower() == "callable":
            continue

        arg_type = get_type_annotation(arg.annotation)
        peri_type = identify_peripheral_type(arg_name, arg_type)

        if peri_type:
            peri_inputs = build_peripheral_inputs(peri_type, arg_name, arg_name)
            inputs.extend(peri_inputs)
            continue

        default_val = None
        if arg_idx >= default_start_idx and defaults_count > 0:
            default_idx_in_list = arg_idx - default_start_idx
            if 0 <= default_idx_in_list < defaults_count:
                default_val = extract_param_default(
                    method_node.args.defaults[default_idx_in_list],
                    class_constants,
                    all_class_constants
                )

        min_val, max_val = extract_param_min_max(method_node, arg_name)

        field_type = FIELD_MAPPING.get(arg_type, "dummy")
        if any(kw in arg_name.lower() for kw in ADDR_KEYWORDS):
            field_type = "dummy"
        elif arg_type == "Number" and any(kw in arg_name.lower() for kw in PIN_KEYWORDS):
            field_type = "pinout"

        # 构造input基础对象
        input_obj = {
            "name": arg_name.upper(),
            "input_type": "value",
            "check_type": "Any" if any(kw in arg_name.lower() for kw in ADDR_KEYWORDS) else arg_type,
            "field": {
                "field_type": field_type,
                "default": default_val,
                "min": min_val,
                "max": max_val,
                "label": arg_name
            }
        }

        # 通用可选参数标记：有默认值/在默认值区间 → 标记optional: true
        if default_val is not None or arg_idx >= default_start_idx:
            input_obj["field"]["optional"] = True
            # 优化：可选参数标签补充备注
            input_obj["field"]["label"] = f"{arg_name} (optional)"

        inputs.append(input_obj)

    return inputs


def build_blocks(tree, class_node, all_class_constants=None):
    """Build blocks array (semantic preservation, English only)"""
    blocks = []
    cls_name = class_node.name
    cls_name_lower = cls_name.lower()
    class_constants = extract_class_constants(class_node)
    all_class_constants = all_class_constants or {}

    for item in class_node.body:
        if not isinstance(item, ast.FunctionDef) or (item.name.startswith("_") and item.name != "__init__"):
            continue
        if should_skip_method(item):
            continue

        func_name = item.name
        is_property = any(isinstance(d, ast.Name) and d.id == "property" for d in item.decorator_list)
        is_setter = any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in item.decorator_list)

        if func_name == "__init__":
            block_type = f"{cls_name_lower}_init"
            colour = 135
            output_type = cls_name
        elif is_property and not is_setter:
            block_type = f"{cls_name_lower}_property_{func_name}"
            colour = 230
            output_type = get_type_annotation(item.returns)
        elif is_setter:
            block_type = f"{cls_name_lower}_property_set_{func_name}"
            colour = 230
            output_type = False
        else:
            block_type = f"{cls_name_lower}_method_{func_name}"
            colour = 230
            ret_type = get_type_annotation(item.returns)
            # MODIFY 5: 确保output_type使用TYPE_MAPPING映射（兼容dict）
            output_type = TYPE_MAPPING.get(ret_type, ret_type) if ret_type not in ("Any", "None") else False

        inputs = build_block_inputs(item, class_constants, all_class_constants)

        message_parts = [f"{cls_name}", func_name]
        for idx, input_item in enumerate(inputs):
            label = input_item["field"]["label"]
            message_parts.append(f"{label}%{idx + 1}")
        message = " ".join(message_parts)

        if func_name == "__init__":
            peri_init_parts = []
            cls_init_params = []

            for arg_idx, arg in enumerate(item.args.args):
                arg_name = arg.arg
                if arg_name == "self":
                    continue
                if "callback" in arg_name.lower() or get_type_annotation(arg.annotation).lower() == "callable":
                    continue

                arg_type = get_type_annotation(arg.annotation)
                peri_type = identify_peripheral_type(arg_name, arg_type)

                if peri_type:
                    peri_lower = f"{arg_name}_inst"
                    rule = PERIPHERAL_RULES[peri_type]

                    if peri_type == "Pin":
                        template_params = {"PIN": f"{{{arg_name.upper()}}}"}
                    elif peri_type == "ADC":
                        template_params = {"ADC_PIN": "{ADC_PIN}"}
                    else:
                        template_params = {p: f"{{{p}}}" for p in rule["params"]}

                    template = rule["init_template"].format(
                        peri_lower=peri_lower,
                        peri_type=peri_type,
                        **template_params
                    )
                    peri_init_parts.append(template)
                    cls_init_params.append(peri_lower)
                else:
                    if any(kw in arg_name.lower() for kw in ADDR_KEYWORDS):
                        cls_init_params.append(f"{arg_name}={{{arg_name.upper()}}}")
                    else:
                        cls_init_params.append(f"{{{arg_name.upper()}}}")

            peri_init = "\n".join(peri_init_parts) if peri_init_parts else ""
            cls_init = f"{cls_name_lower} = {cls_name}({', '.join(cls_init_params)})"
            generator_template = f"{peri_init}\n{cls_init}" if peri_init else cls_init

        elif is_setter:
            param_placeholders = [f"{{{input_item['name']}}}" for input_item in inputs]
            generator_template = f"{cls_name_lower}.{func_name} = {', '.join(param_placeholders)}" if param_placeholders else f"{cls_name_lower}.{func_name}"

        elif is_property and not is_setter:
            generator_template = f"{cls_name_lower}.{func_name}"

        else:
            param_placeholders = [f"{{{input_item['name']}}}" for input_item in inputs]
            params_str = ", ".join(param_placeholders) if param_placeholders else ""
            generator_template = f"{cls_name_lower}.{func_name}({params_str})"

        if output_type is False:
            previous_statement = True
            next_statement = True
        else:
            previous_statement = False
            next_statement = False

        blocks.append({
            "type": block_type,
            "message": message,
            "colour": colour,
            "output_type": output_type,
            "previous_statement": previous_statement,
            "next_statement": next_statement,
            "inputs": inputs,
            "generator_template": generator_template,
            "is_property": is_property and not is_setter,
            "is_setter": is_setter
        })

    return blocks


def generate_generic_json(file_path):
    """Generate generic JSON structure (English only)"""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    module_name = Path(file_path).stem
    dependencies = analyze_dependencies(tree)
    class_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    all_class_constants = extract_all_class_constants(tree)

    json_data = {
        "meta": {
            "module_name": module_name,
            "class_name": class_nodes[0].name if class_nodes else "",
            "version": "1.0.0"
        },
        "dependencies": dependencies,
        "blocks": []
    }

    for cls_node in class_nodes:
        json_data["blocks"].extend(build_blocks(tree, cls_node, all_class_constants))

    return json.dumps(json_data, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) != 2:
        print("Usage: python py_ast2json.py target_file.py")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists() or file_path.suffix != ".py":
        print("Error: Only support existing .py files")
        sys.exit(1)

    json_result = generate_generic_json(file_path)
    print("Generated generic JSON structure:\n")
    print(json_result)

    with open(f"{file_path.stem}.json", "w", encoding="utf-8") as f:
        f.write(json_result)
    print(f"\nJSON file saved to: {file_path.stem}.json")


if __name__ == "__main__":
    main()