/// Auto-generated for relay (BIPES Blockly Definition)
/// Source: https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2

Blockly.Blocks['relaycontroller_init'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerInitTitle'])
        .appendField(new Blockly.FieldImage(
            "media/relay.png",
            300, 300,
            "*"
        ));

    this.appendValueInput("relay_type")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(new Blockly.FieldLabelSerializable("relay_type"), "RELAY_TYPE_MSG");

    this.appendValueInput("pin1")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("PIN1");

    this.appendValueInput("pin2")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("PIN2 (optional)");

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(135);
    this.setTooltip(MSG['RelayControllerInitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['relaycontroller_method_get_state'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerMethodGetStateTitle']);

    this.setOutput(true, null);

    this.setColour(230);
    this.setTooltip(MSG['RelayControllerMethodGetStateTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['relaycontroller_method_on'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerMethodOnTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['RelayControllerMethodOnTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['relaycontroller_method_off'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerMethodOffTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['RelayControllerMethodOffTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['relaycontroller_method_toggle'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerMethodToggleTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['RelayControllerMethodToggleTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};

Blockly.Blocks['relaycontroller_method_deinit'] = {
    init: function() {
    this.appendDummyInput()
        .appendField(MSG['RelayControllerMethodDeinitTitle']);

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip(MSG['RelayControllerMethodDeinitTitle']);
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
    }
};
