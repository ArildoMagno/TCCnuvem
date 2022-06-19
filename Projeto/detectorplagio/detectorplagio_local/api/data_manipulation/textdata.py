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

            if len(sentence_clean) > 0 and not self.verify_sentence_already_segmented(originaltext_segmented,
                                                                                      sentence_clean):
                originaltext_segmented.append((sentence_source, sentence_clean))

        return originaltext_segmented

    def segmentation_based_kgram(self, text):
        originaltext_segmented = []
        kgram = 3

        counter_tokens = 0
        doc = nlp(text)
        temp_original = []
        temp_segmented = []
        position = 0
        position_next_start = 0
        text_tokenized = []

        for token in doc:
            text_tokenized.append(token)

        while position != len(text_tokenized):
            token = text_tokenized[position]
            position += 1

            if token.tag_ != "PUNCT" and token.tag_ != "SPACE":
                temp_original.append(token)

            if token.text not in all_stop_words and token.lemma_ not in all_stop_words \
                    and token.tag_ != "PUNCT" and token.tag_ != "SPACE":
                counter_tokens += 1
                temp_segmented.append(token)
                if counter_tokens == 1:
                    position_next_start = position

            if counter_tokens == kgram:
                originaltext_segmented.append((temp_original.copy(), temp_segmented.copy()))
                temp_original.clear()
                temp_segmented.clear()
                counter_tokens = 0
                position = position_next_start

        return originaltext_segmented

    def verify_sentence_already_segmented(self, list_sentences, sentence):
        if len(list_sentences) == 0:
            return False

        for sentence_in_list in list_sentences:
            sentence_list_str = self.convert_token_to_str(sentence_in_list[1])
            sentence_str = self.convert_token_to_str(sentence)

            if sentence_list_str == sentence_str:
                return True

        return False

    def convert_token_to_str(self, list_token):
        new_str = ""
        for token in list_token:
            new_str += token.text + " "
        new_str = new_str[:-1]
        return new_str

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
    data = request.data
    dits = dict(data.lists())
    files = dits.get('file')
    files_data_store = []

    for file in files:
        file_data = FileData()
        name = file.name

        text = extract_text(file)

        file_data.name_file = name
        file_data.text = text
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

    extracted_text = " ".join(extracted_text.split())
    return extracted_text
