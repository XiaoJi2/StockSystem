from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from App.models import SummaryTable

@login_required(login_url='Login:login')
def index(request):
    return render(request, "App/index.html", context=locals())


def get_market_temperature(request):
    if request.method == 'GET':
        summary = SummaryTable()
        info = summary.get_market_temperature()
        return JsonResponse(info)

def get_lianban_hight(request):
    print(request.method)
    if request.method == 'GET':
        summary = SummaryTable()
        info = summary.get_lianban_hight()
        data = {"data": info}
        return JsonResponse(data)

