from PIL import Image, ImageChops
import os  # ファイルやフォルダ操作
import glob
import shutil
import datetime  # 現在時刻を取得
import pyocr

# インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
# OS自体に設定してあれば以下の2行は不要
path = 'C:\\Program Files\\Tesseract-OCR'
path_tesseract = 'C:\\Program Files\\Tesseract-OCR'
# path = 'C:\\Users\\Owner\\OneDrive - 室蘭工業大学\\画像編集\\3tai2\\jpn_vert.traineddata'
# os.environ['PATH'] = os.environ['PATH'] + path
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
tool = tools[0]

builder = pyocr.builders.TextBuilder(tesseract_layout=6)

dir_name = "input"  # 画像が入っているフォルダ
new_dir_name = "output"  # 画像を保存する先のフォルダ
used_dir_name = "used"


def crop_center(pil_img, crop_width, crop_height):  # 画像の中心を切り出し
    img_width, img_height = pil_img.size  # 画像の横幅と縦の長さを取得
    # 引数の長さにトリミング
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def ocr_name(im_original):

    # 画像から文字を読み込む
    text = tool.image_to_string(im_original, lang="jpn", builder=builder)

    list = []
    list.append(text)

    # print(text.split("\n")[-2])

    body = text.split("\n")[0]
    body = body.replace("\"", "")
    body = body.replace("/", "")
    body = body.replace(" ", "")
    body = body.replace("?", "")
    body = body.replace("*", "")
    title = text.split("\n")[-3]
    title = title.replace("\"", "")
    title = title.replace(" ", "")
    title = title.replace("?", "")
    title = title.replace("*", "")

    return body, title


def func():
    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(new_dir_name):
        os.mkdir(new_dir_name)

    # ディレクトリが存在しない場合は作成する
    if not os.path.exists(used_dir_name):
        os.mkdir(used_dir_name)

    # glob.glob()で抽出された複数のファイルを一括で移動
    def move_glob(dst_path, pathname, recursive=True):
        for p in glob.glob(pathname, recursive=recursive):
            shutil.move(p, dst_path)

    # pngファイルを移動
    move_glob(dir_name, '*.png')
    # jpgファイルを移動
    move_glob(dir_name, '*.jpg')

    files = os.listdir(dir_name)

    i = 1

    for file in files:  # ホーム画面用の処理

        im_original = Image.open(os.path.join(dir_name, file))
        width, height = im_original.size

        # ステータスバーを考慮して正方形にトリミング
        im_crop = im_original.crop((0, 41+50, width, 41+50+width))

        dt_now = datetime.datetime.now()
        body, title = ocr_name(im_crop)
        name_png = title
        name_png += "_"
        name_png += body
        name_jpg = name_png + ".jpg"
        name_png += ".png"

        # 切り抜いた画像を保存
        # im_crop.save(os.path.join(new_dir_name, name_png))

        im_crop = im_crop.convert('RGB')  # RGBA(png)→RGB(jpg)へ変換
        im_crop.save(os.path.join(new_dir_name, name_jpg), "JPEG", quality=95)

        # 1枚ごとに完了を報告
        print(str(i) + " " + name_jpg + " done!")
        i += 1

    # 使った画像は使用済みファイルに移動
    move_glob(used_dir_name, "./input/*.PNG")
    move_glob(used_dir_name, "./input/*.JPG")

    # 終了時に元の画像を削除
    # shutil.rmtree(dir_name)

    # すべて完了
    print("Exit a program")


if __name__ == "__main__":
    print("Execute a program")
    func()
