import re
from collections import Counter


def prep_regexes(regexes, flags=re.I):
    for regex in regexes:
        if isinstance(regex, str):
            if '==' in regex:
                name, regex = regex.split('==')
            else:
                name = regex
            yield name, re.compile(regex, flags)
        elif len(regex) == 2:
            yield regex
        else:
            yield None, regex


def find_regexes_in_corpus(it, regexes):
    all_counts = Counter()
    for *meta, text in it:
        curr_counts = Counter()
        for name, regex in regexes:
            for _ in regex.finditer(text):
                curr_counts[name] += 1
        yield meta, curr_counts
        all_counts += curr_counts
