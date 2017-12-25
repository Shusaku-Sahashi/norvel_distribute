from flask import Flask, render_template, request, url_for
import os

TITLE, URL =('必殺区分け人', 'index.html')
NOVEL_DIR = os.path.join(os.path.curdir, 'novels')

app = Flask(__name__)


def _get_novel_title_list():
    '''
    小説の名称一覧（ファイル名称一覧）を取得する。
    :return:
    '''
    # return [file for root, dir, file in os.walk(NOVEL_DIR)]
    return ['title_1', 'title_2']

def _init():
    """
    初期設定のためのメソッド
    1, 小説一覧の取得
    2,
    :return:
    """

def _do_select():
    pass

def _do_next():
    pass

def _do_set():
    pass

def _do_end():
    pass

res_actions = {
    'SELECT':   _do_select,
    'NEXT'  :   _do_next,
    'SET'   :   _do_set,
    'END'   :   _do_end
}

########################以降はページルーティング#################################
@app.route('/')
def index():
    return render_template(URL, title=TITLE, novel_titles=_get_novel_title_list(), message=None, preview=None)

@app.route('/action', methods=['POST'])
def action():
    print(request.form['action'])
    # return res_actions[request.form['action']]()

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)