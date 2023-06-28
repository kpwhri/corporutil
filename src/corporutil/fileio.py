import datetime
from pathlib import Path


def get_dt():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


class FileWriter:

    def __init__(self, directory: Path, name, suffix='', ext='', mode='w', **kwargs):
        if ext and not ext.startswith('.'):
            ext = f'.{ext}'
        if suffix and not suffix.startswith('.'):
            suffix = f'.{suffix}'

        self.path = directory / f'{name}_{get_dt()}{suffix}{ext}'
        self.fh = None
        self.kwargs = kwargs
        self.mode = mode

    def __enter__(self):
        self.fh = open(self.path, self.mode, encoding='utf8', **self.kwargs)
        return self.fh

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fh is not None:
            self.fh.close()
