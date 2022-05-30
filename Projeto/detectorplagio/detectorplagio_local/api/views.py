# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

import threading
import pickle
import shutil
import os

import api.pdf_generator.pdf as pdf_generator
# import pdf_generator.pdf
import api.data_manipulation.textdata as text_data
import api.data_manipulation.similarity_analysedocs as similarity_analyse_docs


class CalculateSimilarity(APIView):
    def post(self, request, format=None):

        # cria o lock da task executando:
        if not os.path.exists("api/analyse_flags/processing-lock"):
            open("api/analyse_flags/processing-lock", mode='w').close()

            # pega os dados dos arquivos
            info_files = text_data.get_info_from_files(request)
            # inicia a thread
            thread_long = ThreadLong(data=info_files)
            thread_long.start()

            # se ainda nao terminou de processingar
            if not os.path.exists("api/analyse_flags/result_analyse.dictionary"):
                return Response("processing")
            else:
                # Show Info:
                with open('api/analyse_flags/result_analyse.dictionary', 'rb') as config_dictionary_file:
                    config_dictionary = pickle.load(config_dictionary_file)

                self.delete_flags()
                return Response(config_dictionary)
        else:
            if not os.path.exists("api/analyse_flags/result_analyse.dictionary"):
                return Response("processing")
            else:
                # Show Info:
                with open('api/analyse_flags/result_analyse.dictionary', 'rb') as config_dictionary_file:
                    config_dictionary = pickle.load(config_dictionary_file)

                self.delete_flags()
                return Response(config_dictionary)

    def delete_flags(self):
        folder = "api/analyse_flags"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


class GeneratePDF(APIView):

    def post(self, request, format=None):
        data = request.data
        # Gera arquivos PDFs
        pdf_generator.generate_pdf(data)
        pdf_generator.generate_zip()

        relatorio_file = open('relatorio.zip', 'rb').read()
        response = HttpResponse(relatorio_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="relatorio.zip"'

        pdf_generator.temppdf_delete()
        pdf_generator.relatoriozip_delete()
        return response


class ThreadLong(threading.Thread):
    def __init__(self, group=None, target=None, data=None,
                 args=(), kwargs=None, verbose=None):
        super(ThreadLong, self).__init__()
        self.target = target
        self.data = data

    def run(self):
        # executa a analise
        result_analyse = similarity_analyse_docs.calculate_similarity_function(self.data)

        # Save info e gera flag de conclusão
        with open('api/analyse_flags/result_analyse.dictionary', 'wb') as config_dictionary_file:
            pickle.dump(result_analyse, config_dictionary_file)
