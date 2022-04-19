# textract para converter arquivos para texto: (TESTAR)

import textract
text = textract.process("texts/textoformatstestes.pdf")
print(text)