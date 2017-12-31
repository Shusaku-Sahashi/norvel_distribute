from flask import Flask, render_template, request, url_for
import os, random, datetime, pickle, loggger

TITLE, URL = ('必殺区分け人', 'index.html')
TEMP, NOVEL = ('temp', 'novels')

logger = loggger.getLogger(__name__)

class User:
    """
    User情報を保持するクラス
    """

    def __init__(self, candidate, novel_title):
        self._userID = self._generate_user_id()
        self._novel_title = novel_title
        self._candidates = candidate
        self._done = []
        self._conversation = []

    def fitch_next_candidate(self):
        """
        次の会話文と、previewを返す
        :return:
        """
        return (self._candidates.pop(0), self._candidates[:4]) if len(self._candidates) else (None, None)

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
    def candidates(self):
        return self._candidates

    @property
    def done(self):
        return self._done

    @property
    def conversation(self):
        return self._conversation

    @property
    def novel_title(self):
        return self._novel_title

    @candidates.setter
    def candidates(self, value):
        self._candidates = value

    @done.setter
    def done(self, value):
        self._done = value

    @conversation.setter
    def conversation(self, value):
        self._conversation = value


def persist_pkl(user):
    """
    userをpklファイルに保存する。ファイル名称はuserID.pklとする。
    :param userID:
    :return:
    """
    if not isinstance(User, user):
        raise TypeError('User クラスのみpikls化が可能です。')

    filename = user._userID + '.pkl'
    with open(os.path.join(os.curdir, [TEMP, filename]), 'wb', encoding='utf-8') as f:
        pickle.dump(user, f)

def fitch_object(userID):
    """
    userIDに指定
    :param user:
    :return:
    """
    filename = os.path.join(os.curdir, [TEMP , userID + '.pkl'])

    try:
        with open(filename, 'rb', encoding='utf-8') as f:
            return pickle.load(f)

    except FileNotFoundError:
        logger.error('"%s" が見つかりません。' % str(filename))

def fitch_novel_list():
    """
    小説のファイル名称一覧を取得する。
    :return:
    """
    return [file for _, _, files in os.walk(os.path.join(os.curdir, NOVEL)) for file in files]


def extract_dialog_from_file(file):
    """
    引数として与えられたファイル上から、「」で囲まれる会話文の取得を行う。
    :param file:
    :return:
    """
    result, temp = [], []
    ch_logger = logger.getChild('fitch_lines')
    in_talk = False

    try:
        with open(file, 'r', encoding='utf-8') as f:
            line = f.readline()

            while line:
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
        ch_logger.WORNING('{} is not found'.format(file))

    return result


def _do_init():

    user = User()


def _do_next():
    pass

def _do_set():
    pass

def _do_end():
    pass


res_actions = {
    'SELECT':   _do_init,
    'NEXT'  :   _do_next,
    'SET'   :   _do_set,
    'END'   :   _do_end
}

app = Flask(__name__)

########################以降はページルーティング#################################
@app.route('/')
def index():
    return render_template(URL, title=TITLE, novel_titles=fitch_novel_list(), message=None, preview=None)

@app.route('/action', methods=['POST'])
def action():
    return res_actions[request.form['action']]()

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)