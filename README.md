# wikitext data easy-handler

This package helps you handle `wikitext` easily, from download to load.

## Usage

Set `data_type` as one of [None, 'train', 'valid', 'test']

```python
from easy_wikitext import load

dict_of_paragraph = load(name='wikitext-2')
list_of_paragraph = load(name='wikitext-2', data_type='train')
```

You can also load `wikitext-103` with same manner

```python
dict_of_paragraph = load(name='wikitext-103')
list_of_paragraph = load(name='wikitext-103', data_type='valid')
```

Sometime, you just need the list of sentence. However the `load` returns list of namedtuple `Paragraph`.

```python
from easy_wikitext import load

paragraphs = load(name='wikitext-2', data_type='test')
paragraphs[0]
```

```
Paragraph(doc_idx=0, paragraph_idx=1, title='2000 – 2005', texts=['In 2000 <unk> had a guest ...])
```

To acquire sentence,

```
paragraph = paragraphs[0]
paragraph.texts # list of str
```

You can easily transform the list of Paragraph to list of sentence.

```python
from easy_wikitext import paragraphs_to_sentences

sents = paragraphs_to_sentences(paragraphs)
sents[:3]
```

```
['Robert <unk> is an English ...',
 'In 2006 , <unk> starred alongside ...',
 'In 2000 <unk> had a guest @-@ ...']
```
