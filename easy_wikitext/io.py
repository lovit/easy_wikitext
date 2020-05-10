import os
import time
import requests
import zipfile
from collections import namedtuple


Paragraph = namedtuple('Paragraph', 'doc_idx paragraph_idx title texts')

AVAILABLE_NAMES = {
    'wikitext-2': 'https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip',
    'wikitext-103': 'https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip'
}

LICENSE = """
This package provides only easy-download and easy-load token-level wikitext dataset.
Please visit https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset first.

The `wikitext` dataset follows `Creative_Commons_Attribution-ShareAlike_3.0_Unported_License`.
If you wonder what is the LICENSE, please visit https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License firts.

The wonderful site, `paperwithcode.com` provides which paper uses the dataset and how the performance are based on perplexity.
- https://paperswithcode.com/sota/language-modelling-on-wikitext-2
- https://paperswithcode.com/sota/language-modelling-on-wikitext-103
"""

AVAILABLE_DATA_TYPE = {'train', 'valid', 'test'}

installpath = os.path.abspath(os.path.dirname(__file__))


def fetch(name='wikitext-2'):
    check_install(name)


def load(name='wikitext-2', data_type=None):
    """
    Args:
        name: str
            Wikitext name. One of ['wikitext-2', 'wikitext-103']
            If the dataset is not installed, it first download it.
        data_type: None or str
            If the `data_type` is None, `load` returns dict of paragraph list
            If the `data_type` is one of ['train', 'valid', 'test'], `load` returns
            list of Paragraph.
    Returns:
        texts: list of Paragraph or dict of paragraph list
    """
    train, valid, test = check_install(name)
    if data_type is None:
        return {'train': _load(train), 'valid': _load(valid), 'test': _load(test)}
    if data_type not in AVAILABLE_DATA_TYPE:
        raise ValueError(f'`data_type` must be one of {AVAILABLE_DATA_TYPE}')
    return _load({'train': train, 'valid': valid, 'test': test}[data_type])


def _load(path):
    def reset():
        return None, []

    paragraphs = []
    doc_idx, paragraph_idx = -1, -1
    doc_title, paragraph_title = {}, {}
    with open(path, encoding='utf-8') as f:
        title, texts = reset()
        for i, line in enumerate(f):
            line = line.strip()
            if not line and title and texts:
                if level == 1:
                    doc_idx += 1
                paragraph_idx += 1
                paragraphs.append(
                    Paragraph(doc_idx, paragraph_idx, title, texts)
                )
                title, texts = reset()
                continue
            if line[:2] == '= ':
                level = int(line.count('=') / 2)
                title = line.replace('=', '').strip()
            elif line:
                texts.append(line)
    return paragraphs


def check_name(name):
    if name not in AVAILABLE_NAMES:
        raise ValueError(f'Available `name` is one of {AVAILABLE_NAMES.keys()}')
    print(LICENSE)


def check_install(name):
    check_name(name)
    zippath = f'{installpath}/data/{name}-v1.zip'
    textpaths = [f'{installpath}/data/{name}/wiki.{type}.tokens' for type in ['train', 'valid', 'test']]
    train, valid, test = textpaths

    all_exists = True
    for textpath in textpaths:
        if not os.path.exists(textpath):
            all_exists = False

    if all_exists:
        return train, valid, test

    print(f'{name} is not installed yet')
    if not os.path.exists(zippath):
        url = AVAILABLE_NAMES[name]
        print(f'begin downloading {name}.zip from {url}')
        download_a_file(url, zippath)
    if os.path.exists(zippath):
        print(f'unzip the downloaded {name}.zip file')
        unzip(zippath, f'{installpath}/data/')

    return train, valid, test


def download_a_file(url, fname):
    """
    Arguments
    --------
    url : stri
        URL address of file to be downloaded
    fname : str
        Download file address

    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    fname = os.path.abspath(fname)
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # If you do not set user-agent, downloading from url is stalled.
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}

    try:
        r = requests.get(url, stream=True, headers=headers)
        total_length = int(r.headers.get('content-length'))
        n = int(total_length / 1024)
        t = time.time()
        with open(fname, 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
                if i % 100 == 0:
                    progress(i, n, t, done=False)
        progress(-1, -1, t, done=True)
        return True
    except Exception as e:
        print(e)
        return False


def progress(i, n, begin_time, done):
    num_bars = 40
    consumed_time = time.time() - begin_time

    if done:
        print(f'\rDownloading has been finished. consumed {consumed_time:.2} seconds.')
        return None

    i += 1
    expected_time = n * consumed_time / i
    remain_time = expected_time - consumed_time
    num_done = int(40 * i / n)
    bars = '#' * num_done + '-' * (num_bars - num_done)
    print(f'\r[{bars}] ({100 * i / n:.2f} %)', end='')


def unzip(source, destination):
    """
    Arguments
    ---------
    source : str
        zip file address. It doesn't matter absolute path or relative path
    destination :
        Directory path of unzip

    Returns
    -------
    flag : Boolean
        It return True if downloading success else return False
    """

    abspath = os.path.abspath(destination)
    dirname = os.path.dirname(abspath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    try:
        downloaded = zipfile.ZipFile(source)
        downloaded.extractall(destination)
        return True
    except Exception as e:
        print(e)
        return False
