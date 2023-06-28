"""
Create stats
"""
import statistics
from collections import defaultdict
from dataclasses import dataclass


class Patient:

    def __init__(self):
        self.encounters = set()
        self.notes = []

    @property
    def n_encounters(self):
        return len(self.encounters)

    def add(self, encounter, docstat):
        self.encounters.add(encounter)
        self.notes.append(docstat)

    def __getattr__(self, item):
        return sum(getattr(note, item) for note in self.notes)


class Encounter:

    def __init__(self):
        self.notes = []

    def add(self, docstat):
        self.notes.append(docstat)

    def __getattr__(self, item):
        return sum(getattr(note, item) for note in self.notes)


@dataclass(slots=True)
class DocStats:
    n_characters: int = 0
    n_nonspace: int = 0  # number of non-space charactesr
    n_alpha: int = 0
    n_numeric: int = 0
    n_tokens: int = 0  # space-separated units
    n_words: int = 0  # space-separated alpha-only units
    n_content_words: int = 0
    n_sentences: int = 0
    n_notes: int = 1

    def __add__(self, other):
        return DocStats(
            self.n_characters + other.n_characters,
            self.n_nonspace + other.n_nonspace,
            self.n_alpha + other.n_alpha,
            self.n_numeric + other.n_numeric,
            self.n_tokens + other.n_tokens,
            self.n_words + other.n_words,
            self.n_content_words + other.n_content_words,
            self.n_sentences + other.n_sentences,
            self.n_notes + other.n_notes,
        )


def build(text, nlp=None):
    """

    :param text:
    :param nlp: spacy model
    :return:
    """
    n_characters = len(text)
    n_nonspace = sum(map(str.isspace, text))
    n_alpha = sum(map(str.isalpha, text))
    n_numeric = sum(map(str.isdigit, text))
    if nlp:
        doc = nlp(text)
        n_tokens = len(doc)
        n_words = len([token for token in doc if token.is_alpha])
        n_content_words = len([token for token in doc if token.is_alpha and not token.is_stop])
        n_sentences = len(list(doc.sents))
    else:
        n_tokens = len(text.split())
        n_words = len([x for x in text.split() if str.isalpha(x)])
        n_content_words = len([x for x in text.split() if str.isalpha(x) and x.lower() not in {
            'a', 'the', 'an', 'to', 'of', 'and', 'is', 'are', 'am', 'in', 'that', 'have', 'has', 'i', 'it', 'for',
        }])
        n_sentences = len(text.split('. '))
    return DocStats(n_characters, n_nonspace, n_alpha, n_numeric, n_tokens, n_words, n_content_words, n_sentences, 1)


def get_stat(lst):
    """Build a row of min,mode,med,mean,max"""
    if not lst:
        return 0
    return {
        'min': min(lst),
        'mode': statistics.mode(lst),
        'median': statistics.median(lst),
        'mean': statistics.mean(lst),
        'max': max(lst)
    }


def build_stats(it, text_col=-1, enc_col=None, pt_col=None, nlp=None):
    data = defaultdict(lambda: defaultdict(list))  # patient -> encounter -> doc -> DocStats
    if enc_col and pt_col:
        pts, encs, docs = build_stats_all(((d[pt_col], d[enc_col], d[text_col]) for d in it), nlp=nlp)
    elif pt_col:
        pts, encs, docs = build_stats_all(((d[pt_col], 0, d[text_col]) for d in it), nlp=nlp)
    else:  # doc only
        pts, encs, docs = build_stats_all(((0, 0, d[text_col]) for d in it), nlp=nlp)
    # get statistics
    stats = {
        'totals': {
            'n_patients': len(pts),
            'n_encounters': len(encs),
            'n_notes': len(docs),
        },
        'range': {
            'notes_per_patient': get_stat([pt.n_notes for pt in pts.values()]),
            'encounters_per_patient': get_stat([len(pt.encounters) for pt in pts.values()]),
            'notes_per_encounter': get_stat([enc.n_notes for enc in encs.values()]),
        }
    }
    for attr in DocStats.__slots__:
        stats['range'][f'{attr}_per_note'] = get_stat([getattr(doc, attr) for doc in docs])
        stats['range'][f'{attr}_per_patient'] = get_stat([getattr(pt, attr) for pt in pts.values()])
        stats['range'][f'{attr}_per_encounter'] = get_stat([getattr(enc, attr) for enc in encs.values()])
    return stats


def build_stats_all(it, nlp):
    pts = defaultdict(Patient)
    encs = defaultdict(Encounter)
    docs = []
    for pt, enc, text in it:
        doc = build(text, nlp=nlp)
        if pt:
            pts[pt].add(enc, doc)
        if enc:
            encs[enc].add(doc)
        docs.append(doc)
    return pts, encs, docs
