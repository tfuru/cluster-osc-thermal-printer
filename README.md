# Cluster OSC Thermal Printer
cluster のワールドから入力されたテキストを、OSC を通じて
Thermal Printer に送信するためのコードです。

## 概要
このコードは、Cluster のワールドからの入力を受け取り、OSC (Open Sound Control) プロトコルを使用して、Thermal Printer に送信します。

## Python コード
USB接続された Thermal Printer にテキストを送信するための Python スクリプト  
[README](./Python/README.md)

## Unity (Creator Kit Script) コード
ワールドで入力されたテキストを、OSC メッセージを送信する Unity スクリプト
[README](./Unity/README.md)]

## OSC データ
Cluster のワールドから送信される OSC メッセージの形式は以下の通りです。
```
/avatar/parameters/Printer [timestamp (ms)] [デバイス名] [テキスト]
/avatar/parameters/Printer 1752857438185 Printer "Hello, World!"
```