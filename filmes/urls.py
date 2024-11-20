from django.contrib import admin
from django.contrib.auth.decorators import login_required

from filmes import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SignUpView, CustomLogoutView, movie_data, save_related_movie, CustomLoginView
from django.urls import path
from .api.viewsets import FilmesViewSets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', views.HomeView.as_view(), name='home'),
    path('api/movies/', movie_data, name='movie_data'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('save-movie/', views.save_related_movie, name='save_movie'),
    path('api/filmes',FilmesViewSets.as_view(), name='filmes-list'),
    path('api/filmes/<str:id>', FilmesViewSets.as_view(), name='filmes')
]
