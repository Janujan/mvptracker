from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from django.views import generic
from collections import OrderedDict
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view

from .models import Player, Game, Blog
from fusioncharts import FusionCharts
from rest_framework import generics
from .models import Player, Game
from .serializer import PlayerSerializer, PlayerDetailSerializer


@api_view(['GET', 'POST'])
def playersList(request):
    if request.method == 'GET':
        players = Player.objects.all()

        print(request.query_params)
        if(request.query_params.get('max')):
            max_val = int(request.query_params.get('max'))
            players= players[0:max_val-1]
        serializer = PlayerSerializer(players,many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # check if player is authenticated
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():

            if(request.data['complete']==1):
                print('AUTHENTICATED')
                serializer.save()
                return JsonResponse(serializer.data, status=201)

            return JsonResponse(status=401, data={'status':'false','message':"not authorized"})

        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
def detailedPlayer(request, name):
    try:
        #perform some name cleaning
        names = name.split(' ')
        clean_name = names[0].capitalize() + ' ' + names[1].capitalize()
        print(clean_name)

        if clean_name == 'Lebron James':
            clean_name = 'LeBron James'
        player = Player.objects.get(player_name=clean_name)
    except Player.DoesNotExist:
        return HttpResponse(status=400)

    if request.method == 'GET':
        serializer = PlayerDetailSerializer(player)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        serializer = PlayerDetailSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        player.delete()
        return HttpResponse(status=204)

def blogDetails(request, blog_id):
    try:
        blog = Blog.objects.get(pk = blog_id)
    except:
        raise Http404("Post does not exist")

    context = {'blog_details': blog}

    return render(request, 'post.html', context)


def summaryList(request):
    player_list = Player.objects.order_by('-ascore')[0:10]
    blog_list = Blog.objects.all()

    context = { 'player_list' : player_list,
                'blog_list': blog_list[0:5]}

    return render(request, 'playerList.html', context)

def playerDetails(request, player_id):
    model = Player
    template_name = 'details.html'


    try:
        player = Player.objects.get(pk=player_id)
    except:
        raise Http404("Player does not exist")


    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = player.player_name + " Points (2018-19)"
    chartConfig["subCaption"] = "Ongoing Scores"
    chartConfig["xAxisName"] = "Date"
    chartConfig["yAxisName"] = "Points"
    chartConfig["numberSuffix"] = ""
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs of data
    chartData = OrderedDict()

    games = player.games.order_by('start_time')
    for i in range(len(games)-5,len(games)):
        chartData[str(games[i].start_time.strftime('%m-%d'))] = games[i].points

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    #The data for the chart should be in an array wherein each element of the array
    #is a JSON object# having the `label` and `value` as keys.

    #Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    line1 = FusionCharts("line", "Points", "540", "400", "points-container", "json", dataSource)

    dataSource2 = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig2 = OrderedDict()
    chartConfig2["caption"] = player.player_name + " Assists (2018-19)"
    chartConfig2["subCaption"] = "Ongoing Scores"
    chartConfig2["xAxisName"] = "Date"
    chartConfig2["yAxisName"] = "Assists"
    chartConfig2["numberSuffix"] = ""
    chartConfig2["theme"] = "fusion"

    chartData2 = OrderedDict()
    dataSource2["chart"] = chartConfig2
    dataSource2["data"] = []

    for i in range(len(games)-5,len(games)):
        chartData2[str(games[i].start_time.strftime('%m-%d'))] = games[i].assists

    dataSource2["data"] = []
    for key, value in chartData2.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource2["data"].append(data)


    line2 = FusionCharts("line", "Assists", "540", "400", "assists-container", "json", dataSource2)

    dataSource3 = OrderedDict()

    # The `chartConfig` dict contains key-value pairs of data for chart attribute
    chartConfig3 = OrderedDict()
    chartConfig3["caption"] = player.player_name + " Rebounds (2018-19)"
    chartConfig3["subCaption"] = "Ongoing Scores"
    chartConfig3["xAxisName"] = "Date"
    chartConfig3["yAxisName"] = "Rebounds"
    chartConfig3["numberSuffix"] = ""
    chartConfig3["theme"] = "fusion"

    chartData3 = OrderedDict()
    dataSource3["chart"] = chartConfig3
    dataSource3["data"] = []

    for i in range(len(games)-5,len(games)):
        chartData3[str(games[i].start_time.strftime('%m-%d'))] = games[i].rebounds

    dataSource3["data"] = []
    for key, value in chartData3.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource3["data"].append(data)


    line3 = FusionCharts("line", "Rebounds", "540", "400", "rebounds-container", "json", dataSource3)

    context = {'player': player, 'output1':line1.render(), \
        'output2':line2.render(),'output3':line3.render()}
    return render(request, 'details.html', context)
