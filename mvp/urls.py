from django.urls import path

from . import views

app_name = 'mvp'

urlpatterns = [
    #/mvp/
    path('', views.summaryList, name='playerlist'),
    #/mvp/1
    path('<int:player_id>/', views.playerDetails, name='playerDetails'),
]
