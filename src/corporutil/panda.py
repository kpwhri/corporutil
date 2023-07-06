import random
from pathlib import Path

import pandas as pd


def build_counts(df, colname='studyid', axis=None):
    return df.groupby(colname).count().reset_index().groupby('count')[colname].count().plot(ax=axis)


def select_studyid(df: pd.DataFrame, colname='studyid', train_pct=0.9, seed=None, outdir=None):
    """

    :param seed: seed to set for random.seed
    :param outdir: output path
    :param train_pct: percent of `colname`/studyids to include in training sample
    :param df: pd.DataFrame with a column named `colname`, each row should represent a note
    :param colname: column name with studyid
    :return:
    """
    if outdir is None:
        outdir = Path('.')
    outdir.mkdir(exist_ok=True)
    n_notes = df.shape[0]
    studyids = list(df[colname].unique())
    n_studyids = len(studyids)
    random.seed(seed or studyids[int(n_studyids / 2)])
    train_sample = set(random.sample(studyids, int(len(studyids) * train_pct)))
    test_sample = set(studyids) - train_sample
    # get datasets of the samples
    df['count'] = 1
    train_df = df[df.studyid.isin(train_sample)]
    test_df = df[df.studyid.isin(test_sample)]
    # summarize notes at studyid-level
    stats = ['min', 'mean', 'std', 'median', 'max', 'sum']
    tr_cnt_df = train_df.groupby(colname).count().agg(stats)
    te_cnt_df = test_df.groupby(colname).count().agg(stats)
    all_cnt_df = df.groupby(colname).count().agg(stats)
    cnt_df = pd.merge(
        pd.merge(tr_cnt_df, te_cnt_df, left_index=True, right_index=True),
        all_cnt_df,
        left_index=True,
        right_index=True,
    )
    cnt_df.columns = ['train', 'test', 'all']
    cnt_df.to_csv(outdir / f'train_test_distributions.csv')
    # create chart with counts of notes by studyid
    ax = build_counts(test_df, colname=colname,
                      axis=build_counts(train_df, colname=colname,
                                        axis=build_counts(df, colname=colname)))
    ax.get_figure().savefig(outdir / f'train_test_distribution.png')
    # export to file
    with open(outdir / 'train_studyids_20230705.txt', 'w', encoding='utf8') as out:
        out.write('\n'.join(train_sample))
    with open(outdir / 'test_studyids_20230705.txt', 'w', encoding='utf8') as out:
        out.write('\n'.join(test_sample))
