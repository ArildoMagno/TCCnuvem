import spacy
import wn
from wn.similarity import wup
from itertools import product

# configure
# wn.add('banco-own-pt/own-pt-lmf.xml')
spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words


def read_text(text):
    text = open(text, "r").read()
    return text


def calculate_wu_palmer_similarity(word1, word2):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    high_similar_words = []
    similar_words = []

    for sense1, sense2 in product(synset1, synset2):
        if sense1.pos == sense2.pos:
            d = wup(sense1, sense2, True)
            similar_words.append((d, sense1, sense2))

    if len(similar_words) > 0:
        high_similar_words = max(similar_words, key=lambda item: item[0])

    return high_similar_words


def calculate_similarity_between_docs(doc_segmented1, doc_segmented2):
    similar_sets = []
    for set1, set2 in product(doc_segmented1, doc_segmented2):
        temp_similar_sets = calculate_similarity_between_sets(set1, set2)
        if len(temp_similar_sets) > 0:
            similar_sets.append(temp_similar_sets)
    return similar_sets


def calculate_similarity_between_sets(set1, set2):
    similar_sets = []
    for word1, word2 in product(set1, set2):
        similarity = calculate_wu_palmer_similarity(word1, word2)
        # range para a similaridade
        if len(similarity) > 0:
            if similarity[0] > 0.85:
                similar_sets.append(similarity)
    return similar_sets


def tokenization_lematization_stopwordsremoval(text):
    doc = nlp(text)
    words_pos = []
    for token in doc:
        if token.text not in all_stop_words and token.lemma_ not in all_stop_words \
                and token.tag_ != "PUNCT" and token.tag_ != "SPACE" \
                and token.lemma_ not in words_pos:
            words_pos.append(token.lemma_)
    return words_pos


def execute():
    doc_input1 = read_text("text-example1.txt")
    doc_input2 = read_text("text-example2.txt")
    n_gram = 3
    # tokenizacao e segmentacao do texto
    doc_tokenized_lematized_nostopwords1 = tokenization_lematization_stopwordsremoval(doc_input1)
    doc_tokenized_lematized_nostopwords2 = tokenization_lematization_stopwordsremoval(doc_input2)

    doc_segmented1 = ngrams(doc_tokenized_lematized_nostopwords1, n_gram)
    doc_segmented2 = ngrams(doc_tokenized_lematized_nostopwords2, n_gram)
    similarity_between_docs = calculate_similarity_between_docs(doc_segmented1, doc_segmented2)
    if len(similarity_between_docs) > 0:
        print("Documentos similaries em:\n", similarity_between_docs)
    else:
        print("Documentos nada similares!")


def search_synsets(word_source):
    synset_word = wn.synsets(word_source)
    print("From: ", word_source)
    for word in synset_word:
        word_syn = wn.synset(word.id)
        print('syn-lemmas: ', word_syn.lemmas())


def ngrams(input_ngrams, n):
    output = []
    for i in range(len(input_ngrams) - n + 1):
        output.append(input_ngrams[i:i + n])
    return output


execute()
