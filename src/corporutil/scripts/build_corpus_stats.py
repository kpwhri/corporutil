import csv
import json
from pathlib import Path

import click

from corporutil.args import retrieve_text_options, outdir_arg
from corporutil.dataiter import get_documents_from_source
from corporutil.fileio import FileWriter
from corporutil.nlp.spacy import get_spacy_or_none
from corporutil.stats import build_stats, build


@click.command()
@retrieve_text_options
@outdir_arg
@click.option('--spacy-model', default=None,
              help='Specify spacy model')
@click.option('--patient-col', type=int, default=None,
              help='Specify patient column index.')
@click.option('--encounter-col', type=int, default=None,
              help='Specify encounter column index.')
@click.option('--text-col', type=int, default=-1,
              help='Specify note text column index.')
@click.option('--kind', default='json',
              help='Specify json or csv output types.')
def build_corpus_stats(outdir: Path, patient_col, encounter_col, text_col=-1, spacy_model=None, kind='json',
                       **fileargs):
    it = get_documents_from_source(**fileargs)
    nlp = get_spacy_or_none(spacy_model)
    if kind == 'json':
        build_corpus_stats_json(it, text_col, encounter_col, patient_col, nlp, outdir)
    elif kind == 'csv':
        build_corpus_stats_csv(it, nlp, outdir)
    else:
        raise ValueError(f'Unrecognized kind: {kind}')


def build_corpus_stats_json(it, text_col, encounter_col, patient_col, nlp, outdir):
    results = build_stats(it, text_col=text_col, enc_col=encounter_col, pt_col=patient_col, nlp=nlp)
    with FileWriter(outdir, 'summary', ext='.json') as fh:
        json.dump(results, fh, indent=2)


def build_corpus_stats_csv(it, nlp, outdir):
    with FileWriter(outdir, 'summary', ext='.csv', newline='') as fh:
        writer = csv.writer(fh)
        for i, (*meta, text) in enumerate(it):
            docstats = build(text, nlp=nlp)
            if i == 0:
                writer.writerow([f'meta{i}' for i in range(len(meta))] + list(docstats.__slots__))
            writer.writerow(meta + [getattr(docstats, v) for v in docstats.__slots__])


if __name__ == '__main__':
    build_corpus_stats()
