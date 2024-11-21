from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from filmes.api import serializer
from filmes.models import Filme
from filmes.api.serializer import FilmesSerializer


class FilmesViewSets(APIView):
    def get(self, request, id=None):
        if id:
            filme = get_object_or_404(Filme, id=id)
            serializer = FilmesSerializer(filme)
            return Response(serializer.data)
        items = Filme.objects.all()
        serializer = FilmesSerializer(items, many= True)
        return Response(serializer.data)

    def post(self,request):
        serializer = FilmesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        item = get_object_or_404(Filme, id=id)
        item.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        item = get_object_or_404(Filme, id=id)
        serializer = FilmesSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)