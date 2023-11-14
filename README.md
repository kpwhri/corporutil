
# Corporutil

Utility functions for working with a text corpus.

## Installation

* Python 3.9+
  * Install requirements: `pip install -r requirements.txt`
* Currently, there is no install script, so:
  * Need to add `src` directory to `PYTHONPATH` before running the following
    * Powershell: `$env:PYTHONPATH='[PATH]/corporutil/src'`
    * bash: `export PYTHONPATH='[PATH]/corporutil/src'`

## Usage

### Get Counts of Regular Expressions

```shell
python /path/to/src/corporutil/scripts/regex_counts.py
corpus  # see definitions below
--outdir
stats  # output directory
--regex  # regular expressions to include
anaphylaxis==\banaph\w*
--regex
epinephrine==\bepine\w*
```

## Definitions

### Corpus

A corpus can be read in several different ways:

1. Directory of files
   * Path to directory
   * Specify `--glob *.txt` if wanting only a subset of the files in the directory
2. CSV file
3. SAS7BDAT file
4. SQL Table
   * Specify tablename with `.sql` extension (e.g., `corpus.sql`)
   * Specify query like `'select id, text from corpus'`


#### Common Options

* `--column`: (multiple okay) Specify names of columns (e.g., when pulling from sql; the text column should be the last specified)
* `--file-encoding`: Defaults to 'utf8'
* `--sep`: Separator for a CSV file
* `--connection-string`: sqlalchemy-style connection string for database/query
* `--filearg`: (multiple okay) Additional arguments to supply (e.g., to `pandas.read_*`) in form of `--filearg key1==value1`
* `--glob`: Specify glob pattern for collecting files from a directory (e.g., '*.txt' for all files ending in txt; defaults to '*')

When using 'multiple okay', the flag must be specified for each (e.g., `--column id --column date --column text`).