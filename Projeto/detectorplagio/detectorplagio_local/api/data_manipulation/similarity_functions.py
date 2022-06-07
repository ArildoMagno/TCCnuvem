import wn

wn.config.data_directory = 'wn_data'
wn.config.allow_multithreading = True
from wn.similarity import wup
from .constants import SYNONYMGROUPNOTFOUND


class Similarity:

    def wu_palmer_similarity(self, word1, word2):
        if word1 == word2:
            return 1

        synset1 = wn.synsets(word1)
        synset2 = wn.synsets(word2)
        value_similarity = 0

        if len(synset1) > 0 and len(synset2) > 0:
            synset1 = synset1[0]
            synset2 = synset2[0]
            if synset1.pos == synset2.pos:
                value_similarity = wup(synset1, synset2, True)
        else:
            return SYNONYMGROUPNOTFOUND
        return value_similarity

    def calculate_similar_sentences_in_docs(self, doc_segmented1, doc_segmented2, sentences_already_analysed):
        # secao 4.3.3 calculo 2015
        qntd_similar_sets = []
        similar_sentences_log = []

        sentences_analysed = sentences_already_analysed

        for sentence1 in doc_segmented1:
            for sentence2 in doc_segmented2:
                # verifica se essas sentencas ja foram analisadas
                verify_set = self.verify_sentence_analysed(sentences_analysed,
                                                           self.convert_token_to_str(sentence1[1]),
                                                           self.convert_token_to_str(sentence2[1]))
                # Sentenças nao analisadas
                if verify_set == None:
                    similar_sets_temp = self.similarity_between_sentences(sentence1[1], sentence2[1])
                    uAB = similar_sets_temp[0]
                    uBA = similar_sets_temp[1]

                    sentence_result = {
                        "sentence_doc1": self.convert_token_to_str(sentence1[0]),
                        "sentence_doc2": self.convert_token_to_str(sentence2[0]),
                        "sentence_trated_doc1": self.convert_token_to_str(sentence1[1]),
                        "sentence_trated_doc2": self.convert_token_to_str(sentence2[1]),
                        "percentage_doc1_doc2": similar_sets_temp[0],
                        "percentage_doc2_doc1": similar_sets_temp[1],
                    }

                    # Se forem o suficientemente similar
                    if self.sentences_similar_threshold(uAB, uBA):
                        threshold_high = True
                        qntd_similar_sets.append(1)
                        similar_sentences_log.append(sentence_result)
                    else:
                        threshold_high = False
                    sentences_analysed.append((sentence_result, threshold_high))
                # analisados e threshold alto
                elif verify_set != None and verify_set != False:
                    qntd_similar_sets.append(1)
                    similar_sentences_log.append(verify_set)

        return qntd_similar_sets, similar_sentences_log, sentences_analysed

    def verify_sentence_analysed(self, list, sentence_doc1, sentence_doc2):
        # Analisar
        if len(list) == 0:
            return None

        for element in list:
            sentence_trated_doc1 = element[0].get('sentence_trated_doc1')
            sentence_trated_doc2 = element[0].get('sentence_trated_doc2')
            if sentence_trated_doc1 == sentence_doc1 and sentence_trated_doc2 == sentence_doc2 \
                    or sentence_trated_doc1 == sentence_doc2 and sentence_trated_doc2 == sentence_doc1:
                if element[1] == True:
                    return element[0]
                # baixo threshold
                else:
                    return False
        # nao analisado
        return None

    def verify_word_analysed(self, list, word1, word2):
        # Analisar
        if len(list) == 0:
            return None

        for element in list:
            word1_trated = element[0]
            word2_trated = element[1]
            similarity = element[2]
            if word1 == word1_trated and word2 == word2_trated or \
                    word1 == word2_trated and word2 == word1_trated:
                return similarity
        # nao analisado
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

    def similarity_between_sentences(self, set1, set2):
        # calculo secao 4.3.2
        anB = []
        bmA = []

        # anB: a1Bn, a2Bn, a3Bn
        # relacao de cada elemento de A com todos os elementos do conjunto B
        words_analyesd = []
        for word1 in set1:
            similarity = 0
            temp_similarity = []
            for word2 in set2:
                verify = self.verify_word_analysed(words_analyesd, word1.text, word2.text)
                if verify == None:
                    if similarity < 1 or similarity == SYNONYMGROUPNOTFOUND:
                        similarity = self.wu_palmer_similarity(word1.text, word2.text)
                        temp_similarity.append(similarity)
                        words_analyesd.append((word1.text, word2.text, similarity))
                    else:
                        temp_similarity.append(similarity)
                else:
                    similarity = verify
                    temp_similarity.append(similarity)

            if SYNONYMGROUPNOTFOUND in temp_similarity:
                while SYNONYMGROUPNOTFOUND in temp_similarity: temp_similarity.remove(
                    SYNONYMGROUPNOTFOUND)

            if len(temp_similarity) > 0:
                anB.append(max(temp_similarity))

        # relacao de cada elemento de B com todos os elementos do conjunto A
        for word2 in set2:
            similarity = 0
            temp_similarity = []
            for word1 in set1:
                verify = self.verify_word_analysed(words_analyesd, word2.text, word1.text)
                if verify == None:
                    if similarity < 1 or similarity == SYNONYMGROUPNOTFOUND:
                        similarity = self.wu_palmer_similarity(word1.text, word2.text)
                        temp_similarity.append(similarity)
                        words_analyesd.append((word1.text, word2.text, verify, similarity))
                else:
                    similarity = verify
                    temp_similarity.append(similarity)

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
