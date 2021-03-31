# チューター用 PDF化した模試のリネームソフトウェア

import glob
import io
import os
import shutil
# import queue
from pathlib import Path

import PySimpleGUI as sg
from pdf2image import convert_from_path
from PIL import Image, ImageTk

# 別ファイルの模試等リスト
import name_list


# パスの冗長性に使う関数
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# レイアウト生成時の初期画像のための画像関数


def get_img_data(f, maxsize=(300, 300), first=True):
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


# PDFのパスを受け取ってJPEGに変換する関数
def pdf_to_jpeg(pdf_file_path):
    # poppler/binを環境変数PATHに追加する
    poppler_dir = Path(__file__).parent.absolute() / \
        resource_path('./poppler/bin')
    os.environ["PATH"] += os.pathsep + str(poppler_dir)

    # PDFファイルのパス
    pdf_path = Path(pdf_file_path)

    # PDF -> Image に変換（100dpi）
    pages = convert_from_path(str(pdf_path), 100, first_page=1, last_page=3)

    # 画像ファイルを１ページずつ保存
    image_dir = Path(resource_path("./image_file"))
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpg"
        image_path = image_dir / file_name
        # JPEGで保存
        page.save(str(image_path), "JPEG")



# 画像ファイルを見つける関数
def parse_folder(pdf_name):
    images = glob.glob(resource_path(f'./image_file/{pdf_name}*.jpg'))
    return images


def load_image(path, window):
    try:
        image = Image.open(path)
        image.thumbnail((300, 300))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"{path}が開けません。もう一度やり直してください。")


def rename_file(year, school, exam, subject, qa, bef_path, output_dir):
    # "PDF化した模試"のディレクトリを事前に内部で設定しておく処理の追加必要あり

    # "PDF化した模試"のディレクトリ(仮)
    dig_path = resource_path(output_dir)
    # 移動後のパス
    dst_path = dig_path+f'/{year}/{school}/{exam}/{qa}/'
    # 変更後のファイル名
    new_name = f'{year}_{school}_{exam}_{subject}_{qa}.pdf'

    # ファイル名変更の処理
    os.rename(bef_path, new_name)

    # 階層分けを行う
    # 移動後の新しいPDFのパスを格納(~/xxxx.pdf)
    os.makedirs(dst_path, exist_ok=True)
    shutil.move('./'+new_name, dst_path)

    title = window['title']
    title.Update(f'"{year}_{school}_{exam}_{subject}_{qa}"に変更完了。')


# q = queue.Queue()


# PySimpleGuiの設定
sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {
    'BACKGROUND': '#2f3640',
    'TEXT': '#dcdde1',
    'INPUT': '#dcdde1',
    'SCROLL': '#dcdde1',
    'TEXT_INPUT': '#2f3640',
    'BUTTON': ('#dcdde1', '#e84118'),
    'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 0,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

sg.theme('MyNewTheme')

year_list = name_list.year_list
school_list = name_list.school_list
exam_list = []
subject_list = name_list.subject_list

YuGo = '游ゴシック'
T_setting = {'font': YuGo, 'size': (8, 1)}

image_line = [sg.Image(data=get_img_data(resource_path(
    './B5_sample.png')), key='image'), sg.Output(key='queue')]
pn_line = [sg.T(size=(3, 1)), sg.Button('Prev', size=(6, 1)),
           sg.T(size=(2, 1)), sg.Button('Next', size=(6, 1))]

file_line = [sg.T('ファイル', **T_setting),
             sg.InputText(font=YuGo, readonly=True, size=(41, 1),
                          enable_events=True, key='browse_files'),
             sg.FilesBrowse('選択', font=(YuGo, 10), size=(6, 1)), sg.FolderBrowse('A', font=(YuGo, 10), size=(2, 1), key='output_dir')]
year_line = [sg.T('年度', **T_setting),
             sg.Combo(year_list, default_value='2021', size=(10, 1), font=YuGo, readonly=True, key='year')]
school_line = [sg.T('予備校名', **T_setting), sg.Combo(school_list,
                                                   size=(10, 1), font=YuGo, readonly=True, key='school', enable_events=True)]
exam_line = [sg.T('模試名', **T_setting),
             sg.Combo(exam_list, size=(20, 1), font=YuGo, readonly=True, key='exam')]
subject_line = [sg.T('科目名', **T_setting), sg.Combo(subject_list,
                                                   size=(20, 1), font=YuGo, readonly=True, key='subject')]
qa_line = [sg.T('問題/解答', **T_setting),
           sg.Radio('問題', group_id='QA', default=True, font=YuGo, key='que'),
           sg.Radio('解答', group_id='QA', font=YuGo, key='ans')]
ok_line = [sg.Button('OK', size=(8, 1)), sg.T(
    ''), sg.T('', font=YuGo, size=(47, 1), key='title')]

layout = [image_line, pn_line, file_line, year_line,
          school_line, exam_line, subject_line, qa_line, ok_line]


window = sg.Window('PDF化した模試のリネーム', layout)
images = []
location = 0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'browse_files':
        path = values['browse_files']
        path_list = path.split(';')
        for contain in path_list:
            pdf_to_jpeg(contain)
            backplace = contain.rfind('/')
            print(contain[backplace+1:])

            images = parse_folder(contain[backplace+1:-4])
        if images:
            load_image(images[0], window)

    if event == 'school':
        exam_list = name_list.divide_exam(values['school'])
        window['exam'].Update('')
        window['exam'].Update(values=exam_list)

    # リネーム処理への移行
    if event == 'OK':
        qa = '問題' if values['que'] else '解答'

        rename_file(values['year'], values['school'],
                    values['exam'], values['subject'], qa, path, values['output_dir'])

    # Nextボタン
    if event == "Next" and images:
        if location == len(images) - 1:
            location = 0
        else:
            location += 1
        load_image(images[location], window)
    # Prevボタン
    if event == "Prev" and images:
        if location == 0:
            location = len(images) - 1
        else:
            location -= 1
        load_image(images[location], window)

window.close()
