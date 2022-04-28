import textmanipulation_sentences as textmanipulation
import similarity_basedhtml as similarity


def execute(file_name1, file_name2, n_gram):
    # TEMPORARIAMENTE FUNCIONANDO 1:1
    print("\nAnalisando arquivos: ", file_name1, ", ", file_name2)
    doc_input1 = textmanipulation.read_text(file_name1)
    doc_input2 = textmanipulation.read_text(file_name2)

    # # FEM

    doc1 = textmanipulation.tokenization_ngram_stopwords_removal(doc_input1, n_gram)
    doc2 = textmanipulation.tokenization_ngram_stopwords_removal(doc_input2, n_gram)

    # #  SIMILARITY 1: (doc1 em relação ao doc2)
    similarity.calculate_similarity_between_docs(doc1, doc2)
    degree_resemblance1, similar_sets1 = similarity.calculate_degree_resemblance(len(doc1), len(doc2))

    print("\nResemblance doc1,doc2= ", degree_resemblance1)

    # LOG
    # show_words_from_set(similar_sets1)

    #  SIMILARITY 2: (doc2 em relação ao doc1)
    similarity.clear_global_variables()
    similarity.calculate_similarity_between_docs(doc2, doc1)
    degree_resemblance2, similar_sets2 = similarity.calculate_degree_resemblance(len(doc2), len(doc1))

    print("\nResemblance doc2,doc1= ", degree_resemblance2)
    # LOG
    # show_words_from_set(similar_sets2)

    print("\n\nProbabilidade de Plagio entre os dois DOCS:",
          similarity.odds_ratio_in_percent(degree_resemblance1, degree_resemblance2), "%")


def show_words_from_set_inside(set):
    sim = "'"
    for i in range(1, len(set)):
        if i != (len(set) - 1):
            sim += set[i].text + " "
        else:
            sim += set[i].text + "'"
    return sim


def show_words_from_set(set_input):
    for i in set_input:
        print(str(i[0]) + " Similar", "= SentencaDoc1:", show_words_from_set_inside(i[1][0]), "| SentencaDoc2:",
              show_words_from_set_inside(i[2][0]))


if __name__ == '__main__':
    print("\nSimilariade (0~1) 0=Completamente diferentes, 1=Identicos ou Sinonimos\n\n")
    n_gram = 3
    file_name1 = "texts/text2-fonte.txt"
    file_name2 = "texts/text2-plagio.txt"
    execute(file_name1, file_name2, n_gram)

    file_name1 = "texts/text3-fonte.txt"
    file_name2 = "texts/text3-plagio.txt"
    execute(file_name1, file_name2, n_gram)

    file_name1 = "texts/text4-fonte.txt"
    file_name2 = "texts/text4-plagio.txt"
    execute(file_name1, file_name2, n_gram)

    file_name1 = "texts/text5-fonte.txt"
    file_name2 = "texts/text5-plagio.txt"
    execute(file_name1, file_name2, n_gram)
