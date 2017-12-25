"""
Author: Shusaku Sahashi
Date:   2017-12-24
"""

from logging import getLogger, DEBUG, Formatter, StreamHandler
import sys
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


def extract_dialog_from_file(file):
    """
    引数として与えられたファイル上から、「」で囲まれる会話文の取得を行う。
    :param file:
    :return:
    """
    result, temp = [], []
    ch_logger = logger.getChild('fitch_lines')
    Fail = None

    def _fitch_line(file):
        def _iter():
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    line = f.readline()
                    while line:
                        yield line
                        line = f.readline()

            except FileNotFoundError:
                ch_logger.error('{} is not found'.format(file))

        return _iter

    def _extract_dialog(lines):
        temp = []
        for line in lines():
            if line.endswith('」'):
                temp.append(line[0:-2])
                return ''.join(temp)
            else:
                temp.append(line)

        return Fail

    lines = _fitch_line(file)

    for line in lines():
        if line.startswith('「') and line.find('「', 1) == -1:
            if line.endswith('」'):
                result.append(line[1:-2])
            else:
                result.append(_extract_dialog(lines))

    return result
