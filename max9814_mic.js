/// Auto-generated for max9814_mic (BIPES Blockly Definition)
/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2

Blockly.Blocks['max9814mic_init'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicInitTitle'])
        .appendField(new Blockly.FieldImage(
            "media/max9814_mic.png",
            300, 300,
            "*"
        ));

    this.appendValueInput("adc_pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("ADC_PIN");

    this.appendValueInput("gain_pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("GAIN_PIN");

    this.appendValueInput("shdn_pin")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SHDN_PIN");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(135);
    this.setTooltip(MSG['MAX9814MicInitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_read'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodReadTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodReadTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_read_normalized'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodReadNormalizedTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodReadNormalizedTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_read_voltage'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodReadVoltageTitle']);

    this.appendValueInput("vref")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(3.3), "VREF_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodReadVoltageTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_enable'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodEnableTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodEnableTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_disable'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodDisableTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodDisableTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_set_gain'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodSetGainTitle']);

    this.appendValueInput("high")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldCheckbox("FALSE"), "HIGH_MSG");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodSetGainTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_get_state'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodGetStateTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodGetStateTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_get_average_reading'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodGetAverageReadingTitle']);

    this.appendValueInput("samples")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(10), "SAMPLES_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodGetAverageReadingTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_get_peak_reading'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodGetPeakReadingTitle']);

    this.appendValueInput("samples")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(100), "SAMPLES_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodGetPeakReadingTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_detect_sound_level'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodDetectSoundLevelTitle']);

    this.appendValueInput("threshold")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(35000), "THRESHOLD_MSG");

    this.appendValueInput("samples")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(50), "SAMPLES_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodDetectSoundLevelTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['max9814mic_method_calibrate_baseline'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['MAX9814MicMethodCalibrateBaselineTitle']);

    this.appendValueInput("samples")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldNumber(100), "SAMPLES_MSG");

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['MAX9814MicMethodCalibrateBaselineTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};
