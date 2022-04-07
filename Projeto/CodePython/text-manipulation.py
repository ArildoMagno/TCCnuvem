# Usando Spacy para POS
# Usando NLTK para Tokenizacao

# imports
import spacy

# configure
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
    print("Pos-Tagging:", fem)


execute()
