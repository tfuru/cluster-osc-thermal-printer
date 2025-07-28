/** SwitchOSCSendPlayer.js
 * 
 * 
 */

const MODE_PLAYER = {
  INITIALIZED: "INITIALIZED",
  OSC_SEND: "OSC_SEND"
}

// OSCアドレス定義
const OSC_ADDRESS_STRING = "/avatar/parameters/Printer";
const OSC_DEVICE_NAME = "Printer";

// 初期化
const initialized = () => {
  _.log("SwitchOSCSendPlayer initialized");
}

const oscSend = (arg) => {
  _.log(`SwitchOSCSendPlayer oscSend: ${arg.text}`);
  
  // OSC送信処理
  // /avatar/parameters/Printer [timestamp (ms)] [デバイス名] [テキスト]
  const t = OscValue.float((Date.now() / 1000.0).toFixed(3));
  const deviceName = OscValue.asciiString(OSC_DEVICE_NAME);
  const txtBlob = OscValue.blob(arg.text);
  const msg = new OscMessage(OSC_ADDRESS_STRING, [t, deviceName, txtBlob]);

  const oscHandle = _.oscHandle;
  oscHandle.send(msg);
}

_.onReceive((messageType, arg, sender) => {
  _.log(`Received message: ${messageType}, ${arg}`);
  switch (messageType) {
    case MODE_PLAYER.INITIALIZED:
      initialized();
      break;
    case MODE_PLAYER.OSC_SEND:
      // OSC送信処理
      oscSend(arg);
      break;
    default:
      _.log(`Unhandled message type: ${messageType}`);
      break;
  }
});
