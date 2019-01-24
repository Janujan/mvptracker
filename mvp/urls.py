from django.urls import path

from . import views

app_name = 'mvp'

urlpatterns = [
    #/mvp/
    path('', views.summaryList, name='playerlist'),
    path('<int:player_id>/', views.playerDetails, name='playerDetails'),
    path('blog/<int:blog_id>/', views.blogDetails, name='blogDetails'),
    path('api/', views.playersList, name='playersList'),
    path('api/<str:name>', views.detailedPlayer, name='DetailedPlayer'),

]
