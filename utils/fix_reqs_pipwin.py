# Fix pipwin deps to allow heroku installation (run from project root)
import re
from pathlib import Path


def get_broken_deps():
    cwd = Path.cwd()
    reqs_file = cwd.joinpath('requirements.txt')
    with open(reqs_file, 'r') as reqs_txt:
        lines = reqs_txt.readlines()
        for lnum in range(len(lines)):
            split = lines[lnum].split(' @ ')
            if len(split) >= 2:
                wheel_name = split[-1].split('-')
                fixed_dep = split[0] + '==' + wheel_name[1].split('%')[0] + '\n'
                lines[lnum] = fixed_dep
    print(lines)
    with open(reqs_file, 'w') as reqs_txt:
        reqs_txt.writelines(lines)


if __name__ == '__main__':
    get_broken_deps()