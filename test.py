import pickle, os

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

file = os.path.join(os.curdir, 'temp', '9A81H2wyKK.pkl')

with open(file,'rb') as f:
    user = pickle.load(f)

print(user.userID)