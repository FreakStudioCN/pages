/// Auto-generated for soil_moisture (BIPES Blockly Definition)
/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2

Blockly.Blocks['soilmoisturesensor_init'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorInitTitle'])
        .appendField(new Blockly.FieldImage(
            "media/soil_moisture.png",
            300, 300,
            "*"
        ));

    this.appendValueInput("pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("PIN");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(135);
    this.setTooltip(MSG['SoilMoistureSensorInitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_read_raw'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodReadRawTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodReadRawTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_calibrate_dry'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodCalibrateDryTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodCalibrateDryTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_calibrate_wet'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodCalibrateWetTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodCalibrateWetTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_set_calibration'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodSetCalibrationTitle']);

    this.appendValueInput("dry")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("dry"), "DRY_MSG");

    this.appendValueInput("wet")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("wet"), "WET_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodSetCalibrationTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_get_calibration'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodGetCalibrationTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodGetCalibrationTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_read_moisture'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodReadMoistureTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodReadMoistureTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_method_get_level'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorMethodGetLevelTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorMethodGetLevelTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_property_is_calibrated'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorPropertyIsCalibratedTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorPropertyIsCalibratedTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_property_raw'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorPropertyRawTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorPropertyRawTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_property_moisture'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorPropertyMoistureTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorPropertyMoistureTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['soilmoisturesensor_property_level'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['SoilMoistureSensorPropertyLevelTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['SoilMoistureSensorPropertyLevelTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};
