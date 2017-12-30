"""
Author: Shusaku Sahashi
Date:   2017-12-24
"""

from logging import getLogger, DEBUG, Formatter, StreamHandler
import os, sys

NOVEL = 'novels'

# loggerの初期化
logger = getLogger(__name__)
logger.setLevel(DEBUG)

# handler
handler = StreamHandler()
handler.setLevel(DEBUG)

formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.propagate = True

def fitch_novel_list():
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
