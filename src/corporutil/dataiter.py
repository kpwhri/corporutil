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


def get_documents_from_source(file, columns, file_encoding='utf8', sep=',', connection_string=None, chunksize=10_000,
                              **fileargs):
    """

    :param file:
    :param columns:
    :param file_encoding:
    :param sep:
    :param connection_string:
    :param fileargs:
    :return:
    """
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
        case _:
            it = None
    if it is None:
        if 'select ' in file.stem.lower():
            it = pd.read_sql_query(file.name, con=connection_string, chunksize=chunksize, **fileargs)
        elif connection_string is not None:
            it = pd.read_sql_table(file.name, columns=columns, con=connection_string, chunksize=chunksize, **fileargs)
    yield from dociter(it, list(columns))
