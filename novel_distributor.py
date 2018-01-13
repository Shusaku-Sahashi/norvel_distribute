#! coding: utf-8
from flask import Flask, render_template, request, make_response
import os, random, datetime, pickle, loggger, MeCab

TITLE, URL = ('必殺区分け人', 'index.html')
TEMP, NOVEL = ('temp', 'novels')

logger = loggger.getLogger(__name__)

class User:
    """
    User情報を保持するクラス
    """

    def __init__(self, novel_title, novel):
        self._userID = self._generate_user_id()
        self._novel_title = novel_title
        self._novel = novel
        self._done = []
        self._conversation = []
        self._question = None
        self._answer = None
        self._preview = None

    def fitch_next_candidate(self):
        """
        次の会話文と、previewを返す
        :return:
        """
        return (self._novel.pop(0), self._novel[:4]) if len(self._novel) else (None, None)

    def _generate_user_id(self):
        """
        英数字から10桁のランダムな文字列を生成する。
        :return:
        """
        SEEDS = '1234567890abcdefghigklmopqrstuvwsxyzABCDEFGHIJKLMNOPQRSTUVWYZ'
        rand = random.Random(datetime.datetime.now())
        return ''.join([n for _ in range(10) for n in rand.choice(SEEDS)])

    @property
    def userID(self):
        return self._userID

    @property
    def novel(self):
        return self._novel

    @property
    def done(self):
        return self._done.pop()

    @property
    def conversation(self):
        return self._conversation

    @property
    def novel_title(self):
        return self._novel_title

    @property
    def question(self):
        return self._question

    @property
    def answer(self):
        return self._answer

    @property
    def preview(self):
        return self._preview

    @novel.setter
    def novel(self, value):
        self._novel = value

    @done.setter
    def done(self, value):
        self._done.append(value)

    @conversation.setter
    def conversation(self, value):
        self._conversation.append(value)

    @question.setter
    def question(self, value):
        self._question = value

    @answer.setter
    def answer(self, value):
        self._answer = value

    @preview.setter
    def preview(self, value):
        self._preview = value

def persist_pkl(user):
    """
    userをpklファイルに保存する。ファイル名称はuserID.pklとする。
    :param userID:
    :return:
    """
    if not isinstance(user, User):
        raise TypeError('User クラスのみpikls化が可能です。')

    filename = user._userID + '.pkl'
    with open(os.path.join(os.curdir, TEMP, filename), 'wb') as f:
        pickle.dump(user, f)

def load_pkl(userID):
    """
    userIDに指定
    :param user:
    :return:
    """
    filename = os.path.join(os.curdir, TEMP, '{}.pkl'.format(userID))

    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)

    except FileNotFoundError:
        logger.error('"%s" が見つかりません。' % str(filename))

def fitch_novel_list():
    """
    小説のファイル名称一覧を取得する。
    :return:
    """
    return [file for _, _, files in os.walk(os.path.join(os.curdir, NOVEL)) for file in files]


def extract_dialog_from_file(novel_title):
    """
    引数として与えられたファイル上から、「」で囲まれる会話文の取得を行う。
    :param file:
    :return:
    """
    ch_logger = logger.getChild('fitch_lines')

    result, temp = [], []
    in_talk = False
    file = os.path.join(os.curdir, NOVEL, novel_title)

    try:
        with open(file, 'r', encoding='utf-8') as f:
            line = f.readline()

            while line:
                # TODO \u3000の全角空白を除く
                if line.startswith('「') and line.find('「', 1) == -1:
                    if line.endswith('」\n'):
                        '一文で会話が終了'
                        result.append(line[1:-2])
                    else:
                        '一文以上の会話が開始'
                        temp.append(line[1:-1])
                        in_talk = True
                elif in_talk:
                    if line.endswith('」\n'):
                        '一文以上の会話が終了'
                        temp.append(line[:-2])
                        result.append(''.join(temp))
                        in_talk, temp = False, []
                    else:
                        '一文以上の会話が継続中'
                        temp.append(line[:-1])

                line = f.readline()

    except FileNotFoundError:
        ch_logger.error('{} is not found'.format(file))

    return result

def get_userInfo(novel_title, question, answer, preview):
    userInfo = {
        'novel_title'   :   novel_title,
        'question'      :   question,
        'answer'        :   answer,
        'preview'       :   preview
    }
    return userInfo

def _resume():
    """
    COOKIEを元に前回のページを表示
    :return:
    """
    # cookieからuserIDを取得
    user = load_pkl(request.cookies.get('userID'))

    # webに渡すuserInfoの作成
    userInfo = get_userInfo(user.novel_title, user.question, user.answer, user.preview)

    return render_template(URL, novel_list=None, userInfo=userInfo)

def _show_init_page():
    """
    初期ページの表示
    :return:
    """
    userInfo = get_userInfo(None, None, None, None)
    return render_template(URL, novel_list=fitch_novel_list(), userInfo=userInfo)

def _initialize():
    """
    SELECTボタンが押下された時の処理
    :return:
    """
    novel_title = request.form['novel_list']
    novel = extract_dialog_from_file(novel_title)

    # Userクラスの作成とPickle化を実施
    user = User(novel_title=novel_title, novel=novel)
    persist_pkl(user)

    # 質問文の候補とpreviewの取得
    user.question, user.preview = question, preview = user.fitch_next_candidate()

    # webに渡すユーザ情報の作成
    userInfo = get_userInfo(novel_title, question, None, preview)

    # クッキー情報にユーザIDを保持
    resp = make_response(render_template(URL, novel_list=None, userInfo=userInfo))
    resp.set_cookie('userID', value=user.userID, max_age=60 * 60 * 24 * 30) # default_30days

    return resp


def _show_next_candidate():
    """
    NEXTボタンが押下された時の処理
    :return:
    """
    # pklの取得
    user = load_pkl(request.cookies.get('userID'))

    # Userクラス内のパラメータを書き換える。
    next_letter, preview = user.fitch_next_candidate()
    user.preview = preview

    if user.answer is None:
        user.done = user.question
        user.question = next_letter
    else:
        user.done = user.answer
        user.answer = next_letter

    # Userクラスの保存
    persist_pkl(user)

    # webに渡すuserInfoの作成
    userInfo = get_userInfo(user.novel_title, user.question, user.answer, user.preview)

    return render_template(URL, novel_list=None, userInfo=userInfo)


def _persist_dialog():
    """
    会話文を『質問文』もしくは、『解答文』として記録する。
    :return:
    """
    # cookieからuserIDを取得
    user = load_pkl(request.cookies.get('userID'))

    if user.answer:
        user.conversation = (user.question, user.answer)
        user.question, user.answer = None, None
    else:
        user.answer = 'NEXT'

    # Userクラスの保存
    persist_pkl(user)

    return _show_next_candidate()

def _end_application():
    """
    アプリケージョンの終了を行う。
    アプリケーションを終了する際に以下の処理を実施する。
    ①会話文に対してMecabを実施する。
    ②そのファイルを元にoutputとinputを作成する。
    :return:
    """
    # cookieからuserIDを取得
    user = load_pkl(request.cookies.get('userID'))

    mt = MeCab.Tagger("-Owakati")

    def make_output_file_name(filename):
        return os.path.join(os.path.curdir, 'out', '{}_{}.txt'.format(user.userID, filename))

    with open(make_output_file_name('output'), 'w', encoding='utf-8') as f_output, open(make_output_file_name('input'), 'w', encoding='utf-8') as f_input:
        for question, answer in user.conversation:
            f_input.writelines(mt.parse(question))
            f_output.writelines(mt.parse(answer))

    resp = make_response(_show_init_page())
    resp.set_cookie('userID', expires=0)

    tempfile = os.path.join(os.path.curdir, 'temp', '{}.pkl'.format(user.userID))
    if os.path.exists(tempfile):
        os.remove(tempfile)

    return resp


res_actions = {
    'SELECT':   _initialize,
    'NEXT'  :   _show_next_candidate,
    'SET'   :   _persist_dialog,
    'END'   :   _end_application
}

app = Flask(__name__)

########################以降はページルーティング#################################
@app.route('/')
def index():
    if request.cookies.get('userID'):
        return _resume()
    else:
        return _show_init_page()

@app.route('/action', methods=['POST', 'GET'])
def action():
    return res_actions[request.form['action']]()

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)