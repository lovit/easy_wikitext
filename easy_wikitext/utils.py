def paragraphs_to_sentences(paragraphs):
    """
    Args:
        paragraphs: list of Paragraph
            Paragraph is namedtuple
            Paragraph has {doc_idx: int, paragraph_idx:int, title:str, texts: list of str}
    Return:
        sents: list of str
            Flatten sentence list
    """
    sents = [sent for para in paragraphs for sent in para.texts]
    return sents
