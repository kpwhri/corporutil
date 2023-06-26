import re
from collections import defaultdict, Counter


def prep_regexes(regexes):
    return [re.compile(regex, re.I) if isinstance(regex, str) else regex for regex in regexes]


def count_regex_matches(it, *regexes, lowercase=True):
    regexes = prep_regexes(regexes)
    results = defaultdict(Counter)
    for doc in it:
        text = doc[-1]
        for regex in regexes:
            for m in regex.finditer(text):
                res = m.group().lower() if lowercase else m.group()
                results[regex.pattern][res] += 1
    return results
