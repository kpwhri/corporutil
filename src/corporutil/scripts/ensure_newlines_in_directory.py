"""
Script to ensure that all files in a directory terminate in a newline. If they do not, add the newline.
"""
from pathlib import Path

import click
from charset_normalizer import from_path
from loguru import logger


@click.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True, path_type=Path))
def ensure_newlines_in_directory(directories: list[Path]):
    total_cnt = 0
    for d in directories:
        cnt = 0
        for file in d.iterdir():
            charset = from_path(file).best()
            text = str(charset)
            if not text.endswith('\n'):
                with open(file, 'w', encoding=charset.encoding) as out:
                    out.write(text + '\n')  # add missing newline
        logger.info(f'Modified {cnt} files in {d}.')
        total_cnt += cnt
    logger.info(f'Fixed {total_cnt} files that were missing newlines.')


if __name__ == '__main__':
    ensure_newlines_in_directory()
