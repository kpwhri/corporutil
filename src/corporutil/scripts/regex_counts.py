import csv
from pathlib import Path

import click

from corporutil.args import retrieve_text_options, outdir_arg
from corporutil.dataiter import get_documents_from_source
from corporutil.fileio import FileWriter
from corporutil.nlp.regex import find_regexes_in_corpus, prep_regexes


@click.command()
@retrieve_text_options
@outdir_arg
@click.option('--regex', 'regexes', multiple=True,
              help='Regex to search for. To give the regex a name, use NAME==REGEX.')
def compute_regex_counts(outdir: Path, regexes, **fileargs):
    it = get_documents_from_source(**fileargs)
    regexes = list(prep_regexes(regexes))
    names = [n for n, r in regexes]
    with FileWriter(outdir, 'regex_counts', 'csv', newline='') as fh:
        wrote_header = False
        writer = csv.writer(fh)
        for meta, counter in find_regexes_in_corpus(it, regexes):
            if not wrote_header:
                writer.writerow([f'meta{i}' for i in range(len(meta))] + names)
                wrote_header = True
            writer.writerow(meta + [counter[name] for name in names])


if __name__ == '__main__':
    compute_regex_counts()
