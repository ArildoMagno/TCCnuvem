import wn
from wn.similarity import wup
import constants

# configure
# wn.download('own-pt')
# wn.remove('own-pt')
# wn.add('banco-own-pt/own-pt-lmf.xml')

var_glob_qnt_sim_vetor = []

var_glob_qnt_degree_resemblance_vetor = []


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


def clear_global_variables():
    global var_glob_qnt_sim_vetor
    global var_glob_qnt_degree_resemblance_vetor

    var_glob_qnt_sim_vetor = []
    var_glob_qnt_degree_resemblance_vetor = []


def calculate_similarity_between_docs(doc_segmented1, doc_segmented2):
    global var_glob_qnt_sim_vetor
    global var_glob_qnt_degree_resemblance_vetor

    for set1 in doc_segmented1:
        similar_sets = []
        set2_store = []
        similar = False
        for set2 in doc_segmented2:
            similar_sets_temp = calculate_similarity_between_sets(set1[1], set2[1])

            # secao 4.3.3 calculo

            # NO MOMENTO VOU USAR A MAX, MAS NAO É ELA QUE USA AQUI, TEM QUE VERIFICAR ISSO
            similar_value_analyses = [similar_sets_temp[0], similar_sets_temp[1]]
            similar_value = max(similar_value_analyses)
            if plagiarism_detection_analyse(similar_value):
                similar = True
                similar_sets = similar_sets_temp
                set2_store = set2
        if similar:
            if (similar_sets[0], set1, set2_store) not in var_glob_qnt_sim_vetor and (
                    similar_sets[0], set2_store, set1) not in var_glob_qnt_sim_vetor:
                sim_percent = round(similar_sets[0], 2)
                var_glob_qnt_sim_vetor.append((sim_percent, set1, set2_store))
            var_glob_qnt_degree_resemblance_vetor.append(1)
        else:
            var_glob_qnt_degree_resemblance_vetor.append(0)


def show_words_from_set(set_input):
    sim = []
    for i in set_input:
        sim.append(i[0])
    return sim


def plagiarism_detection_analyse(average):
    # calculo secao 4.3.3
    p = 0.8
    if average >= p:
        return True
    else:
        return False


# Aqui envolve os calculos propostos nos pdf's
def calculate_similarity_between_sets(set1, set2):
    anB = []
    bmA = []
    # calculo secao 4.3.2

    # anB: a1Bn, a2Bn, a3Bn
    # relacao de cada elemento de A com todos os elementos do conjunto B
    for word1 in set1:
        temp_similarity = []
        for word2 in set2:
            temp_similarity.append(calculate_wu_palmer_similarity(word1.lemma_, word2.lemma_))

        if not all(p == constants.SYNONYMGROUPNOTFOUND for p in temp_similarity):
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)
            anB.append(max(temp_similarity))

    # relacao de cada elemento de B com todos os elementos do conjunto A
    for word2 in set2:
        temp_similarity = []
        for word1 in set1:
            temp_similarity.append(calculate_wu_palmer_similarity(word2.lemma_, word1.lemma_))

        if not all(p == constants.SYNONYMGROUPNOTFOUND for p in temp_similarity):
            while constants.SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                constants.SYNONYMGROUPNOTFOUND)
            bmA.append(max(temp_similarity))

    average_anB = sum(anB) / len(anB)
    average_bmA = sum(bmA) / len(bmA)
    return average_anB, average_bmA


def calculate_probability_plagiarism_documents(tam_doc1, tam_doc2):
    global var_glob_qnt_sim_vetor
    calc = (len(var_glob_qnt_sim_vetor) / (tam_doc1 * tam_doc2)) * 100
    calc = round(calc, 2)
    return calc, var_glob_qnt_sim_vetor


def calculate_degree_resemblance(tam1, tam2):
    global var_glob_qnt_sim_vetor
    global var_glob_qnt_degree_resemblance_vetor
    tam_total = (tam1 * tam2)
    calc = sum(var_glob_qnt_degree_resemblance_vetor) / len(var_glob_qnt_degree_resemblance_vetor)
    calc = round(calc, 2)
    return calc, var_glob_qnt_sim_vetor


# Temporariamente 1:1
def odds_ratio_in_percent(resemblance1, resemblance2):
    total_resemblance = resemblance1 * resemblance2

    if total_resemblance != 1:
        odds_ratio = total_resemblance / (1 - total_resemblance)
        odds_ratio_to_percent = odds_ratio / (1 + odds_ratio)
        result = odds_ratio_to_percent * 100
    else:
        result = 100

    return round(result, 2)
