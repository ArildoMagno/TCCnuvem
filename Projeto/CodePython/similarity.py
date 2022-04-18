import wn
from wn.similarity import wup
import constants

# configure
# wn.download('own-pt')
# wn.remove('own-pt')
# wn.add('banco-own-pt/own-pt-lmf.xml')

var_glob_qnt_sim = 0


def calculate_wu_palmer_similarity(word1, word2):
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


def calculate_similarity_between_docs(doc_segmented1, doc_segmented2):
    global var_glob_qnt_sim
    similar_sets = []
    for set1 in doc_segmented1:
        for set2 in doc_segmented2:
            similar_sets_temp = calculate_similarity_between_sets(set1, set2)
            similar_sets.append((similar_sets_temp, set1, set2))

            # secao 4.3.3 calculo
            if plagiarism_detection_analyse(similar_sets_temp[0], similar_sets_temp[1]):
                sw1 = show_words_from_set(set1)
                sw2 = show_words_from_set(set2)
                var_glob_qnt_sim += 1
                print("Similaridade:", round(similar_sets_temp[0], 2), " entre ", sw1, " do doc1 e", sw2, "do doc2")
    return similar_sets


def show_words_from_set(set_input):
    sim = []
    for i in set_input:
        sim.append(i[0])
    return sim


def plagiarism_detection_analyse(average_ab, avegare_ba):
    # calculo secao 4.3.3
    p = 0.78
    if average_ab >= p:
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
            # [1] = lemma
            temp_similarity.append(calculate_wu_palmer_similarity(word1[1], word2[1]))

        if not all(p == constants.SYNONYMGROUPNOTFOUND for p in temp_similarity):
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)
            anB.append(max(temp_similarity))

    # relacao de cada elemento de B com todos os elementos do conjunto A
    for word2 in set2:
        temp_similarity = []
        for word1 in set1:
            temp_similarity.append(calculate_wu_palmer_similarity(word2[1], word1[1]))

        if not all(p == constants.SYNONYMGROUPNOTFOUND for p in temp_similarity):
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)
            bmA.append(max(temp_similarity))

    average_anB = sum(anB) / len(anB)
    average_bmA = sum(bmA) / len(bmA)
    return average_anB, average_bmA


def calculate_probability_plagiarism_documents(tam_doc1, tam_doc2):
    global var_glob_qnt_sim
    calc = (var_glob_qnt_sim / (tam_doc1 + tam_doc2)) * 100
    calc = round(calc, 4)
    return calc
