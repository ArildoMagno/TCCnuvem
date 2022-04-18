import textmanipulation
import similarity


def execute():
    print("\nSimilariade (0~1) 0=Completamente diferentes, 1=Identicos ou Sinonimos\n\n")
    doc_input1 = textmanipulation.read_text("text-example1.txt")
    doc_input2 = textmanipulation.read_text("text-example2.txt")
    n_gram = 5
    # FEM
    doc_tokenized_lematized_nostopwords1 = textmanipulation.tokenization_lematization_stopwordsremoval(doc_input1)
    doc_tokenized_lematized_nostopwords2 = textmanipulation.tokenization_lematization_stopwordsremoval(doc_input2)
    doc_segmented1 = textmanipulation.ngrams(doc_tokenized_lematized_nostopwords1, n_gram)
    doc_segmented2 = textmanipulation.ngrams(doc_tokenized_lematized_nostopwords2, n_gram)
    similarity.calculate_similarity_between_docs(doc_segmented1, doc_segmented2)
    relacao_doc = similarity.calculate_probability_plagiarism_documents(len(doc_segmented1), len(doc_segmented2))
    print("\nProbabilidade de Plagio entre estes Documentos:", str(relacao_doc) + "%")


execute()