/// Auto-generated for ds1307 (BIPES Blockly Definition)
/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2

Blockly.Blocks['ds1307_init'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307InitTitle'])
        .appendField(new Blockly.FieldImage(
            "media/ds1307.png",
            300, 300,
            "*"
        ));

    this.appendValueInput("i2c_bus")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("i2c_bus (I2C bus number)"), "I2C_BUS_MSG");

    this.appendValueInput("sda_pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SDA_PIN");

    this.appendValueInput("scl_pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SCL_PIN");

    this.appendValueInput("baudrate")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("baudrate (Baud rate)"), "BAUDRATE_MSG");

    this.appendValueInput("addr")
        .setCheck("Any")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("addr (optional)"), "ADDR_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(135);
    this.setTooltip(MSG['DS1307InitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['ds1307_property_datetime'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307PropertyDatetimeTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['DS1307PropertyDatetimeTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['ds1307_property_set_datetime'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307PropertySetDatetimeTitle']);

    this.appendValueInput("datetime")
        .setCheck("Array")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("datetime (optional)"), "DATETIME_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['DS1307PropertySetDatetimeTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['ds1307_property_datetimeRTC'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307PropertyDatetimertcTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['DS1307PropertyDatetimertcTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['ds1307_property_disable_oscillator'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307PropertyDisableOscillatorTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['DS1307PropertyDisableOscillatorTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['ds1307_property_set_disable_oscillator'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['DS1307PropertySetDisableOscillatorTitle']);

    this.appendValueInput("value")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("value"), "VALUE_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['DS1307PropertySetDisableOscillatorTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};
