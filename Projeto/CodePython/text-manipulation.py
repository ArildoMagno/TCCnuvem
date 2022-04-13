import spacy
import wn
from wn.similarity import wup
from itertools import product

# configure
# wn.add('banco-own-pt/own-pt-lmf.xml')
spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_lg")
all_stop_words = nlp.Defaults.stop_words


# 1 - implementar PD
# 2 - passar palavra original junto com o lema para mostrar na hora do print


def read_text(text):
    text = open(text, "r").read()
    return text


def calculate_wu_palmer_similarity(word1, word2):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    value_similarity = 0
    if len(synset1) > 0 and len(synset2) > 0:
        synset1 = synset1[0]
        synset2 = synset2[0]
        if synset1.pos == synset2.pos:
            value_similarity = wup(synset1, synset2, True)

    return value_similarity


def calculate_similarity_between_docs(doc_segmented1, doc_segmented2):
    similar_sets = []
    for set1 in doc_segmented1:
        for set2 in doc_segmented2:
            similar_sets_temp = calculate_similarity_between_sets(set1, set2)
            similar_sets.append((calculate_similarity_between_sets(set1, set2), set1, set2))

            # no lugar desse IF vai jogar para o PD(A,B)
            # e se PD der True, já joga p saida a similaridade entre os conjuntos
            if similar_sets_temp[0] > 0.7:
                print("Similaridade de:", similar_sets_temp[0], " entre ", set1, set2)
            if similar_sets_temp[1] > 0.7:
                print("Similaridade de:", similar_sets_temp[1], " entre ", set1, set2)
    return similar_sets


def plagiarism_detection_analyse():
    print()


def calculate_similarity_between_sets(set1, set2):
    similar_sets = []
    anB = []
    bmA = []
    # algoritmo matematico descrito na secao 4.3.2

    # anB: a1Bn, a2Bn, a3Bn
    # calcula a relacao de cada elemento de a com todos os elementos do conjunto B
    for word1 in set1:
        temp_similarity = []
        for word2 in set2:
            temp_similarity.append(calculate_wu_palmer_similarity(word1, word2))
        anB.append(max(temp_similarity))

    # calcula a relacao de cada elemento de b com todos os elementos do conjunto A
    for word2 in set2:
        temp_similarity = []
        for word1 in set1:
            temp_similarity.append(calculate_wu_palmer_similarity(word2, word1))
        bmA.append(max(temp_similarity))

    # calcula a media, para ter a relação entre AB e BA
    average_anB = sum(anB) / len(anB)
    average_bmA = sum(bmA) / len(bmA)
    return average_anB, average_bmA


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
    doc_input1 = read_text("texto1.txt")
    doc_input2 = read_text("texto2.txt")
    n_gram = 3
    # FEm
    doc_tokenized_lematized_nostopwords1 = tokenization_lematization_stopwordsremoval(doc_input1)
    doc_tokenized_lematized_nostopwords2 = tokenization_lematization_stopwordsremoval(doc_input2)
    doc_segmented1 = ngrams(doc_tokenized_lematized_nostopwords1, n_gram)
    doc_segmented2 = ngrams(doc_tokenized_lematized_nostopwords2, n_gram)

    calculate_similarity_between_docs(doc_segmented1, doc_segmented2)
    print("end")


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
