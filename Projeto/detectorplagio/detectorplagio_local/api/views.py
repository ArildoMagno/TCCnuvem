# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pickle
import shutil
import threading

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import api.data_manipulation.similarity_analysedocs as similarity_analyse_docs
import api.data_manipulation.textdata as text_data
import api.pdf_generator.pdf as pdf_generator


class CalculateSimilarity(APIView):
    def post(self, request, format=None):
        # Not remove variable data (cause heroku error!):
        data = request.data

        if not os.path.exists("api/analyse_flags"):
            os.makedirs("api/analyse_flags")

        # cria o lock da task executando:
        if not os.path.exists("api/analyse_flags/processing-lock.txt"):
            with open("api/analyse_flags/processing-lock.txt", "w") as f:
                f.write(str(0))
                f.close()

            # pega os dados dos arquivos
            info_files = text_data.get_info_from_files(request)

            # inicia a thread
            thread_long = ThreadLong(data=info_files)
            thread_long.start()

            # se ainda nao terminou de processingar
            if not os.path.exists("api/analyse_flags/result_analyse.dictionary"):
                with open('api/analyse_flags/processing-lock.txt', 'rb') as f:
                    data_file = int(f.read())
                    calc = data_file / len(info_files)
                    f.close()
                return Response(calc)
            else:
                # Show Info:
                with open('api/analyse_flags/result_analyse.dictionary', 'rb') as config_dictionary_file:
                    config_dictionary = pickle.load(config_dictionary_file)

                delete_flags()
                return Response(config_dictionary)
        else:
            if not os.path.exists("api/analyse_flags/result_analyse.dictionary"):
                with open('api/analyse_flags/processing-lock.txt', 'rb') as f:
                    data_file = int(f.read())
                    dits = dict(data.lists())
                    files = dits.get('file')

                    calc = data_file / len(files)
                    f.close()

                return Response(calc)
            else:
                # Show Info:
                with open('api/analyse_flags/result_analyse.dictionary', 'rb') as config_dictionary_file:
                    config_dictionary = pickle.load(config_dictionary_file)

                delete_flags()
                return Response(config_dictionary)


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


class CleanFiles(APIView):
    def post(self, request, format=None):
        delete_flags()
        return Response("ok")


def delete_flags():
    folder = "api/analyse_flags"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
