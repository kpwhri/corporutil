import json
from pathlib import Path

import click

from corporutil.args import retrieve_text_options, outfile_arg
from corporutil.dataiter import get_documents_from_source
from corporutil.nlp.spacy import get_spacy_or_none
from corporutil.stats import build_stats


@click.command()
@retrieve_text_options
@outfile_arg
@click.option('--spacy-model', default=None,
              help='Specify spacy model')
@click.option('--patient-col', type=int, default=None,
              help='Specify patient column index.')
@click.option('--encounter-col', type=int, default=None,
              help='Specify patient column index.')
@click.option('--text-col', type=int, default=-1,
              help='Specify patient column index.')
def build_corpus_stats(outfile: Path, patient_col, encounter_col, text_col=-1, spacy_model=None, **fileargs):
    it = get_documents_from_source(**fileargs)
    nlp = get_spacy_or_none(spacy_model)
    results = build_stats(it, text_col=text_col, enc_col=encounter_col, pt_col=patient_col, nlp=nlp)
    with open(outfile, 'w', encoding='utf8') as fh:
        json.dump(results, fh, indent=2)


if __name__ == '__main__':
    build_corpus_stats()
