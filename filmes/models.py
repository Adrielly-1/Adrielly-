from django.contrib.auth.models import User
from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem_url = models.URLField()
    disponibilidade_url = models.URLField()

    def __str__(self):
        return self.titulo


class UserFilme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'filme')

    def __str__(self):
        return f'{self.user.username} - {self.filme.titulo}'
