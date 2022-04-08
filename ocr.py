import os
from PIL import Image
import pyocr

# インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
# OS自体に設定してあれば以下の2行は不要
path = 'C:\\Program Files\\Tesseract-OCR'
os.environ['PATH'] = os.environ['PATH'] + path

# pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
tool = tools[0]

input_dir = "ocr"
if not os.path.exists(input_dir):
    os.mkdir(input_dir)
files = os.listdir(input_dir)

list = []

for file in files:
    # OCR対象の画像ファイルを読み込む
    # img = Image.open("test.jpg")
    img = Image.open(os.path.join(input_dir, file))

    # 画像から文字を読み込む
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    text = tool.image_to_string(img, lang="jpn", builder=builder)

    list.append(text)

    print(text)
    print()
    print(text.split("\n")[0])
    print()
    print(text.split("\n")[0].replace("\"", ""))
    print()
    print(text.split("\n")[-2])
    print()
    f = open('myfile.txt', 'a')
    f.write(text.split("\n")[-2].replace("\"", ""))
    f.write("\n")
# print(list)
