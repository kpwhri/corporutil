"""
A script to build the initial file structure required by MetaMapLite.

This file will build 1 or more directories containing files with the name
 f'{note_id}.txt' and containing only the note's complete text.
"""
from pathlib import Path

import click
from loguru import logger

from corporutil.dataiter import get_documents_from_source



@click.command()
@click.argument('file', type=click.Path(dir_okay=False, path_type=Path), default=None)
@click.option('--column', 'columns', multiple=True, type=str,
              help='Name of columns. If including a lot of metadata and text, provide the unique id as'
                   '  element 0 (first) and the text as element -1 (last).')
@click.option('--outdir', type=click.Path(file_okay=False, path_type=Path), default=None,
              help='Directory to create subfolders and filelists.')
@click.option('--n-dirs', default=1, type=int,
              help='Number of directories to create.')
@click.option('--text-extension', default='.txt',
              help='Extension of text files to be created.')
@click.option('--text-encoding', default='utf8',
              help='Encoding for writing text files.')
@click.option('--file-encoding', default='utf8',
              help='Encoding for source CSV file.')
@click.option('--sep', default=',',
              help='Column delimiter for csv file.')
@click.option('--connection-string', default=None,
              help='Connection string if using database table/query.')
@click.option('--filearg', 'fileargs', multiple=True,
              help='Any additional arguments to pass to relevant pandas read_*; should be of form key==value.')
@click.option('--force', is_flag=True, default=False)
def text_from_file(file, columns, outdir: Path, n_dirs=1, text_extension='.txt', connection_string=None,
                   text_encoding='utf8', file_encoding='utf8', sep=',', fileargs=None, force=False):
    fileargs = {key: value for arg in fileargs or [] for key, value in arg.split('==')}
    it = get_documents_from_source(file, columns, file_encoding, sep, connection_string, **fileargs)
    build_files(it, outdir=outdir, n_dirs=n_dirs, text_extension=text_extension, text_encoding=text_encoding,
                force=force)


def build_files(text_gen, outdir: Path, n_dirs=1, text_extension='.txt', text_encoding='utf8', force=False):
    """
    Write files to directory from generator outputting (note_id, text).
        A filelist will also be created for each outdirectory.
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
        with open(outfile, 'w', encoding=text_encoding, errors='replace') as out:
            out.write(text)
        filelists[i % n_dirs].write(f'{outfile.absolute()}\n')
    for fl in filelists:
        fl.close()


if __name__ == '__main__':
    text_from_file()
