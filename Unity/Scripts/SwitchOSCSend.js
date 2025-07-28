/** SwitchOSCSend
 * 
 * 1. 1回目 インタラクトで プレイヤースクリプトを設定
 * 2. 2回目 インタラクトで、テキスト入力を要求
 * 3. テキスト入力が完了したら、OSCメッセージを送信
 * 
 */

const MODE_PLAYER = {
  INITIALIZED: "INITIALIZED",
  OSC_SEND: "OSC_SEND"
}

const MODE = {
  INITIALIZED: "INITIALIZED",
  TEXT_INPUT: "TEXT_INPUT",
  ON_TEXT_INPUT: "ON_TEXT_INPUT",
  SEND_OSC_MESSAGE: "SEND_OSC_MESSAGE"
}

const META_TEXT_INPUT = "META_TEXT_INPUT";

const setMode = (mode) => {
  switch (mode) {
    case MODE.INITIALIZED:
      $.log("SwitchOSCSend initialized");
      initialized();
      break;
    case MODE.TEXT_INPUT:
      $.log("SwitchOSCSend text input mode");
      iextInput();
      break;
    case MODE.ON_TEXT_INPUT:
      $.log("SwitchOSCSend text input mode");
      onTextInput();
      break;
    case MODE.SEND_OSC_MESSAGE:
      $.log("SwitchOSCSend send OSC message mode");
      sendOSCMessage();
      break;
    default:
      $.log(`Unhandled mode: ${mode}`);
      break;
  }
}

const initialized = () => {
  $.log("SwitchOSCSend initialized");
}

const iextInput = () => {
  // テキスト入力を要求する
  $.state.inputText = "";
  const player = $.state.textInputPlayer;
  player.requestTextInput(META_TEXT_INPUT, "OSC送信するテキストを入力してください");
}

const onTextInput = () => {
  $.log(`inputText: ${$.state.inputText}`);
  setMode(MODE.SEND_OSC_MESSAGE);
}

const sendOSCMessage = () => {
  const player = $.state.textInputPlayer;
  const text = $.state.inputText;
  $.log(`sendOSCMessage ${player} ${text}`);
  player.send(MODE_PLAYER.OSC_SEND, {text: text});
}

$.onInteract(player => {
  let players = $.state.players || [];

  //players に player.id が存在しない場合のみ追加
  if (players.some(p => p.id === player.id)) {
    $.state.textInputPlayer = player;
    setMode(MODE.TEXT_INPUT);
    return;
  }

  players.push(player);
  $.state.players = players;

  // player のスクリプトを設定
  $.setPlayerScript(player);
  player.send(MODE_PLAYER.INITIALIZED, {});
  setMode(MODE.INITIALIZED);
});

$.onTextInput((text, meta, status) => {
  switch(status) {
    case TextInputStatus.Success:
      $.log(text);
      $.state.inputText = text;
      setMode(MODE.ON_TEXT_INPUT);
      break;
    default:
      $.log(`Text input status: ${status}`);
      break;
    /*
    case TextInputStatus.Busy:
      // 5秒後にretryする
      $.state.should_retry = true;
      $.state.retry_timer = 5;
      break;
    case TextInputStatus.Refused:
      // 拒否された場合は諦める
      $.state.should_retry = false;
      break;
    */
  }
});