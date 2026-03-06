
// 自动生成的DS1307积木定义
// PY文件路径：G:\BIPES\ui\pylibs\ds1307.py
// 原始类：ds1307.DS1307

// 1. 初始化积木
Blockly.Blocks['ds1307_init'] = {
  init: function() {
    // 基础输入（图标+标题）
    this.appendDummyInput()
        .appendField("DS1307 Init")
        .appendField(new Blockly.FieldImage(
          "media/ds1307.png", 
          300, 300, 
          "*" 
        ));

    // 初始化参数
    
    this.appendValueInput("i2c_id")
      .setCheck("Number")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("I2C Bus ID")
      ;
      
    
    this.appendValueInput("scl_pin")
      .setCheck("Number")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("SCL Pin")
      
      .appendField(new Blockly.FieldNumber(5), "SCL_PIN");
      
    
    this.appendValueInput("sda_pin")
      .setCheck("Number")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("SDA Pin")
      
      .appendField(new Blockly.FieldNumber(4), "SDA_PIN");
      
    
    this.appendValueInput("addr")
      .setCheck("Number")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("Addr")
      
      .appendField(new Blockly.FieldNumber(104), "ADDR");
      
    

    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);

    this.setColour(230);
    this.setTooltip("Initialize self.  See help(type(self)) for accurate signature.");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};

// 2. 功能方法积木


// 输出型积木（有返回值）
Blockly.Blocks['ds1307_datetime'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("DS1307 datetime");
    
    this.setOutput(true, "Array");
    this.setColour(230);
    this.setTooltip("Get datetime from DS1307");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};



// 执行型积木（无返回值）
Blockly.Blocks['ds1307_set_datetime'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("DS1307 set_datetime");
    
    this.appendValueInput("datetime")
      .setCheck("Array")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("datetime");
    
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Set datetime for DS1307");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};



// 输出型积木（有返回值）
Blockly.Blocks['ds1307_datetimeRTC'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("DS1307 datetimeRTC");
    
    this.setOutput(true, "Array");
    this.setColour(230);
    this.setTooltip("Get datetimeRTC from DS1307");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};



// 输出型积木（有返回值）
Blockly.Blocks['ds1307_disable_oscillator'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("DS1307 disable_oscillator");
    
    this.setOutput(true, "Boolean");
    this.setColour(230);
    this.setTooltip("Get disable_oscillator from DS1307");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};



// 执行型积木（无返回值）
Blockly.Blocks['ds1307_set_disable_oscillator'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("DS1307 set_disable_oscillator");
    
    this.appendValueInput("value")
      .setCheck("Boolean")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("value");
    
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Set disable_oscillator for DS1307");
    this.setHelpUrl("https://freakstudio.cn/node/019b88b8-4451-7065-92ee-d20e8165a0c2");
  }
};

