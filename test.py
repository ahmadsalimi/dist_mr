import glob
import os

from golden_standard import standard_count


OUT_DIR = 'out'


def parse_line(line):
    word, count = line.split()
    count = int(count)
    return word, count


def test():
    real_counts = standard_count()
    os.system('./dist_mr.sh -N 6 -M 4')
    for filename in glob.glob(f'{OUT_DIR}/*'):
        with open(filename) as file:
            for word, count in map(parse_line, file.readlines()):
                assert word in real_counts, f'{word} is not in real words'
                assert count == real_counts.pop(word)
