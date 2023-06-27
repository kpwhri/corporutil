"""
Script to ensure that all files in a directory terminate in a newline. If they do not, add the newline.
"""
from pathlib import Path

import click
from loguru import logger

from corporutil.charset import get_charset


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option('--encoding', default=None,
              help='Default encoding to use, otherwise will perform detection.')
def ensure_newlines_in_directory(directories: list[Path], encoding=None):
    total_cnt = 0
    for d in directories:
        cnt = 0
        directory_encoding = encoding
        for file in d.iterdir():
            text, directory_encoding = read_file_with_encoding(file, directory_encoding)
            if not text.endswith('\n'):
                with open(file, 'w', encoding=directory_encoding) as out:
                    out.write(text + '\n')  # add missing newline
                    cnt += 1
        logger.info(f'Modified {cnt} files in {d}.')
        total_cnt += cnt
    logger.info(f'Fixed {total_cnt} files that were missing newlines.')


def read_file_with_encoding(file, directory_encoding):
    if directory_encoding:
        with open(file, encoding=directory_encoding) as fh:
            return fh.read(), directory_encoding
    return get_charset(file)


if __name__ == '__main__':
    ensure_newlines_in_directory()
