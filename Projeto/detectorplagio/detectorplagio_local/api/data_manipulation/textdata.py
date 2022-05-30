import spacy
from pdfminer import high_level
import docx2txt

spacy.prefer_gpu()
nlp = spacy.load("pt_core_news_sm")
all_stop_words = nlp.Defaults.stop_words


class TextManipulation:
    def read_text(self, text):
        text = open(text, mode="r", encoding="utf-8").read()
        return text

    def segmentation_based_sentences(self, text):
        originaltext_segmented = []
        doc = nlp(text)

        for sentence in doc.sents:
            sentence_source = self.remove_only_spaces(sentence)
            sentence_clean = self.remove_stop_words_puncts_spaces(sentence)
            if len(sentence_clean) > 0:
                originaltext_segmented.append((sentence_source, sentence_clean))

        return originaltext_segmented

    def remove_stop_words_puncts_spaces(self, sentence):
        sentence_result = []
        for token in sentence:
            if token.tag_ != "SPACE" and token.tag_ != "PUNCT" and token.text not in all_stop_words \
                    and token.lemma_ not in all_stop_words:
                sentence_result.append(token)
        return sentence_result

    def remove_only_spaces(self, sentence):
        sentence_result = []
        for token in sentence:
            if token.tag_ != "SPACE":
                sentence_result.append(token)
        return sentence_result


class FileData:
    name_file = None
    text = None


def get_info_from_files(request):
    # Get infos from files:
    data = request.data
    dits = dict(data.lists())
    files = dits.get('file')
    files_data_store = []

    for file in files:
        file_data = FileData()
        name = file.name

        # extrai o texto do arquivo
        text = extract_text(file)

        file_data.name_file = name
        file_data.text = text
        # adiciona na lista de arquivos
        files_data_store.append(file_data)

    return files_data_store


# Extrai texto de .txt,.pdf,.docx
def extract_text(file):
    name = file.name
    obj = file.file
    extracted_text = ""

    if name.endswith('.pdf'):
        extracted_text = high_level.extract_text(obj, "")
    elif name.endswith('.txt'):
        for line in obj:
            extracted_text += line.decode() + ' '
        extracted_text = extracted_text[:-1]
    elif name.endswith('.docx'):
        extracted_text = docx2txt.process(obj)

    return extracted_text
