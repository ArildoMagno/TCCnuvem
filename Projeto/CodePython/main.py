import textmanipulation
import similarity
import show
from os import walk


def analyse_docs(file_name1, file_name2):
    print("Analisando arquivos: ", file_name1, ", ", file_name2)
    doc1 = textmanipulation.read_text(file_name1)
    doc2 = textmanipulation.read_text(file_name2)

    # FEM
    doc1_segmented = textmanipulation.segmentation_based_sentences(doc1)
    doc2_segmented = textmanipulation.segmentation_based_sentences(doc2)

    #  SIMILARITY 1: (doc1 em relação ao doc2)
    qntd_similar_sets1, similar_sets_log1 = similarity.calculate_similar_sets_in_docs(doc1_segmented, doc2_segmented)
    degree_resemblance1 = similarity.degree_resemblance(qntd_similar_sets1, len(doc1_segmented))

    #  SIMILARITY 2: (doc2 em relação ao doc1)
    qntd_similar_sets2, similar_sets_log2 = similarity.calculate_similar_sets_in_docs(doc2_segmented, doc1_segmented)
    degree_resemblance2 = similarity.degree_resemblance(qntd_similar_sets2, len(doc2_segmented))

    percent_plagiarism = similarity.odds_ratio_in_percent(degree_resemblance1, degree_resemblance2)

    return (file_name1, file_name2, similar_sets_log1, similar_sets_log2, percent_plagiarism)


def file_names(mypath):
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    return filenames


if __name__ == '__main__':
    file_names_store = file_names("texts/")
    result_analyses_geral = []
    files_analysed = []
    for i in file_names_store:
        for j in file_names_store:
            if i != j and ((i, j) not in files_analysed and not (j, i) in files_analysed):
                file_name1 = "texts/" + i
                file_name2 = "texts/" + j
                result_analyse_docs = analyse_docs(file_name1, file_name2)
                print("Probabilidade de Plagio entre os dois DOCS:", result_analyse_docs[4], "%")
                result_analyses_geral.append(result_analyse_docs)
                files_analysed.append((i, j))
                show.show_log_from_docs(file_name1, file_name2, result_analyses_geral)
                print("\n")

    # # Para testes rapidos 1:1:
    # file_name1 = "texts/text2-fonte.txt"
    # file_name2 = "texts/text2-plagio.txt"
    # result_analyse_docs = analyse_docs(file_name1, file_name2)
    # print("Probabilidade de Plagio entre os dois DOCS:", result_analyse_docs[4], "%")
    # result_analyses_geral.append(result_analyse_docs)
    # show.show_log_from_docs(file_name1, file_name2, result_analyses_geral)
    # print("\n\n")
