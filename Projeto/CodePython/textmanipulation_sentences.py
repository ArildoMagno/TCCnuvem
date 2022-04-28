import spacy

spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words

var_glob_qnt_sim = 0


def read_text(text):
    text = open(text, mode="r", encoding="utf-8").read()
    return text


def tokenization_ngram_stopwords_removal(text, n_gram):
    originaltext_segmented = []

    doc = nlp(text)

    for sentence in doc.sents:
        sentence = remove_stop_words_puncts(sentence)
        # essa parte do ocupando espaco é onde vai o log
        if len(sentence) > 0:
            # Fazer ele armazenar o conteudo original para mostrar a sentença no log
            # no lugar do ocupando espaço aqui
            originaltext_segmented.append(("ocupandoespaco", sentence))

    return originaltext_segmented


def remove_stop_words_puncts(sentence):
    sentence_result = []
    for token in sentence:
        if token.tag_ != "SPACE" and token.tag_ != "PUNCT" and token.text not in all_stop_words \
                and token.lemma_ not in all_stop_words:
            sentence_result.append(token)
    return sentence_result
