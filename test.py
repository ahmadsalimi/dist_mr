import glob
import os

from golden_standard import standard_count


OUT_DIR = 'out'


def parse_line(line):
    word, count = line.split()
    count = int(count)
    return word, count


def run_dist_mr():
    os.system('python worker.py --name 1 &')
    os.system('python worker.py --name 2 &')
    os.system('python worker.py --name 3 &')
    os.system('python worker.py --name 4 &')
    os.system('python driver.py -N 6 -M 4')


def test():
    real_counts = standard_count()
    run_dist_mr()
    for filename in glob.glob(f'{OUT_DIR}/*'):
        with open(filename) as file:
            for word, count in map(parse_line, file.readlines()):
                assert word in real_counts, f'{word} is not in real words'
                assert count == real_counts.pop(word)

    # the dictionary must be empty
    assert not real_counts
