import argparse
import sys
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from escpos.printer import Usb
import usb.core

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# グローバル変数としてプリンターオブジェクトを保持
printer = None

# フォントの保存先
fontPath = "fonts/FLOPDesignFont.ttf"

# image を生成する
def createImage(text):
    width = 500
    height = 250
    image = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontPath, 28, encoding='unic')

    tests = text.split("\\n")
    for i, t in enumerate(tests):
        draw.text((0, i * 28), t, font=font, fill=0)        
    # draw.text((0, 0), f"{text}", font=font, fill=0)
    # font = ImageFont.truetype(fontPath, 28, encoding='unic')
    # draw.text((0, 82), "abcdefghijklmnopqrstuvwxyz", font=font, fill=0)
    # draw.text((0, 112), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=font, fill=0)
    # draw.text((0, 142), "1234567890" + " ", font=font, fill=0)
    # draw.text((0, 172), "!\"#$%&'()=~|+*<>?_{}" + " ", font=font, fill=0)
    return image

# テスト用
def test(args):
    print(f"プリンターを検索中...")
    try:
        printer = Usb(idVendor=args.vendor, idProduct=args.product, timeout=0, in_ep=0x01, out_ep=0x04)
        # image を生成して 印刷する
        img = createImage(args.test)
        printer.image(img)
        # printer.cut()
        print("印刷が完了しました。")
    except Exception as e:
        print(f"印刷中にエラーが発生しました: {e}")

def print_handler(address: str, *args: list):
    """
    OSCメッセージを受け取り、プリンターに印刷するハンドラ
    """
    global printer
    if not printer:
        print("エラー: プリンターが初期化されていません。")
        return

    # OSCメッセージの引数が1つ以上あるか確認
    if not args:
        print("警告: 印刷するテキストがありません。")
        return

    # 最初の引数をテキストとして取得
    text_to_print = str(args[0])
    print(f"受信したテキスト: {text_to_print}")

    try:
        # プリンターにテキストを送信して印刷し、改行とカットを行う
        printer.text(text_to_print + "\n")
        printer.cut()
        print("印刷が完了しました。")
    except Exception as e:
        print(f"印刷中にエラーが発生しました: {e}")

def main():
    """
    メイン処理
    コマンドライン引数を解釈し、プリンターを初期化してOSCサーバーを起動する
    """
    global printer

    parser = argparse.ArgumentParser(
        description="clusterからのOSCメッセージをサーマルプリンターに印刷します。"
    )
    parser.add_argument("--ip", default="127.0.0.1", help="OSCサーバーを起動するIPアドレス")
    parser.add_argument("--port", type=int, default=9000, help="OSCサーバーが使用するポート番号")
    parser.add_argument("--vendor", default="0483", type=lambda x: int(x, 0), required=True, help="プリンターのベンダーID")
    parser.add_argument("--product", default="5840", type=lambda x: int(x, 0), required=True, help="プリンターのプロダクトID")
    parser.add_argument("--osc-address", default="/osc/print", help="待機するOSCアドレス")
    parser.add_argument("--test", default="", help="テスト用オプション")
    args = parser.parse_args()

    # --test が 空文字以外の場合 test(args) を実行
    if args.test:
        test(args)
        sys.exit(0)

    # プリンターの初期化
    try:
        print(f"プリンターを検索中...")
        printer = Usb(idVendor=args.vendor, idProduct=args.product, timeout=0, in_ep=0x01, out_ep=0x04)
        print("プリンターの接続に成功しました。")
    except Exception as e:
        print(f"エラー: プリンターの初期化に失敗しました: {e}")
        print("ベンダーID/プロダクトIDが正しいか、プリンターがPCに接続・認識されているか確認してください。")
        sys.exit(1)

    # OSCサーバーのセットアップ
    disp = Dispatcher()
    disp.map(args.osc_address, print_handler)

    server = ThreadingOSCUDPServer((args.ip, args.port), disp)
    print(f"OSCサーバーを起動します: http://{server.server_address[0]}:{server.server_address[1]}")
    print(f"OSCアドレス '{args.osc_address}' でメッセージを待機します...")
    print("Ctrl+Cで終了します。")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nサーバーを終了します。")
    finally:
        if printer:
            printer.close()
        server.server_close()

if __name__ == "__main__":
    main()