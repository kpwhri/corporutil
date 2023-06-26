from pathlib import Path

import click

from corporutil.args import retrieve_text_options, outfile_arg
from corporutil.dataiter import get_documents_from_source
from corporutil.nlp.freq import count_regex_matches


@click.command()
@retrieve_text_options
@outfile_arg
@click.option('--regex', 'regexes', multiple=True,
              help='Regular expressions to search for.')
@click.option('--lowercase/--keepcase', default=True,
              help='Keep matches cased/uncased.')
def regex_matches_for_freq(outfile: Path, regexes, lowercase=True, **kwargs):
    it = get_documents_from_source(**kwargs)
    results = count_regex_matches(it, *regexes, lowercase=lowercase)
    with open(outfile, 'w', encoding='utf8') as out:
        for pattern, cnt in results.items():
            out.write(f'{pattern}\n')
            for match, count in cnt.most_common():
                out.write(f'\t{match}\t{count}\n')


if __name__ == '__main__':
    regex_matches_for_freq()
