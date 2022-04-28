import wn
from wn.similarity import wup
import constants

# configure
# wn.download('own-pt')
# wn.remove('own-pt')
# wn.add('banco-own-pt/own-pt-lmf.xml')


value_similarity_sets_store = []
similar_sets_log = []


def wu_palmer_similarity(word1, word2):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    value_similarity = 0
    # Diferente duas palavras nao tem nenhuma similaridade com nao existir synset para a palavra
    if len(synset1) > 0 and len(synset2) > 0:
        synset1 = synset1[0]
        synset2 = synset2[0]
        if synset1.pos == synset2.pos:
            value_similarity = wup(synset1, synset2, True)
    else:
        return constants.SYNONYMGROUPNOTFOUND
    return value_similarity


def clear_global_variables():
    global var_glob_qnt_sim_vetor
    global value_similarity_sets_store

    var_glob_qnt_sim_vetor = []
    value_similarity_sets_store = []


def calculate_similarity_between_docs(doc_segmented1, doc_segmented2):
    global value_similarity_sets_store

    for set1 in doc_segmented1:
        for set2 in doc_segmented2:
            similar_sets_temp = calculate_similarity_between_sets(set1[1], set2[1])
            uAB = similar_sets_temp[0]
            uBA = similar_sets_temp[1]

            # secao 4.3.3 calculo
            if sentences_similar_threshold(uAB, uBA):
                # salva quais sao os sets similares, cria o log
                value_similarity_sets_store.append(1)
                similar_sets_log.append((similar_sets_temp, set1, set2))


def show_words_from_set(set_input):
    sim = []
    for i in set_input:
        sim.append(i[0])
    return sim


def sentences_similar_threshold(uAB, uBA):
    # calculo secao 4.3.3
    p = 0.8
    v = 0.15
    diference = abs(uAB - uBA)
    if min(uAB, uBA) >= p and diference <= v:
        return True
    else:
        return False


def calculate_similarity_between_sets(set1, set2):
    anB = []
    bmA = []

    # calculo secao 4.3.2
    # anB: a1Bn, a2Bn, a3Bn
    # relacao de cada elemento de A com todos os elementos do conjunto B
    for word1 in set1:
        temp_similarity = []
        for word2 in set2:
            temp_similarity.append(wu_palmer_similarity(word1.lemma_, word2.lemma_))

        if constants.SYNONYMGROUPNOTFOUND in temp_similarity:
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)

        if len(temp_similarity) > 0:
            anB.append(max(temp_similarity))

    # relacao de cada elemento de B com todos os elementos do conjunto A
    for word2 in set2:
        temp_similarity = []
        for word1 in set1:
            temp_similarity.append(wu_palmer_similarity(word2.lemma_, word1.lemma_))

        if constants.SYNONYMGROUPNOTFOUND in temp_similarity:
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)

        if len(temp_similarity) > 0:
            bmA.append(max(temp_similarity))

    uAB = sum(anB) / len(anB)
    uBA = sum(bmA) / len(bmA)
    return uAB, uBA


def calculate_degree_resemblance(tam, t):
    global value_similarity_sets_store
    global similar_sets_log
    # Quantidade de similar que apareceu em doc1 comparado com doc2, qntd de sentencas em doc1
    calc = len(value_similarity_sets_store) / tam
    calc = round(calc, 2)
    return calc, similar_sets_log


# Temporariamente 1:1
def odds_ratio_in_percent(resemblance1, resemblance2):
    total_resemblance = resemblance1 * resemblance2
    odds_ratio = total_resemblance / (1 - total_resemblance)
    odds_ratio_to_percent = odds_ratio / (1 + odds_ratio)
    return round(odds_ratio_to_percent * 100, 2)
