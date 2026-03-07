# Python env   :               
# -*- coding: utf-8 -*-        
# @Time    : 2026/3/6 下午10:58   
# @Author  : 李清水            
# @File    : py_xml.py       
# @Description : 纯JS解析生成BIPES XML，无硬耦合/无默认值硬编码

import re
import os
import argparse

# ===================== 通用配置（仅固定BIPES规范配置，无业务耦合） =====================
# 固定库地址（BIPES规范要求的统一地址）
DEFAULT_LIB_URL = "https://github.com/FreakStudioCN/GraftSense-Drivers-MicroPython"
# 固定回调键（BIPES规范要求）
DEFAULT_CALLBACK_KEY = "installPyLib"
# 2空格缩进（BIPES XML格式规范）
XML_INDENT = "  "

# ===================== Field类型映射（仅BIPES规范映射，无业务逻辑） =====================
FIELD_TYPE_MAP = {
    # JS Field类型 → BIPES Shadow类型 + Field名
    "FieldNumber": ("math_number", "NUM"),
    "FieldCheckbox": ("logic_boolean", "BOOL"),
    "FieldTextInput": ("text", "TEXT"),
    "FieldDropdown": ("dropdown", "DROP"),
    "pinout_label": ("pinout", "PIN"),  # 引脚类静态标签 → pinout类型
    "FieldArray": ("array", "ARRAY"),
    "default": ("math_number", "NUM")   # 兜底默认
}


# ===================== 工具函数：深度解析Blockly JS（提取参数+Field类型+默认值） =====================
def parse_blockly_js(js_path: str) -> dict:
    """
    深度解析Blockly JS文件，仅从JS内容提取：
    1. 积木类型
    2. 参数名
    3. 参数对应的Field类型（从appendField推导）
    4. 参数对应的默认值（从JS的Field构造函数提取）
    无任何硬编码默认值/模块专属规则
    返回格式：
    {
        "blocks": [
            {
                "type": "max9814mic_init",
                "params": [
                    {
                        "name": "adc_pin",
                        "field_type": "pinout_label",
                        "default_val": ""
                    },
                    {
                        "name": "vref",
                        "field_type": "FieldNumber",
                        "default_val": 3.3
                    }
                ]
            }
        ],
        "prefix": "max9814mic",  # 积木前缀（从第一个积木type推导）
        "filename_prefix": "max9814mic"  # 文件名前缀
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

    # 2. 深度解析每个积木的参数（仅从JS提取，无外部规则）
    blocks_info = []
    for block_type in block_types:
        # 提取该积木的init函数完整内容（避免跨积木匹配）
        block_init_pattern = re.compile(
            rf"Blockly\.Blocks\['{block_type}'\]\s*=\s*\{{\s*init:\s*function\(\)\s*\{{(.*?)\}}\s*\}};",
            re.DOTALL | re.MULTILINE
        )
        init_match = block_init_pattern.search(js_content)
        params = []

        if init_match:
            init_content = init_match.group(1)
            # 匹配所有appendValueInput块（提取参数名+Field信息）
            value_input_pattern = re.compile(
                r'appendValueInput\("([a-zA-Z0-9_]+)"\)(.*?);',
                re.DOTALL | re.MULTILINE
            )
            value_input_matches = value_input_pattern.findall(init_content)

            for param_name, field_content in value_input_matches:
                param_info = {
                    "name": param_name,
                    "field_type": "default",
                    "default_val": ""
                }

                # 解析Field类型和默认值（仅从JS提取）
                # 匹配FieldNumber：new Blockly.FieldNumber(3.3)
                field_number_pattern = re.compile(r"new Blockly\.FieldNumber\(([\d\.]+)\)")
                field_number_match = field_number_pattern.search(field_content)
                if field_number_match:
                    param_info["field_type"] = "FieldNumber"
                    param_info["default_val"] = field_number_match.group(1)

                # 匹配FieldCheckbox：new Blockly.FieldCheckbox("FALSE")
                field_checkbox_pattern = re.compile(r"new Blockly\.FieldCheckbox\(\"([A-Z]+)\"\)")
                field_checkbox_match = field_checkbox_pattern.search(field_content)
                if field_checkbox_match:
                    param_info["field_type"] = "FieldCheckbox"
                    param_info["default_val"] = field_checkbox_match.group(1)

                # 匹配引脚类静态标签：.appendField("ADC_PIN")
                field_pin_label_pattern = re.compile(r"\.appendField\(\"([A-Z_]+_PIN)\"\)")
                field_pin_label_match = field_pin_label_pattern.search(field_content)
                if field_pin_label_match:
                    param_info["field_type"] = "pinout_label"
                    param_info["default_val"] = ""  # 引脚无硬编码默认值，由BIPES动态提供

                # 匹配FieldTextInput：new Blockly.FieldTextInput("xxx")
                field_text_pattern = re.compile(r"new Blockly\.FieldTextInput\(\"(.*?)\"\)")
                field_text_match = field_text_pattern.search(field_content)
                if field_text_match:
                    param_info["field_type"] = "FieldTextInput"
                    param_info["default_val"] = field_text_match.group(1)

                params.append(param_info)

        blocks_info.append({
            "type": block_type,
            "params": params
        })

    # 3. 推导积木前缀（纯字符串解析，无业务规则）
    block_prefix = ""
    if blocks_info:
        first_block_type = blocks_info[0]["type"]
        prefix_match = re.match(r"^([a-zA-Z0-9]+)_", first_block_type)
        if prefix_match:
            block_prefix = prefix_match.group(1)

    # 4. 推导文件名前缀（纯字符串解析）
    filename = os.path.basename(js_path)
    filename_prefix = re.sub(r"_blocks\.js$|\.js$", "", filename)

    return {
        "blocks": blocks_info,
        "prefix": block_prefix or filename_prefix,
        "filename_prefix": filename_prefix
    }


# ===================== 工具函数：生成BIPES XML（仅用解析结果，无硬编码） =====================
def generate_bipes_xml(
        js_parse_result: dict,
        category_name: str = None,
        block_desc: str = None,
        lib_name: str = None
) -> str:
    """
    生成BIPES标准XML：
    1. 仅使用JS解析结果，无任何硬编码默认值/模块规则
    2. 纯字符串拼接，严格遵循BIPES格式规范
    """
    prefix = js_parse_result["prefix"]

    # 推导基础配置（纯字符串解析，无业务耦合）
    category_name = category_name or prefix.upper()
    block_desc = block_desc or f"{prefix.upper()} Module"
    lib_name = lib_name or prefix.lower()

    # 初始化XML字符串（手动拼接，逐行控制）
    xml_lines = []
    xml_lines.append(f"<category name=\"{category_name}\">")

    # 1. 库地址Label（完整闭合，BIPES规范）
    xml_lines.append(f"{XML_INDENT}<label text=\"Library: {DEFAULT_LIB_URL} \"></label>")

    # 2. Install按钮（完整闭合，BIPES规范）
    xml_lines.append(
        f"{XML_INDENT}<button text=\"Install {lib_name} library\" callbackKey=\"{DEFAULT_CALLBACK_KEY}\"></button>")

    # 3. 空行（对齐BIPES示例格式）
    xml_lines.append("")

    # 4. 模块描述Label（完整闭合）
    xml_lines.append(f"{XML_INDENT}<label text=\"{block_desc}\"></label>")

    # 5. 遍历生成每个积木的block节点（仅用解析结果）
    for block in js_parse_result["blocks"]:
        block_type = block["type"]
        params = block["params"]

        # 无参数block：单行完整闭合
        if not params:
            xml_lines.append(f"{XML_INDENT}<block type=\"{block_type}\"></block>")
        # 有参数block：多行缩进（仅用解析的Field类型/默认值）
        else:
            xml_lines.append(f"{XML_INDENT}<block type=\"{block_type}\">")

            # 生成每个参数的value/shadow节点（仅用解析结果）
            for param in params:
                param_name = param["name"]
                field_type = param["field_type"]
                default_val = param["default_val"]

                # 映射BIPES Shadow类型（仅用规范映射，无业务规则）
                shadow_type, field_name = FIELD_TYPE_MAP.get(field_type, FIELD_TYPE_MAP["default"])

                # 生成XML节点（无硬编码值）
                xml_lines.append(f"{XML_INDENT * 2}<value name=\"{param_name}\">")
                xml_lines.append(f"{XML_INDENT * 3}<shadow type=\"{shadow_type}\">")
                xml_lines.append(f"{XML_INDENT * 4}<field name=\"{field_name}\">{default_val}</field>")
                xml_lines.append(f"{XML_INDENT * 3}</shadow>")
                xml_lines.append(f"{XML_INDENT * 2}</value>")

            xml_lines.append(f"{XML_INDENT}</block>")

    # 闭合根节点
    xml_lines.append("</category>")

    # 拼接并格式化（仅格式处理，无业务逻辑）
    xml_content = "\n".join(xml_lines)
    # 修复空行缩进（符合BIPES格式）
    xml_content = re.sub(r"\n\s*\n", f"\n{XML_INDENT}\n", xml_content)

    return xml_content


# ===================== 主函数：命令行交互（仅解析+生成，无业务逻辑） =====================
def main():
    parser = argparse.ArgumentParser(description="Blockly JS → BIPES XML 转换工具（纯JS解析，无硬耦合）")
    parser.add_argument("--js-path", required=True, help="Blockly JS文件路径（必填，如max9814_mic.js）")
    parser.add_argument("--category", help="XML分类名（可选，默认从JS文件名推导）")
    parser.add_argument("--desc", help="模块描述（可选，默认：前缀+Module）")
    parser.add_argument("--lib-name", help="库名（用于Install按钮，可选，默认前缀小写）")
    parser.add_argument("--output", help="XML输出路径（可选，默认：JS同目录/前缀.xml）")
    args = parser.parse_args()

    try:
        # 1. 解析JS文件（纯解析，无硬编码）
        js_info = parse_blockly_js(args.js_path)
        print(f"✅ 解析JS成功，提取到 {len(js_info['blocks'])} 个积木，前缀：{js_info['prefix']}")

        # 2. 生成XML（仅用解析结果）
        xml_content = generate_bipes_xml(
            js_parse_result=js_info,
            category_name=args.category,
            block_desc=args.desc,
            lib_name=args.lib_name
        )

        # 3. 输出XML文件
        if args.output:
            output_path = args.output
        else:
            js_dir = os.path.dirname(args.js_path)
            output_path = os.path.join(js_dir, f"{js_info['prefix']}.xml")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        print(f"✅ XML生成成功！输出路径：{output_path}")
        print("\n📌 生成的XML预览：")
        print(xml_content[:800] + "..." if len(xml_content) > 800 else xml_content)

    except Exception as e:
        print(f"❌ 执行失败：{str(e)}")
        exit(1)


if __name__ == "__main__":
    main()