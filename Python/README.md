# Cluster OSC Thermal Printer
cluster のワールドから入力されたテキストを、OSC (Open Sound Control) を通じてPCに接続されたサーマルプリンターに印刷するためのPythonプロジェクトです。

## 概要
このスクリプトは、指定されたIPアドレスとポートでOSCメッセージを待ち受けます。
clusterのワールドから特定のOSCアドレス（例: `/cluster/print`）に文字列が送信されると、その内容をシリアル接続されたサーマルプリンターに印刷します。

日本語の印刷にも対応しています。

## 1. 準備

### 1.1. プリンターのシリアルポートを調べる
スクリプトの実行には、お使いのプリンターがどのシリアルポートに接続されているかを知る必要があります。

#### macOS / Linux の場合
プリンターをPCに接続してから、ターミナルで以下のコマンドを実行してデバイスファイル名を探します。

```bash
lsusb 

Bus 000 Device 002: ID 0483:5840 STMicroelectronics 58Printer 
```

### 1.2. 必要なライブラリのインストール

#### libusb
このスクリプトが使用する `python-escpos` ライブラリは、`libusb` というライブラリに依存しています。OSに応じてインストールしてください。

- **macOS**: `brew install libusb`
- **Linux (Debian/Ubuntu)**: `sudo apt-get install libusb-1.0-0`
- **Windows**: Zadig などのツールを使い、プリンターに `libusb` または `WinUSB` ドライバを割り当てる必要があります。詳細は `python-escpos` のドキュメントを参照してください。

#### Python ライブラリ
**以降のコマンドは、すべてプロジェクトのルートディレクトリ（`Python`フォルダがある場所）で実行してください。**

Python 3.x の環境で、以下のコマンドを実行して、このプロジェクト専用の仮想環境を作成し、ライブラリをインストールします。
```bash
# 仮想環境の作成と有効化 (推奨)
# これにより、PCの他のPython環境を汚さずにライブラリをインストールできます。
# プロジェクトのルートに `venv` フォルダが作成されます。
python -m venv venv

# --- ここからOSに合わせて実行 ---
# macOS / Linux の場合:
. venv/bin/activate

# Windows (コマンドプロンプト / PowerShell) の場合:
venv\Scripts\activate
# --------------------------

# 依存ライブラリのインストール
# コマンドラインの先頭に `(venv)` と表示されていれば、仮想環境は有効です。
# `Python` フォルダ内の requirements.txt を指定します。
pip install -r requirements.txt

# (任意) インストールの確認
# 以下のコマンドを実行し、`pythonosc` と `python-escpos` が表示されれば成功です。
pip list
```

## 実行
以下のコマンドでスクリプトを実行します。

```bash
. venv/bin/activate
python main.py --ip 127.0.0.1 --port 9000 --osc-address /osc/print --vendor 0x0483 --product 0x5840

python main.py --vendor 0x0483 --product 0x5840 --test "Hello World"
```

## フォントをダウンロードする
FLOPDesignFont.ttf をダウンロードして、`fonts` フォルダに配置してください。  
フォントは、[FLOPDesignFont](https://flopdesign.booth.pm/items/2296481) から入手できます。　　
