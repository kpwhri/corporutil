import json

import pandas as pd
from pathlib import Path


def dociter(it, columns: list):
    """

    :param it: iterator of dataframe
    :param columns: list of columns to return
    :return:
    """
    if it is None:
        return
    for df in it:
        for row in df[columns].itertuples(index=False, name=None):
            yield row


def diriter(path: Path, encoding='utf8', glob_pattern='*', **kwargs):
    for file in path.glob(glob_pattern):
        with open(file, encoding=encoding) as fh:
            text = fh.read()
        yield file.stem, text


def compile_fileargs(fileargs):
    return {key: value for arg in fileargs or [] for key, value in arg.split('==')}


def get_documents_from_source(file: Path, columns, file_encoding='utf8', sep=',', connection_string=None,
                              chunksize=10_000, glob='*', **fileargs):
    """

    :param chunksize:
    :param glob:
    :param file:
    :param columns:
    :param file_encoding:
    :param sep:
    :param connection_string:
    :param fileargs:
    :return:
    """
    if 'fileargs' in fileargs:
        fileargs = compile_fileargs(fileargs['fileargs'])
    if file.is_dir():  # corpus of files
        yield from diriter(file, file_encoding, glob, **fileargs)
        return
    it = None
    match file.suffix:
        case '.csv':
            it = pd.read_csv(file, **{
                'sep': sep, 'usecols': columns, 'chunksize': chunksize, 'encoding': file_encoding,
            }, **fileargs)
        case '.sas7bdat' | '.xport':
            it = pd.read_sas(file, **{
                'encoding': file_encoding, 'chunksize': chunksize,
            }, **fileargs)
        case '.sql':  # interpret as a tablename
            it = pd.read_sql_table(file.stem, columns=columns, con=connection_string,
                                   chunksize=chunksize, **fileargs)
        case '.jsonl':  # jsonlines
            with open(file, encoding=file_encoding) as fh:
                for line in fh:
                    data = json.loads(line.strip())
                    yield [data[col] for col in columns]
            return
    if it is None:
        if 'select ' in file.stem.lower():
            it = pd.read_sql_query(file.name, con=connection_string, chunksize=chunksize, **fileargs)
        elif connection_string is not None:
            it = pd.read_sql_table(file.name, columns=columns, con=connection_string, chunksize=chunksize, **fileargs)
    yield from dociter(it, list(columns))
