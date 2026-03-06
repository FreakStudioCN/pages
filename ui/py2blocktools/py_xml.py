# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2026/3/6 下午10:58   
# @Author  : 李清水            
# @File    : py_xml.py       
# @Description :

import re
import os
import argparse

# ===================== 通用配置（无模块类型耦合，适配多接口/多参数） =====================
# 固定库地址（用户要求的统一地址）
DEFAULT_LIB_URL = "https://github.com/FreakStudioCN/GraftSense-Drivers-MicroPython"
# 固定回调键（对齐BIPES示例）
DEFAULT_CALLBACK_KEY = "installPyLib"
# 2空格缩进（严格对齐BIPES示例格式）
XML_INDENT = "  "


# ===================== Grove接口通用默认规则（按特征匹配，支持多参数） =====================
def get_grove_default_value(param_name: str) -> int:
    """
    按参数名特征返回Grove接口默认值（通用适配多ADC/多PIN等场景）
    规则：
    - I2C类：i2c/i2c1/i2c2 → 0/1/2；sda/sda1/sda2 → 4/5/6；scl/scl1/scl2 →5/6/7；addr →104
    - UART类：uart/uart1/uart2 →0/1/2；tx/rx/tx1/rx1 →16/17/18/19；baudrate →9600
    - 模拟类：adc/adc1/adc2 →26/26/27；analog/analog1 →26/27
    - 数字类：pin/pin1/pin2 →0/1/2；digital/digital1 →0/1
    """
    param_lower = param_name.lower()

    # I2C接口规则（支持多I2C）
    if re.match(r"i2c(\d+)?", param_lower):
        num = re.findall(r"i2c(\d+)", param_lower)
        return int(num[0]) if num else 0
    elif re.match(r"sda(\d+)?", param_lower):
        num = re.findall(r"sda(\d+)", param_lower)
        return 4 + int(num[0]) if num else 4
    elif re.match(r"scl(\d+)?", param_lower):
        num = re.findall(r"scl(\d+)", param_lower)
        return 5 + int(num[0]) if num else 5
    elif "addr" in param_lower:
        return 104

    # UART接口规则（支持多UART）
    elif re.match(r"uart(\d+)?", param_lower) or re.match(r"uart_port(\d+)?", param_lower):
        num = re.findall(r"uart(\d+)", param_lower) or re.findall(r"uart_port(\d+)", param_lower)
        return int(num[0]) if num else 0
    elif re.match(r"tx(\d+)?", param_lower) or re.match(r"tx_pin(\d+)?", param_lower):
        num = re.findall(r"tx(\d+)", param_lower) or re.findall(r"tx_pin(\d+)", param_lower)
        return 16 + int(num[0]) if num else 16
    elif re.match(r"rx(\d+)?", param_lower) or re.match(r"rx_pin(\d+)?", param_lower):
        num = re.findall(r"rx(\d+)", param_lower) or re.findall(r"rx_pin(\d+)", param_lower)
        return 17 + int(num[0]) if num else 17
    elif "baudrate" in param_lower:
        return 9600

    # 模拟接口规则（支持多ADC，如PS2模块双ADC）
    elif re.match(r"adc(\d+)?", param_lower):
        num = re.findall(r"adc(\d+)", param_lower)
        return 26 + int(num[0]) if num and int(num[0]) > 0 else 26
    elif re.match(r"analog(\d+)?", param_lower):
        num = re.findall(r"analog(\d+)", param_lower)
        return 26 + int(num[0]) if num and int(num[0]) > 0 else 26

    # 数字接口规则（支持多PIN）
    elif re.match(r"pin(\d+)?", param_lower) or re.match(r"digital(\d+)?", param_lower):
        num = re.findall(r"pin(\d+)", param_lower) or re.findall(r"digital(\d+)", param_lower)
        return int(num[0]) if num else 0

    # 默认值
    else:
        return 0


def get_shadow_type_and_value(param_name: str, block_type: str = "", custom_defaults: dict = None) -> tuple:
    """
    按参数名+积木类型返回Shadow类型、Field名、默认值
    返回：(shadow_type, field_name, default_val)
    - 引脚类（pin/sda/scl/tx/rx）→ pinout + PIN + 对应默认值
    - 布尔型参数（如set_disable_oscillator的value）→ logic_boolean + BOOL + FALSE
    - 其他数字类 → math_number + NUM + 对应默认值
    """
    custom_defaults = custom_defaults or {}
    param_lower = param_name.lower()

    # 特殊处理布尔型参数
    if block_type.endswith("_set_disable_oscillator") and param_lower == "value":
        default_val = custom_defaults.get(param_name, "FALSE")
        return ("logic_boolean", "BOOL", default_val)
    # 引脚类参数
    elif any(key in param_lower for key in ["pin", "sda", "scl", "tx", "rx"]):
        default_val = custom_defaults.get(param_name, get_grove_default_value(param_name))
        return ("pinout", "PIN", default_val)
    # 普通数字类参数
    else:
        default_val = custom_defaults.get(param_name, get_grove_default_value(param_name))
        return ("math_number", "NUM", default_val)


# ===================== 工具函数：解析Blockly JS文件（纯结构化，精准匹配init内参数） =====================
def parse_blockly_js(js_path: str) -> dict:
    """
    解析Blockly JS文件，提取积木信息（仅结构化解析，无模块类型判断）
    核心优化：先提取每个积木的init函数块，再在块内精准匹配appendValueInput，避免跨积木误匹配
    返回格式：
    {
        "blocks": [
            {"type": "ps2_init", "params": ["adc1", "adc2", "pin1"]},
            {"type": "ps2_read", "params": []},
            ...
        ],
        "prefix": "ps2",  # 积木前缀（从第一个积木type推导）
        "filename_prefix": "ps2"  # 文件名前缀（如ps2_blocks.js → ps2）
    }
    """
    if not os.path.exists(js_path):
        raise FileNotFoundError(f"JS文件不存在：{js_path}")

    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # 1. 提取所有积木type
    block_pattern = re.compile(r"Blockly\.Blocks\['([a-zA-Z0-9_]+)'\]", re.DOTALL)
    block_types = block_pattern.findall(js_content)
    if not block_types:
        raise ValueError("JS文件中未找到Blockly积木定义（Blockly.Blocks）")

    # 2. 提取每个积木的参数（精准到当前积木的init函数内）
    blocks_info = []
    for block_type in block_types:
        # 先提取该积木的init函数完整内容（避免跨积木匹配）
        block_init_pattern = re.compile(
            rf"Blockly\.Blocks\['{block_type}'\]\s*=\s*\{{\s*init:\s*function\(\)\s*\{{(.*?)\}}\s*\}};",
            re.DOTALL | re.MULTILINE
        )
        init_match = block_init_pattern.search(js_content)

        if init_match:
            init_content = init_match.group(1)
            # 在init函数内精准匹配appendValueInput的参数名
            param_pattern = re.compile(r'appendValueInput\("([a-zA-Z0-9_]+)"\)')
            params = param_pattern.findall(init_content)
        else:
            params = []

        blocks_info.append({
            "type": block_type,
            "params": params
        })

    # 3. 推导积木前缀
    block_prefix = ""
    if blocks_info:
        first_block_type = blocks_info[0]["type"]
        prefix_match = re.match(r"^([a-zA-Z0-9]+)_", first_block_type)
        if prefix_match:
            block_prefix = prefix_match.group(1)

    # 4. 推导文件名前缀
    filename = os.path.basename(js_path)
    filename_prefix = re.sub(r"_blocks\.js$|\.js$", "", filename)

    return {
        "blocks": blocks_info,
        "prefix": block_prefix or filename_prefix,
        "filename_prefix": filename_prefix
    }


# ===================== 工具函数：生成BIPES XML（纯字符串拼接，100%控制格式） =====================
def generate_bipes_xml(
        js_parse_result: dict,
        category_name: str = None,
        block_desc: str = None,
        lib_name: str = None,
        custom_defaults: dict = None
) -> str:
    """
    生成BIPES标准XML（纯字符串拼接，彻底避免自闭合标签，精准控制格式）
    """
    custom_defaults = custom_defaults or {}
    prefix = js_parse_result["prefix"]

    # 推导基础配置
    category_name = category_name or prefix.upper()
    block_desc = block_desc or f"{prefix.upper()} Module"
    lib_name = lib_name or prefix.lower()

    # 初始化XML字符串（手动拼接，逐行控制）
    xml_lines = []
    xml_lines.append(f"<category name=\"{category_name}\">")

    # 1. 库地址Label（完整闭合）
    xml_lines.append(f"{XML_INDENT}<label text=\"Library: {DEFAULT_LIB_URL} \"></label>")

    # 2. Install按钮（完整闭合）
    xml_lines.append(
        f"{XML_INDENT}<button text=\"Install {lib_name} library\" callbackKey=\"{DEFAULT_CALLBACK_KEY}\"></button>")

    # 3. 空行（对齐官方示例）
    xml_lines.append("")

    # 4. 模块描述Label（完整闭合）
    xml_lines.append(f"{XML_INDENT}<label text=\"{block_desc}\"></label>")

    # 5. 遍历生成每个积木的block节点（核心修改：区分有/无参数block）
    for block in js_parse_result["blocks"]:
        block_type = block["type"]
        params = block["params"]

        # 无参数block：单行完整闭合
        if not params:
            xml_lines.append(f"{XML_INDENT}<block type=\"{block_type}\"></block>")
        # 有参数block：多行缩进
        else:
            # 开始block标签
            xml_lines.append(f"{XML_INDENT}<block type=\"{block_type}\">")

            # 生成每个参数的value/shadow节点
            for param in params:
                shadow_type, field_name, default_val = get_shadow_type_and_value(param, block_type, custom_defaults)

                # value节点
                xml_lines.append(f"{XML_INDENT * 2}<value name=\"{param}\">")
                # shadow节点
                xml_lines.append(f"{XML_INDENT * 3}<shadow type=\"{shadow_type}\">")
                # field节点
                xml_lines.append(f"{XML_INDENT * 4}<field name=\"{field_name}\">{default_val}</field>")
                # 闭合shadow
                xml_lines.append(f"{XML_INDENT * 3}</shadow>")
                # 闭合value
                xml_lines.append(f"{XML_INDENT * 2}</value>")

            # 闭合block标签
            xml_lines.append(f"{XML_INDENT}</block>")

    # 闭合根节点
    xml_lines.append("</category>")

    # 拼接所有行，处理空行缩进
    xml_content = "\n".join(xml_lines)
    # 修复空行的缩进（确保空行后内容仍有2空格缩进）
    xml_content = re.sub(r"\n\s*\n", f"\n{XML_INDENT}\n", xml_content)

    return xml_content

# ===================== 主函数：命令行交互 =====================
def main():
    parser = argparse.ArgumentParser(description="Blockly JS → BIPES XML 转换工具（通用Grove接口，无模块类型耦合）")
    parser.add_argument("--js-path", required=True, help="Blockly JS文件路径（必填，如ds1307_blocks.js）")
    parser.add_argument("--category", help="XML分类名（可选，默认从JS文件名推导，如PS2）")
    parser.add_argument("--desc", help="模块描述（可选，默认：前缀+Module，如PS2 Module）")
    parser.add_argument("--lib-name", help="库名（用于Install按钮，可选，默认前缀小写，如ps2）")
    parser.add_argument("--defaults", help="自定义参数默认值（可选，格式：adc1=26,adc2=27,pin1=0）")
    parser.add_argument("--output", help="XML输出路径（可选，默认：JS同目录/前缀.xml）")
    args = parser.parse_args()

    try:
        # 1. 解析JS文件
        js_info = parse_blockly_js(args.js_path)
        print(f"✅ 解析JS成功，提取到 {len(js_info['blocks'])} 个积木，前缀：{js_info['prefix']}")

        # 2. 解析自定义默认值
        custom_defaults = {}
        if args.defaults:
            for item in args.defaults.split(","):
                if "=" in item:
                    k, v = item.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    # 兼容布尔型默认值
                    if v.upper() in ["TRUE", "FALSE"]:
                        custom_defaults[k] = v.upper()
                    else:
                        try:
                            custom_defaults[k] = int(v)
                        except ValueError:
                            custom_defaults[k] = v

        # 3. 生成XML
        xml_content = generate_bipes_xml(
            js_parse_result=js_info,
            category_name=args.category,
            block_desc=args.desc,
            lib_name=args.lib_name,
            custom_defaults=custom_defaults
        )

        # 4. 输出XML文件
        if args.output:
            output_path = args.output
        else:
            # 默认输出路径：JS同目录/前缀.xml
            js_dir = os.path.dirname(args.js_path)
            output_path = os.path.join(js_dir, f"{js_info['prefix']}.xml")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        print(f"✅ XML生成成功！输出路径：{output_path}")
        print("\n📌 生成的XML预览：")
        print(xml_content[:500] + "..." if len(xml_content) > 500 else xml_content)

    except Exception as e:
        print(f"❌ 执行失败：{str(e)}")
        exit(1)


if __name__ == "__main__":
    main()