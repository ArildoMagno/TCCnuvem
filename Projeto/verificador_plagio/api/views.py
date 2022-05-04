# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status


class MainView(APIView):
    def get(self, request, format=None):
        return Response({'Nice Request'}, status=status.HTTP_200_OK)


class SendFilesView(APIView):
    def post(self, request, format=None):
        return Response({'Nice Request'}, status=status.HTTP_200_OK)
