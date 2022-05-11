import spacy

spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words


def read_text(text):
    text = open(text, mode="r", encoding="utf-8").read()
    return text


def segmentation_based_sentences(text):
    originaltext_segmented = []
    doc = nlp(text)

    for sentence in doc.sents:
        sentence_source = remove_only_spaces(sentence)
        sentence_clean = remove_stop_words_puncts_spaces(sentence)
        if len(sentence_clean) > 0:
            originaltext_segmented.append((sentence_source, sentence_clean))

    return originaltext_segmented


def remove_stop_words_puncts_spaces(sentence):
    sentence_result = []
    for token in sentence:
        if token.tag_ != "SPACE" and token.tag_ != "PUNCT" and token.text not in all_stop_words \
                and token.lemma_ not in all_stop_words:
            sentence_result.append(token)
    return sentence_result


def remove_only_spaces(sentence):
    sentence_result = []
    for token in sentence:
        if token.tag_ != "SPACE":
            sentence_result.append(token)
    return sentence_result


def segmentation_based_kgrams(text, n_gram):
    originaltext_segmented = []
    counter_tokens = 0
    doc = nlp(text)
    temp_original = []
    temp_segmented = []
    position = 0
    position_next_start = 0
    text_tokenized = []

    for token in doc:
        text_tokenized.append(token)

    while position != len(text_tokenized):
        token = text_tokenized[position]
        position += 1

        if token.tag_ != "PUNCT" and token.tag_ != "SPACE":
            temp_original.append(token)

        if token.text not in all_stop_words and token.lemma_ not in all_stop_words \
                and token.tag_ != "PUNCT" and token.tag_ != "SPACE":
            counter_tokens += 1
            temp_segmented.append(token)
            if counter_tokens == 1:
                position_next_start = position

        if counter_tokens == n_gram:
            originaltext_segmented.append((temp_original.copy(), temp_segmented.copy()))
            temp_original.clear()
            temp_segmented.clear()
            counter_tokens = 0
            position = position_next_start

    return originaltext_segmented
