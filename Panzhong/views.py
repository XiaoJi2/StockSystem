from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Panzhong.models import PanZhongData

bkgg_id = 801001

@login_required(login_url='Login:login')
def panzhong_shishi(request):
    global bkgg_id
    pz_data = PanZhongData()
    ggrq_data = pz_data.gegurenqi()
    bkrq_data = pz_data.bankuairenqi()
    news_data = pz_data.getnews()
    dx_data = pz_data.duanxianjingling()
    zb_data = pz_data.getdapanzhibo()
    bkgg_data = pz_data.bankuaigegu(bkgg_id)
    datadirc = {'ggrq': ggrq_data, 'bbrq': bkrq_data, 'news': news_data, 'duanxian': dx_data, 'dapanzhibo': zb_data, 'bankuaigegu': bkgg_data}
    # print(datadirc)

    return render(request, 'Panzhong/panzhongshishi.html', context=datadirc)

@login_required(login_url='Login:login')
def bankuaigegu(request):
    if request.method == "POST":
        data_id = request.POST.get('id')
        print(data_id)
        pz_data = PanZhongData()
        bkgg_data = pz_data.bankuaigegu(data_id)
        global bkgg_id
        bkgg_id = data_id
        return JsonResponse(bkgg_data)
