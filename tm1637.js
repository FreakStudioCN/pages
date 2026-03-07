/// Auto-generated for tm1637 (BIPES Blockly Definition)
/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2

Blockly.Blocks['tm1637_init'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637InitTitle'])
        .appendField(new Blockly.FieldImage(
            "media/tm1637.png",
            300, 300,
            "*"
        ));

    this.appendValueInput("pin1")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("PIN1");

    this.appendValueInput("pin2")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("PIN2");

    this.appendValueInput("brightness")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("brightness"), "BRIGHTNESS_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(135);
    this.setTooltip(MSG['TM1637InitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_brightness'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodBrightnessTitle']);

    this.appendValueInput("val")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("val"), "VAL_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodBrightnessTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_write'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodWriteTitle']);

    this.appendValueInput("segments")
        .setCheck("Array")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("segments"), "SEGMENTS_MSG");

    this.appendValueInput("pos")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("pos"), "POS_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodWriteTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_encode_digit'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodEncodeDigitTitle']);

    this.appendValueInput("digit")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("digit"), "DIGIT_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodEncodeDigitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_encode_string'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodEncodeStringTitle']);

    this.appendValueInput("string")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("string"), "STRING_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodEncodeStringTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_encode_char'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodEncodeCharTitle']);

    this.appendValueInput("char")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("char"), "CHAR_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodEncodeCharTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_hex'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodHexTitle']);

    this.appendValueInput("val")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("val"), "VAL_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodHexTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_number'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodNumberTitle']);

    this.appendValueInput("num")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("num"), "NUM_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodNumberTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_numbers'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodNumbersTitle']);

    this.appendValueInput("num1")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("num1"), "NUM1_MSG");

    this.appendValueInput("num2")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("num2"), "NUM2_MSG");

    this.appendValueInput("colon")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("colon"), "COLON_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodNumbersTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_temperature'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodTemperatureTitle']);

    this.appendValueInput("num")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("num"), "NUM_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodTemperatureTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_show'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodShowTitle']);

    this.appendValueInput("string")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("string"), "STRING_MSG");

    this.appendValueInput("colon")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("colon"), "COLON_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodShowTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['tm1637_method_scroll'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['TM1637MethodScrollTitle']);

    this.appendValueInput("string")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("string"), "STRING_MSG");

    this.appendValueInput("delay")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("delay"), "DELAY_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['TM1637MethodScrollTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};
