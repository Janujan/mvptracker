from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views import generic
from collections import OrderedDict

from .models import Player, Game, Blog
from fusioncharts import FusionCharts

# Create your views here.
# def playerlist(request):
#     player_list = Player.objects.all()
#     context = {'player_list': player_list}
#     return render(request, 'playerList.html', context)
#
# def playerDetails(request, player_id):
#     try:
#         player = Player.objects.get(pk=player_id)
#     except:
#         raise Http404("Player does not exist")
#
#     context = {'player': player}
#     return render(request, 'details.html', context)
def blogDetails(request, blog_id):
    try:
        blog = Blog.objects.get(pk = blog_id)
    except:
        raise Http404("Post does not exist")

    context = {'blog_details': blog}

    return render(request, 'post.html', context)


def summaryList(request):
    player_list = Player.objects.order_by('-ascore')
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

    games = player.game_set.all()
    for i in range(len(games)-5,len(games)):
        chartData[str(games[i].start_time)] = games[i].points

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
        chartData2[str(games[i].start_time)] = games[i].assists

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
        chartData3[str(games[i].start_time)] = games[i].rebounds

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
