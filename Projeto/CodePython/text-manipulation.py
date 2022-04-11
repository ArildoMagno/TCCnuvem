# Usando Spacy para POS
# Usando NLTK para Tokenizacao

# imports
import spacy
import wn

# configure
# adiciona o banco lexico xml na lib wn
# wn.add('banco-own-pt/own-pt-lmf.xml')
spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words


def read_text(text):
    text = open(text, "r").read()
    return text


def tokenization_and_part_of_speech(text):
    doc = nlp(text)
    words_pos = []
    for token in doc:
        # remove stop-words e pontuação e espaços
        # faz a lematizacao

        if token.text not in all_stop_words and token.tag_ != "PUNCT" and token.tag_ != "SPACE":
            words_pos.append((token, token.tag_, token.lemma_))
    return words_pos


def execute():
    text = read_text("text-example.txt")
    # fem = (Palavra, Tag, Lema)
    fem = tokenization_and_part_of_speech(text)
    for fprint in fem:
        print(fprint)


def search_synsets(word_source):
    synset_word = wn.synsets(word_source)

    print("From: ", word_source)
    for word in synset_word:
        word_syn = wn.synset(word.id)
        print('syn-lemmas: ', word_syn.lemmas())



search_synsets('homem')
