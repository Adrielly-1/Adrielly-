import json
import logging
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.core.checks import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from filmes.forms import SignUpForm
from filmes.models import UserFilme, Filme

logger = logging.getLogger(__name__)

from django.contrib import messages


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'movies.html'
    login_url = '/login/'


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return response

    def form_invalid(self, form):
        print("Dados recebidos:", form.cleaned_data)
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados fornecidos.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class CustomLoginView(LoginView):
    def get_redirect_url(self):
        return '/'

@login_required
def film_search(request):
    return render(request, 'movies.html')

@login_required
def recommended_films(request):
    user_films = request.user.films.all()
    films = user_films[:10]
    data = [{'title': film.title, 'image_url': film.image_url} for film in films]
    return JsonResponse(data, safe=False)

@login_required
def vertical_films(request):
    films = Filme.objects.all()[:3]
    data = [{'title': film.title, 'image_url': film.image_url} for film in films]
    return JsonResponse(data, safe=False)

@login_required
def search_films(request):
    query = request.GET.get('q', '')
    films = Filme.objects.filter(title__icontains=query)
    data = [{'title': film.title, 'image_url': film.image_url} for film in films]
    return JsonResponse(data, safe=False)

def movie_data(request):
    user_id = request.user.id

    recommended_user_filmes = UserFilme.objects.filter(user_id=user_id)
    recommended_filmes = [uf.filme for uf in recommended_user_filmes]

    all_filmes = list(Filme.objects.all())
    random_filmes = random.sample(all_filmes, min(3, len(all_filmes)))

    def filme_to_dict(filme):
        return {
            'id': filme.id,
            'titulo': filme.titulo,
            'descricao': filme.descricao,
            'imagem_url': filme.imagem_url,
            'disponibilidade_url': filme.disponibilidade_url,
        }

    recommended_filmes_data = [filme_to_dict(filme) for filme in recommended_filmes]
    random_filmes_data = [filme_to_dict(filme) for filme in random_filmes]

    data = {
        'recommended_filmes': recommended_filmes_data,
        'random_filmes': random_filmes_data,
    }

    return JsonResponse(data)


@login_required
def movie_detail(request, movie_id):
    filme = get_object_or_404(Filme, id=movie_id)
    is_related = UserFilme.objects.filter(user=request.user, filme=filme).exists()
    return render(request, 'movie_detail.html', {'filme': filme, 'is_related': is_related})


@login_required
def save_related_movie(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            filme_id = int(data.get('filme_id'))
            filme = Filme.objects.get(id=filme_id)
        except (Filme.DoesNotExist, ValueError, json.JSONDecodeError):
            return JsonResponse({'error': 'Filme não encontrado'}, status=404)

        user = request.user
        user_filme, created = UserFilme.objects.get_or_create(user=user, filme=filme)

        if created:
            return JsonResponse({'message': 'Filme salvo com sucesso!'})
        else:
            user_filme.delete()
            return JsonResponse({'message': 'Filme removido com sucesso!'})

    return JsonResponse({'error': 'Método inválido'}, status=405)
