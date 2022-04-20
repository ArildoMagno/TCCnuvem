import spacy

spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words

var_glob_qnt_sim = 0


# CRIAR FUNCAO PARA LER PDF/DOC

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
    print("\nPrimeiro:", output)
    return output


# se funcionar traduzir para inglês
def tokenization_ngram_stopwords_removal(text, n_gram):
    textooriginal_segmentado = []
    n_counter = 0
    doc = nlp(text)
    temp_original = []
    temp_segmentado = []

    for token in doc:
        if token.tag_ != "PUNCT" and token.tag_ != "SPACE":
            temp_original.append(token)

        if token.text not in all_stop_words and token.lemma_ not in all_stop_words \
                and token.tag_ != "PUNCT" and token.tag_ != "SPACE":
            n_counter += 1
            temp_segmentado.append(token)

        if n_counter == n_gram:
            textooriginal_segmentado.append((temp_original.copy(), temp_segmentado.copy()))
            temp_original.clear()
            temp_segmentado.clear()
            n_counter = 0

    print("\nSegundo:")
    print(textooriginal_segmentado)
    return textooriginal_segmentado
