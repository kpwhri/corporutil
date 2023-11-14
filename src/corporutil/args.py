from pathlib import Path

import click


def retrieve_text_options(f):
    return click.argument(
        'file', type=click.Path(path_type=Path), default=None
    )(
        click.option(
            '--column', 'columns', multiple=True, type=str,
            help='Name of columns. If including a lot of metadata and text, provide the'
                 ' unique id as element t 0 (first) and the text as element -1 (last).'
        )(
            click.option(
                '--file-encoding', default='utf8', help='Encoding for source CSV file.'
            )(
                click.option(
                    '--sep', default=',', help='Column delimiter for csv file.'
                )(
                    click.option(
                        '--connection-string', default=None,
                        help='Connection string if using database table/query.'
                    )(
                        click.option('--filearg', 'fileargs', multiple=True,
                                     help='Any additional arguments to pass to relevant pandas read_*;'
                                          ' should be of form key==value.')
                        (click.option('--glob', 'glob', default='*',
                                      help='For directory, specify glob pattern to select relevant files')(f))
                    )
                )
            )
        )
    )


def outdir_arg(f):
    return click.option('--outdir', type=click.Path(file_okay=False, path_type=Path), default=None,
                        help='Directory to create subfolders and filelists.')(f)


def outfile_arg(f):
    return click.option('--outfile', type=click.Path(dir_okay=False, path_type=Path), default=None,
                        help='Output file.')(f)
