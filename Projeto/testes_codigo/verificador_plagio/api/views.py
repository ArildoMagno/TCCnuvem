# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status

from .data_manipulation.similarity import Similarity
from .data_manipulation.textdata import TextManipulation
import json


class CalculateSimilarity(APIView):
    def post(self, request, format=None):
        # Get infos from files:
        data = request.data
        dits = dict(data.lists())
        files = dits.get('file')
        files_data_store = []

        for file in files:
            file_data = FileData()
            text = ''
            name = file.name

            for line in file:
                text += line.decode() + ' '
            text = text[:-1]

            file_data.name_file = name
            file_data.text = text
            files_data_store.append(file_data)

        # Analyse Files:
        result_analyse = []
        for file1 in files_data_store:
            for file2 in files_data_store:
                if file1.name_file != file2.name_file:
                    result = analyse_docs(file1.name_file, file2.name_file, file1.text, file2.text)
                    print("Result: ", result)
                    result_analyse.append(result)

        # Generate Result
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

        print(data_final_analyse)

        return Response(data_final_analyse)


def analyse_docs(file_name1, file_name2, doc1, doc2):
    text_manipulation = TextManipulation()
    similarity = Similarity()

    # # FEM REPLICA ESSE ALGORITMO DE LA AQUI
    doc1_segmented = text_manipulation.segmentation_based_sentences(doc1)
    doc2_segmented = text_manipulation.segmentation_based_sentences(doc2)

    # #  SIMILARITY 1: (doc1 em relação ao doc2) SÓ REPLICAR O METODO AQUI:
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