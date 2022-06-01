import wn

wn.config.data_directory = 'wn_data'
wn.config.allow_multithreading = True
from wn.similarity import wup
from .constants import SYNONYMGROUPNOTFOUND


class Similarity:

    def wu_palmer_similarity(self, word1, word2):
        synset1 = wn.synsets(word1)
        synset2 = wn.synsets(word2)
        value_similarity = 0

        if word1 == word2:
            return 1

        if len(synset1) > 0 and len(synset2) > 0:
            synset1 = synset1[0]
            synset2 = synset2[0]
            if synset1.pos == synset2.pos:
                value_similarity = wup(synset1, synset2, True)
        else:
            return SYNONYMGROUPNOTFOUND
        return value_similarity

    def calculate_similar_sets_in_docs(self, doc_segmented1, doc_segmented2):
        # secao 4.3.3 calculo 2015
        qntd_similar_sets = []
        similar_sets_log = []

        for set1 in doc_segmented1:
            found_similar_set = False
            sentence = {}
            for set2 in doc_segmented2:

                verify_set = self.verify_set_in_sentencelist(similar_sets_log, self.convert_token_to_str(set1[1]),
                                                             self.convert_token_to_str(set2[1]))
                # Se a analise da sentença nao ta na lista, avalia
                if verify_set == None:
                    similar_sets_temp = self.similarity_between_sets(set1[1], set2[1])
                    uAB = similar_sets_temp[0]
                    uBA = similar_sets_temp[1]
                    # Se forem o suficiente similar
                    if self.sentences_similar_threshold(uAB, uBA):
                        sentence = {
                            "sentence_doc1": self.convert_token_to_str(set1[0]),
                            "sentence_doc2": self.convert_token_to_str(set2[0]),
                            "sentence_trated_doc1": self.convert_token_to_str(set1[1]),
                            "sentence_trated_doc2": self.convert_token_to_str(set2[1]),
                            "percentage_doc1_doc2": similar_sets_temp[0],
                            "percentage_doc2_doc1": similar_sets_temp[1],
                        }
                        found_similar_set = True
                        # similar_sets_log.append(sentence)
                else:
                    sentence = verify_set
                    found_similar_set = True

            if found_similar_set:
                qntd_similar_sets.append(1)
                similar_sets_log.append(sentence)

        return qntd_similar_sets, similar_sets_log

    def verify_set_in_sentencelist(self, list, sentence_trated1, sentence_trated2):
        if len(list) == 0:
            return None

        for element in list:
            sentence_trated_doc1 = element.get('sentence_trated_doc1')
            sentence_trated_doc2 = element.get('sentence_trated_doc2')
            if sentence_trated_doc1 == sentence_trated1 and sentence_trated_doc2 == sentence_trated2:
                return element
        return None

    def convert_token_to_str(self, list_token):
        new_str = ""
        for token in list_token:
            new_str += token.text + " "
        new_str = new_str[:-1]
        return new_str

    def sentences_similar_threshold(self, uAB, uBA):
        # calculo secao 4.3.3
        p = 0.73
        if min(uAB, uBA) >= p:
            return True
        else:
            return False

    def similarity_between_sets(self, set1, set2):
        # calculo secao 4.3.2
        anB = []
        bmA = []

        # anB: a1Bn, a2Bn, a3Bn
        # relacao de cada elemento de A com todos os elementos do conjunto B
        for word1 in set1:

            temp_similarity = []
            for word2 in set2:
                temp_similarity.append(self.wu_palmer_similarity(word1.lemma_, word2.lemma_))

            if SYNONYMGROUPNOTFOUND in temp_similarity:
                while SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                    SYNONYMGROUPNOTFOUND)

            if len(temp_similarity) > 0:
                anB.append(max(temp_similarity))

        # relacao de cada elemento de B com todos os elementos do conjunto A
        for word2 in set2:
            temp_similarity = []
            for word1 in set1:
                temp_similarity.append(self.wu_palmer_similarity(word2.lemma_, word1.lemma_))

            if SYNONYMGROUPNOTFOUND in temp_similarity:
                while SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                    SYNONYMGROUPNOTFOUND)

            if len(temp_similarity) > 0:
                bmA.append(max(temp_similarity))
        if len(anB) > 0:
            uAB = sum(anB) / len(anB)
        else:
            uAB = 0
        if len(bmA) > 0:
            uBA = sum(bmA) / len(bmA)
        else:
            uBA = 0
        return uAB, uBA

    def degree_resemblance(self, qntd_similar_sets, tam):
        # Trabalho HTML
        if qntd_similar_sets == 0:
            calc = 0
        else:
            calc = len(qntd_similar_sets) / tam
            calc = round(calc, 2)
        return calc

    def odds_ratio_in_percent(self, resemblance1, resemblance2):
        # Trabalho HTML
        total_resemblance = resemblance1 * resemblance2
        if total_resemblance != 1:
            odds_ratio = total_resemblance / (1 - total_resemblance)
            odds_ratio_to_percent = odds_ratio / (1 + odds_ratio)
            result = round(odds_ratio_to_percent * 100, 2)
        else:
            result = 100
        return round(result, 2)
