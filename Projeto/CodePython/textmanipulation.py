import spacy

spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words

var_glob_qnt_sim = 0


def read_text(text):
    text = open(text, mode="r", encoding="utf-8").read()
    return text


def tokenization_lematization_stopwordsremoval(text):
    doc = nlp(text)
    words_pos = []
    for token in doc:
        if token.text not in all_stop_words and token.lemma_ not in all_stop_words \
                and token.tag_ != "PUNCT" and token.tag_ != "SPACE" \
                and token.lemma_ not in words_pos:
            words_pos.append((token.text, token.lemma_))
    return words_pos


def ngrams(input_ngrams, n):
    output = []
    for i in range(len(input_ngrams) - n + 1):
        output.append(input_ngrams[i:i + n])
    return output
