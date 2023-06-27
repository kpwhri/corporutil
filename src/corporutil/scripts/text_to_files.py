"""
A script to build the initial file structure required by MetaMapLite.

This file will build 1 or more directories containing files with the name
 f'{note_id}.txt' and containing only the note's complete text.
"""
from pathlib import Path

import click
from loguru import logger

from corporutil.args import retrieve_text_options, outdir_arg
from corporutil.dataiter import get_documents_from_source


@click.command()
@retrieve_text_options
@outdir_arg
@click.option('--n-dirs', default=1, type=int,
              help='Number of directories to create.')
@click.option('--text-extension', default='.txt',
              help='Extension of text files to be created.')
@click.option('--text-encoding', default='utf8',
              help='Encoding for writing text files.')
@click.option('--ensure-newline', is_flag=True, default=False,
              help='Ensure that each text file has a newline;'
                   ' certain programs (e.g., Metamap) will fail without newlines.')
@click.option('--force', is_flag=True, default=False)
def text_from_file(outdir: Path, n_dirs=1, text_extension='.txt', text_encoding='utf8', force=False,
                   ensure_newline=False, **fileargs):
    it = get_documents_from_source(**fileargs)
    build_files(it, outdir=outdir, n_dirs=n_dirs, text_extension=text_extension, text_encoding=text_encoding,
                force=force)


def build_files(text_gen, outdir: Path, n_dirs=1, text_extension='.txt', text_encoding='utf8',
                ensure_newline=False, force=False):
    """
    Write files to directory from generator outputting (note_id, text).
        A filelist will also be created for each outdirectory.
    :param ensure_newline: ensure that file ends with newline before writing
    :param force: force overwriting existing directory
    :param text_gen:
    :param outdir:
    :param n_dirs:
    :param text_extension:
    :param text_encoding:
    :return:
    """
    if outdir is None:
        outdir = Path('.')
    logger.info(f'Writing files to: {outdir}.')
    outdirs = [outdir / f'notes{i}' if n_dirs > 1 else outdir / f'notes' for i in range(n_dirs)]
    for d in outdirs:
        d.mkdir(exist_ok=force, parents=True)
    filelists = [open(outdir / f'filelist{i}.txt', 'w') if n_dirs > 1
                 else open(outdir / f'filelist.txt', 'w')
                 for i in range(n_dirs)]
    for i, (note_id, text) in enumerate(text_gen):
        outfile = outdirs[i % n_dirs] / f'{note_id}{text_extension}'
        if ensure_newline and not text.endswith('\n'):  # ensure that every text files ends in a newline
            text += '\n'
        with open(outfile, 'w', encoding=text_encoding, errors='replace') as out:
            out.write(text)
        filelists[i % n_dirs].write(f'{outfile.absolute()}\n')
    for fl in filelists:
        fl.close()


if __name__ == '__main__':
    text_from_file()
