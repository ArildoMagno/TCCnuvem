# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .data_manipulation.similarity import Similarity
from .data_manipulation.textdata import TextManipulation
from math import ceil
from rest_framework.views import APIView
from rest_framework.response import Response
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from zipfile import ZipFile
from django.http import HttpResponse
from textwrap import wrap
from os import walk
import os
import shutil

from pdfminer import high_level
import docx2txt

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import textract


class CalculateSimilarity(APIView):
    def post(self, request, format=None):
        # Get infos from files:
        data = request.data
        dits = dict(data.lists())
        files = dits.get('file')
        files_data_store = []

        for file in files:
            # cria objeto tipo arquivo
            file_data = FileData()
            name = file.name

            # extrai o texto do arquivo
            text = extract_text(file)

            file_data.name_file = name
            file_data.text = text
            # adiciona na lista de arquivos
            files_data_store.append(file_data)

        # Analyse Files:
        result_analyse = []
        for file1 in files_data_store:
            for file2 in files_data_store:
                if file1.name_file != file2.name_file:
                    # Otimização
                    # Verifica se os documentos ainda não foram analisados pois (doc1,doc2) == (doc2,doc1)
                    files_already_analysed = files_already_analyzed(result_analyse, file1.name_file, file2.name_file)
                    # Caso não tiverem analisa, e caso já, apenas busca o resultado
                    if files_already_analysed == None:
                        result = analyse_docs(file1.name_file, file2.name_file, file1.text, file2.text)
                        result_analyse.append(result)
                    else:
                        result_analyse.append(files_already_analysed)

        # Generate Result Object Json
        data_analyse_objects = []
        source_name_files = []
        for result in result_analyse:
            if result.name_file1 not in source_name_files:
                source_name_files.append(result.name_file1)

            resultobject = {"name_file1": result.name_file1, "name_file2": result.name_file2,
                            "similar_sets_log1": result.similar_sets_log1,
                            "similar_sets_log2": result.similar_sets_log2,
                            "percent_plagiarism": result.percent_plagiarism}
            data_analyse_objects.append(resultobject)

        # Generate Result Graph
        data_final_analyse = []
        # Ordenation
        for name in source_name_files:
            data_source_file = [x for x in data_analyse_objects if x.get('name_file1') == name]
            relation_files = []
            name_source = ""
            for data_file in data_source_file:
                name_source = data_file.get('name_file1')
                relation_files.append(
                    {
                        "name_file_dest": data_file.get('name_file2'),
                        "similar_set_source_dest": data_file.get('similar_sets_log1'),
                        "similar_set_dest_source": data_file.get('similar_sets_log2'),
                        "percent": data_file.get('percent_plagiarism')
                    })

            data_final_analyse.append({
                "name_file_source": name_source,
                "relation_files": relation_files
            })

        return Response(data_final_analyse)


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


def files_already_analyzed(list, file1, file2):
    if len(list) <= 0:
        return None

    for item in list:
        item_name_file1 = item.__getattribute__('name_file1')
        item_name_file2 = item.__getattribute__('name_file2')
        percent_plagiarism = item.__getattribute__('percent_plagiarism')
        similar_sets_log1 = item.__getattribute__('similar_sets_log1')
        similar_sets_log2 = item.__getattribute__('similar_sets_log2')
        # Se essa combinação de Doc já foi analisada, retorna apenas atualziando os valores
        if item_name_file2 == file1 and item_name_file1 == file2:
            analyse = AnalyseResult()
            analyse.name_file1 = item_name_file2
            analyse.name_file2 = item_name_file1
            analyse.similar_sets_log1 = similar_sets_log2
            analyse.similar_sets_log2 = similar_sets_log1
            analyse.percent_plagiarism = percent_plagiarism
            return analyse

    return None


def analyse_docs(file_name1, file_name2, doc1, doc2):
    text_manipulation = TextManipulation()
    similarity = Similarity()

    # # FEM
    doc1_segmented = text_manipulation.segmentation_based_sentences(doc1)
    doc2_segmented = text_manipulation.segmentation_based_sentences(doc2)

    # #  SIMILARITY 1: (doc1 em relação ao doc2)
    qntd_similar_sets1, similar_sets_log1 = similarity.calculate_similar_sets_in_docs(doc1_segmented, doc2_segmented)
    degree_resemblance1 = similarity.degree_resemblance(qntd_similar_sets1, len(doc1_segmented))

    #  SIMILARITY 2: (doc2 em relação ao doc1)
    qntd_similar_sets2, similar_sets_log2 = similarity.calculate_similar_sets_in_docs(doc2_segmented, doc1_segmented)
    degree_resemblance2 = similarity.degree_resemblance(qntd_similar_sets2, len(doc2_segmented))

    percent_plagiarism = similarity.odds_ratio_in_percent(degree_resemblance1, degree_resemblance2)

    analyse = AnalyseResult()
    analyse.name_file1 = file_name1
    analyse.name_file2 = file_name2
    analyse.similar_sets_log1 = similar_sets_log1
    analyse.similar_sets_log2 = similar_sets_log2
    analyse.percent_plagiarism = percent_plagiarism

    return analyse


class FileData:
    name_file = None
    text = None


class AnalyseResult:
    name_file1 = None
    name_file2 = None
    similar_sets_log1 = None
    similar_sets_log2 = None
    percent_plagiarism = None


class GeneratePDF(APIView):

    def post(self, request, format=None):
        data = request.data
        # Gera arquivos PDFs
        generate_pdf(data)
        generate_zip()

        relatorio_file = open('relatorio.zip', 'rb').read()
        response = HttpResponse(relatorio_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="relatorio.zip"'

        temppdf_delete()
        relatoriozip_delete()
        return response


def generate_pdf(data):
    temppdf_create()

    # CADA DOCUMENTO
    for document in data:
        name_of_document_source = document.get('name_file_source')
        relation_files = document.get('relation_files')

        # CRIA DOCUMENTO:
        pre, ext = os.path.splitext(name_of_document_source)
        dest_filename = pre + ".pdf"

        canvas = Canvas("temppdf/" + dest_filename, pagesize=A4)
        pagesize = canvas._pagesize
        page_width = pagesize[0]
        page_height = pagesize[1]

        # CABEÇALHO
        y = 780
        size = 22
        canvas.setFont("Helvetica-Bold", size)

        text = "Relatório"
        text_width = canvas.stringWidth(text)
        xposition = (page_width - text_width) / 2.0
        canvas.drawString(xposition, y, text)
        y = y - (size * 2.5)

        size = 16
        canvas.setFont("Helvetica-Bold", size)
        name_of_document_source = name_of_document_source.split('.', 1)[0]
        text = "Sentenças Similares Documento " + name_of_document_source
        text_width = canvas.stringWidth(text)
        xposition = (page_width - text_width) / 2.0
        textobject = canvas.beginText(xposition, y)

        wraped_text = "\n".join(wrap(text, 80))  # 120 is line width
        textobject.textLines(wraped_text)
        canvas.drawText(textobject)
        lenstring = ceil((len(text) / 80))
        y = y - ((size * lenstring) * 2.5)

        # CONTEUDO (X EM RELACAO A Y)
        for file_rel in relation_files:
            name_of_document_dest = file_rel.get('name_file_dest')
            name_of_document_dest = name_of_document_dest.split('.', 1)[0]
            similar_set_result = file_rel.get('similar_set_source_dest')
            percent = file_rel.get('percent')

            canvas.setFont("Helvetica", 15)
            textobject = canvas.beginText(40, y)
            text = 'Documento ' + name_of_document_source + " em relação ao Documento " + name_of_document_dest + ": "
            wraped_text = "\n".join(wrap(text, 80))
            textobject.textLines(wraped_text)
            canvas.drawText(textobject)
            lenstring = ceil((len(text) / 80))
            y = y - ((size * lenstring) * 1.5)

            canvas.setFont("Helvetica", 13)
            canvas.drawString(40, y,
                              'Similaridade ' + str(percent) + "%")

            # SENTENCAS
            count = 0
            for sentences in similar_set_result:
                sentencedoc1 = name_of_document_source + ': ' + sentences.get('sentence_doc1')
                sentencedoc2 = name_of_document_dest + ': ' + sentences.get('sentence_doc2')
                lenstring = ceil((len(sentencedoc1) / 120))
                size = 12

                # Calcula se vai caber toda a sentenca na pagina, caso nao caiba, nova pagina
                calc_axisy = y - ((size * 2.5) + (size * 1.5) + ((size * lenstring) * 1.5))
                if (calc_axisy <= 30):
                    canvas.showPage()
                    y = 770

                canvas.setFont("Helvetica", size)
                y = y - (size * 2.5)
                canvas.drawString(60, y, "Sentença " + str(count) + ':')

                size = 8
                canvas.setFont("Helvetica", size)
                y = y - (size * 1.5)

                textobject = canvas.beginText(80, y)
                wraped_text = "\n".join(wrap(sentencedoc1, 120))  # 120 is line width
                textobject.textLines(wraped_text)
                canvas.drawText(textobject)
                y = y - ((size * lenstring) * 1.5)

                textobject = canvas.beginText(80, y)
                wraped_text = "\n".join(wrap(sentencedoc2, 120))  # 120 is line width
                textobject.textLines(wraped_text)
                canvas.drawText(textobject)
                y = y - ((size * lenstring) * 1.5)
                count += 1

            # troca pagina
            canvas.showPage()
            y = 750
            size = 16

        # salva documento
        canvas.save()


def temppdf_create():
    path_temppdf = 'temppdf'
    isExist = os.path.exists(path_temppdf)
    if not isExist:
        os.makedirs(path_temppdf)


def relatoriozip_delete():
    path_relatorio = 'relatorio.zip'
    isExist = os.path.exists(path_relatorio)
    if isExist:
        os.remove(path_relatorio)


def temppdf_delete():
    path_temppdf = 'temppdf'
    isExist = os.path.exists(path_temppdf)
    if isExist:
        shutil.rmtree(path_temppdf, ignore_errors=True)


def generate_zip():
    zipObj = ZipFile('relatorio.zip', 'w')

    filenames = next(walk('temppdf'), (None, None, []))[2]
    for filename in filenames:
        zipObj.write('temppdf/' + filename, filename)

    zipObj.close()
