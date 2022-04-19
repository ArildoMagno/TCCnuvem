import textmanipulation
import similarity


def execute(file_name1, file_name2, n_gram):
    print("Analisando arquivos: ", file_name1, ", ", file_name2)
    doc_input1 = textmanipulation.read_text(file_name1)
    doc_input2 = textmanipulation.read_text(file_name2)

    # FEM
    doc_tokenized_lematized_nostopwords1 = textmanipulation.tokenization_lematization_stopwordsremoval(doc_input1)
    doc_tokenized_lematized_nostopwords2 = textmanipulation.tokenization_lematization_stopwordsremoval(doc_input2)
    doc_segmented1 = textmanipulation.ngrams(doc_tokenized_lematized_nostopwords1, n_gram)
    doc_segmented2 = textmanipulation.ngrams(doc_tokenized_lematized_nostopwords2, n_gram)
    similarity.calculate_similarity_between_docs(doc_segmented1, doc_segmented2)
    relacao_doc, similar_docs = similarity.calculate_probability_plagiarism_documents(len(doc_segmented1),
                                                                                      len(doc_segmented2))
    print("\nProbabilidade de Plagio entre estes Documentos:", str(relacao_doc) + "%\n\n")
    show_words_from_set(similar_docs)


def show_words_from_set_inside(set):
    sim = []
    for i in set:
        sim.append(i[0])
    return sim


def show_words_from_set(set_input):
    for i in set_input:
        print(str((i[0] * 100)) + "% Similar", "= SentencaDoc1:", show_words_from_set_inside(i[1]), "SentencaDoc2:",
              show_words_from_set_inside(i[2]))


if __name__ == '__main__':
    print("\n-----------------------------------------------------------------------------"
          "\nSimilariade\n\n")
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
