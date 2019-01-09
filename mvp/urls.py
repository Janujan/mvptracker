from django.urls import path

from . import views
from .views import ListPlayerView

app_name = 'mvp'

urlpatterns = [
    #/mvp/
    path('', views.summaryList, name='playerlist'),
    #/mvp/1
    path('<int:player_id>/', views.playerDetails, name='playerDetails'),
    path('blog/<int:blog_id>/', views.blogDetails, name='blogDetails'),
    #path('api/', ListPlayerView.as_view(), name="players-all"),
    path('api/', views.playersList, name='playersList'),
    path('api/<str:name>', views.detailedPlayer, name='DetailedPlayer'),

]
