import glob
from typing import Dict

from reducer import WordCounter


INPUTS_DIR = 'inputs'


def standard_count() -> Dict[str, int]:
    wc = WordCounter()

    for filename in glob.glob(f'{INPUTS_DIR}/*'):
        with open(filename) as file:
            text: str = file.read()
            for word in text.split():
                wc.count(word)
    return wc._dict
