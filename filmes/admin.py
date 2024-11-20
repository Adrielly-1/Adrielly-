from django.contrib import admin
from filmes.models import Filme, UserFilme


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'imagem_url', 'disponibilidade_url')
    search_fields = ('titulo', 'descricao')

@admin.register(UserFilme)
class UserFilmeAdmin(admin.ModelAdmin):
    list_display = ('user', 'filme', 'data_adicionado')
    list_filter = ('user', 'filme')