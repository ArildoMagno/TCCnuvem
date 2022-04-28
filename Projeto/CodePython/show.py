
def show_log_from_docs(file_name1, file_name2, result_analyses):
    found_result = [x for x in result_analyses if x[0] == file_name1 and x[1] == file_name2]
    found_result = found_result[0]
    logdoc12 = found_result[2]
    logdoc21 = found_result[3]
    print("\nLog:", file_name1, ",", file_name2)
    show_sentences(logdoc12)
    print("\nLog:", file_name2, ",", file_name1)
    show_sentences(logdoc21)

def show_sentences(set_input):
    for i in set_input:
        percent = str(i[0][0])
        sentence1 = show_words(i[1][0])
        sentence2 = show_words(i[2][0])
        print(percent + " Similar", "= SentencaDoc1:", sentence1, "| SentencaDoc2:", sentence2)

def show_words(set):
    sim = "'"
    for i in set:
        sim += i.text + " "
    sim = sim[:-1]
    return sim



