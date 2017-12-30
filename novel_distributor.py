from flask import Flask, render_template, request, url_for
import os
import methods as m

TITLE, URL =('必殺区分け人', 'index.html')
NOVEL_DIR = os.path.join(os.path.curdir, 'novels')
userInfo = None

class User:

    def __init__(self, novel, dialogs):
        self.dialogs = dialogs
        self.novel = novel

    def fitch_next_dialog(self):
        return self.dialogs.pop(0), self.dialogs[:4]


def _do_init():
    novel = request.form['novel_list']
    dialogs = m.extract_dialog_from_file(os.path.join(NOVEL_DIR, novel))
    userInfo = User(novel, dialogs)
    question, preview = userInfo.fitch_next_dialog()
    return render_template(URL, title=TITLE, novel_titles=userInfo.novel, message={'question': question}, preview=preview)


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
    print(m.fitch_novel_list())
    return render_template(URL, title=TITLE, novel_titles=m.fitch_novel_list(), message=None, preview=None)

@app.route('/action', methods=['POST'])
def action():
    print(request.form['novel_list'])
    return res_actions[request.form['action']]()

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)