from pathlib import Path

from charset_normalizer import from_path


def get_charset(file: Path):
    charset = from_path(file).best()
    encoding = 'utf8' if charset.encoding == 'ascii' else charset.encoding
    return str(charset), encoding
