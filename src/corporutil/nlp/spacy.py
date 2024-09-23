from loguru import logger

SPACY = True
try:
    import spacy
except ImportError:
    SPACY = False


def get_spacy_or_none(model=None):
    if not SPACY:
        logger.warning(f'Spacy not found: unable to use spacy models.')
        return None
    if model is not None:
        return spacy.load(model)  # fail if specified model not found
    for model in ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg', 'en_core_web_trf']:
        try:
            return spacy.load(model)
        except OSError as e:
            print(e)
    return None
