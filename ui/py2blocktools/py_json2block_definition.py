# -*- coding: utf-8 -*-
import json
from pathlib import Path


def map_check_type(json_check_type: str) -> str | None:
    """
    将JSON中的check_type映射为Blockly可识别的类型
    - Any → null（无类型限制）
    - bytes/bytearray → Array（用数组类型代替）
    - 其他类型直接返回（保持首字母大写）
    """
    if json_check_type == "Any":
        return None
    elif json_check_type in ["bytes", "bytearray"]:
        return "Array"
    else:
        return json_check_type


def get_field_code(field: dict, input_name: str) -> str:
    """
    根据field_type生成对应的Blockly Field代码（移除不可靠的min/max/precision依赖）
    """
    field_type = field.get('field_type', '')
    label = field.get('label', input_name)
    default_val = field.get('default', None)

    if field_type == 'pinout':
        # 引脚参数：显示静态文本标签（如SDA_PIN），动态下拉菜单由XML中的<shadow type="pinout">提供
        pin_label = input_name.upper() if "(optional)" not in label else f"{input_name.upper()} (optional)"
        return f'        .appendField("{pin_label}")'
    elif field_type == 'text_input':
        # 文本输入框：仅保留默认值（无其他不可靠参数）
        default_text = default_val if default_val is not None else ""
        return f'        .appendField(new Blockly.FieldTextInput("{default_text}"), "{input_name.upper()}_MSG")'
    elif field_type == 'numeric':
        # 数字输入框：移除min/max/precision（仅保留默认值，避免JSON错误）
        # 默认值为空时用0，确保Blockly不报错
        num_default = default_val if default_val is not None else 0
        return f'        .appendField(new Blockly.FieldNumber({num_default}), "{input_name.upper()}_MSG")'
    elif field_type == 'checkbox':
        # 复选框：仅保留默认值（TRUE/FALSE）
        checked = 'TRUE' if default_val else 'FALSE'
        return f'        .appendField(new Blockly.FieldCheckbox("{checked}"), "{input_name.upper()}_MSG")'
    elif field_type == 'dropdown':
        # 下拉菜单：仅保留基础结构（避免JSON中options错误）
        # 若JSON无options，用默认选项
        options = field.get('options', [])
        if not options:
            options = [['Option 1', 'OPT1'], ['Option 2', 'OPT2']]
        options_str = ', '.join([f"['{opt[0]}', '{opt[1]}']" for opt in options])
        return f'        .appendField(new Blockly.FieldDropdown([{options_str}]), "{input_name.upper()}_MSG")'
    else:
        # 默认：静态文本标签（仅用label，无其他参数）
        return f'        .appendField(new Blockly.FieldLabelSerializable("{label}"), "{input_name.upper()}_MSG")'


def get_clean_block_suffix(block_type, class_name):
    """
    从block_type中提取干净的后缀（如relaycontroller_init → init）
    """
    class_name_lower = class_name.lower()
    if block_type.startswith(class_name_lower + "_"):
        return block_type.replace(class_name_lower + "_", "")
    return block_type


def camel_case_suffix(suffix):
    """
    后缀转驼峰（如init → Init；method_get_state → MethodGetState）
    """
    if not suffix:
        return ""
    parts = suffix.split('_')
    return ''.join(part.capitalize() for part in parts)


def generate_block_js(json_path, js_output_path=None):
    """
    最终修正版：从JSON生成符合BIPES规范的Blockly积木JS（适配官方pinout逻辑）
    """
    # 固定配置
    FIXED_HELP_URL = "https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2"
    ICON_WIDTH = 300
    ICON_HEIGHT = 300

    # 读取JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    meta = json_data['meta']
    blocks = json_data['blocks']
    module_name = meta['module_name']
    class_name = meta['class_name']
    class_name_lower = class_name.lower()
    icon_path = f"media/{module_name}.png"

    # 初始化JS代码（严格4空格缩进）
    js_code = []
    js_code.append(f"/// Auto-generated for {module_name} (BIPES Blockly Definition)")
    js_code.append("/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2\n")

    for block in blocks:
        block_type = block['type']
        colour = block['colour']
        output_type = block['output_type']
        inputs = block['inputs']
        is_init_block = '_init' in block_type

        # 提取干净的后缀，生成正确的MSG键
        block_suffix = get_clean_block_suffix(block_type, class_name)
        suffix_camel = camel_case_suffix(block_suffix)
        msg_key = f"{class_name}{suffix_camel}Title"

        # 构建积木定义（严格4空格缩进）
        js_code.append(f"Blockly.Blocks['{block_type}'] = {{")
        js_code.append("    init: function() {")

        # 第一步：appendDummyInput（修复缩进+分号位置）
        dummy_lines = [
            "    this.appendDummyInput()",
            f"        .appendField(MSG['{msg_key}'])"
        ]
        if is_init_block:
            dummy_lines.extend([
                "        .appendField(new Blockly.FieldImage(",
                f"            \"{icon_path}\",",
                f"            {ICON_WIDTH}, {ICON_HEIGHT},",
                "            \"*\"",
                "        ))"
            ])
        # 分号放在最后一行末尾（同一行）
        dummy_lines[-1] += ";"
        js_code.extend(dummy_lines)
        js_code.append("")

        # 第二步：处理inputs（适配官方pinout逻辑 + 类型映射 + 可选参数）
        for input_item in inputs:
            input_name = input_item['name'].lower()
            check_type = input_item['check_type']
            # 映射为Blockly可识别的类型
            check_type_mapped = map_check_type(check_type)
            field = input_item['field']

            # 构建ValueInput行
            input_lines = [
                f"    this.appendValueInput(\"{input_name}\")",
            ]
            # 处理setCheck：映射后类型为None时，生成setCheck(null)
            if check_type_mapped is None:
                input_lines.append(f"        .setCheck(null)")
            else:
                input_lines.append(f"        .setCheck(\"{check_type_mapped}\")")
            input_lines.append(f"        .setAlign(Blockly.ALIGN_RIGHT)")

            # 生成对应的Field代码（适配官方pinout逻辑）
            input_lines.append(get_field_code(field, input_name) + ";")

            js_code.extend(input_lines)
            js_code.append("")

        # 第三步：设置statement/output（初始化块强制可串联）
        if is_init_block:
            js_code.append("    this.setPreviousStatement(true, null);")
            js_code.append("    this.setNextStatement(true, null);")
        else:
            if output_type is False:
                js_code.append("    this.setPreviousStatement(true, null);")
                js_code.append("    this.setNextStatement(true, null);")
            else:
                js_code.append("    this.setOutput(true, null);")
        js_code.append("")

        # 第四步：固定配置
        js_code.append(f"    this.setColour({colour});")
        js_code.append(f"    this.setTooltip(MSG['{msg_key}']);")
        js_code.append(f"    this.setHelpUrl(\"{FIXED_HELP_URL}\");")
        js_code.append("    }")
        js_code.append("};")
        js_code.append("")

    # 写入文件
    final_js = "\n".join(js_code)
    if js_output_path is None:
        js_output_path = Path(json_path).with_suffix('.js')
    with open(js_output_path, 'w', encoding='utf-8') as f:
        f.write(final_js)

    print(f"✅ 最终修正版JS生成完成：{js_output_path}")
    return str(js_output_path)


def main():
    import sys
    if len(sys.argv) != 2:
        print("使用方法：python json2bipes_block_final.py 目标JSON文件路径")
        sys.exit(1)

    json_path = sys.argv[1]
    if not Path(json_path).exists() or Path(json_path).suffix != '.json':
        print("错误：仅支持存在的.json文件")
        sys.exit(1)

    generate_block_js(json_path)


if __name__ == "__main__":
    main()