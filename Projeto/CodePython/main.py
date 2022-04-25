import textmanipulation
import similarity


def execute(file_name1, file_name2, n_gram):
    print("\nAnalisando arquivos: ", file_name1, ", ", file_name2)
    doc_input1 = textmanipulation.read_text(file_name1)
    doc_input2 = textmanipulation.read_text(file_name2)

    # # FEM

    doc1 = textmanipulation.tokenization_ngram_stopwords_removal(doc_input1, n_gram)
    doc2 = textmanipulation.tokenization_ngram_stopwords_removal(doc_input2, n_gram)

    similarity.calculate_similarity_between_docs(doc1, doc2)
    relacao_doc, similar_docs = similarity.calculate_probability_plagiarism_documents(len(doc1),
                                                                                      len(doc2))
    print("\nProbabilidade de Plagio entre estes Documentos:", str(relacao_doc) + "%\n")
    show_words_from_set(similar_docs)


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
    n_gram = 7
    file_name1 = "texts/text2-fonte.txt"
    file_name2 = "texts/text2-plagio.txt"
    execute(file_name1, file_name2, n_gram)

    # file_name1 = "texts/text3-fonte.txt"
    # file_name2 = "texts/text3-plagio.txt"
    # execute(file_name1, file_name2, n_gram)
    #
    # file_name1 = "texts/text4-fonte.txt"
    # file_name2 = "texts/text4-plagio.txt"
    # execute(file_name1, file_name2, n_gram)
    #
    # file_name1 = "texts/text5-fonte.txt"
    # file_name2 = "texts/text5-plagio.txt"
    # execute(file_name1, file_name2, n_gram)
