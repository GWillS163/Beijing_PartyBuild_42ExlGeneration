from django.shortcuts import render
from scorerank.models import cal
from django.http import HttpResponse
import json

# Create your views here.
rank_list = []

# def index(request):
#     return render(request, 'index.html')

def calPag(request):
    return render(request, 'upload_score.html')

def receive(request):
    """接收上传并保存数据"""
    client_num = request.POST['client_num']
    score = request.POST['score']
    cal.objects.create(client=client_num, score=score, rank=0)
    # s.append
    return render(request, 'upload_score.html', context={"data":  client_num + ' ' + str(score) + "保存成功"})

def DelData(request):
    cal.objects.exclude(client='客户端').delete()
    return HttpResponse('清库完成')

def alllist(request):
    data = cal.objects.all().order_by('score')
    n = 0
    for i in data:
        n += 1
        i.rank = n
        print(i.client, i.score, i.rank)

    return render(request, 'index.html', context={'data': data})

# 接口一, 过滤分数1~10000
def receive_query_score(request):
    try:
        down_strict = request.POST['down_strict']
        up_strict = request.POST['up_strict']
        current_client = request.POST['current_client']
        print(down_strict, up_strict)
        data = cal.objects.all()

        n = 0
        for i in data:
            n += 1
            i.rank = n
        current_client_data = cal.objects.filter(client__exact=current_client)[0]
        print(current_client_data.client, current_client_data.score, current_client_data.rank)
        data = data.filter(score__gte=down_strict)
        data = data.filter(score__lte=up_strict)
        # data = cal.objects.all().filter('score'.__gt__(down_strict) and 'score'.__lt__(up_strict))
        print(data)
        return render(request, 'query_score_range.html', context={'score_data': data,
                                                                  'current_client': current_client_data})
    except:
        pass
    return render(request, 'query_score_range.html' )


# 接口er, 过滤rank n~n
def receive_query_rank(request):
    try:
        down_strict = int(request.POST['down_strict'])
        up_strict = int(request.POST['up_strict'])
        current_client = request.POST['current_client']
        print(down_strict, up_strict)

        # 排序+rank号
        data = cal.objects.order_by('score')
        current_client_data = data.filter(client__exact=current_client)[0]
        # print(current_client_data.client, current_client_data.score, current_client_data.rank)
        data_new = []
        n = 0
        for i in data:
            n += 1
            i.rank = n
            # 筛选rank区间 - 1
            if i.rank>= down_strict and i.rank<= up_strict:
                data_new.append({'client': i.client, 'score': i.score, 'rank': i.rank})
                print('收录', i.client, i.score, i.rank)
        # 筛选区间 - 2
        # range_list = [i for i in range(down_strict, up_strict)]
        # data = data.filter(rank__in=range_list)
        # 筛选区间 - 3
        # data = data.filter(rank__gte=down_strict)
        # data_new = data.filter(rank__lte=up_strict)
        print('score_gte', data)

        print(data_new)
        return render(request, 'query_rank_range.html', context={'rank_data': data_new,
                                                                  'current_client': current_client_data})
    except:
        pass
    return render(request, 'query_rank_range.html', )


# API
def api_alllist(request):
    data = cal.objects.all().order_by('score')
    n = 0
    dict = {}
    for i in data:
        n += 1
        i.rank = n
        dict.update({i.pk: {'rank': i.rank,
                            'client': i.client,
                            'score': i.score}, })
    return HttpResponse(json.dumps(dict))

def api_getRank(request, down_strict, up_strict, client):
    print(down_strict, up_strict, client)

    # 排序+rank号
    data = cal.objects.order_by('score')
    current_client_data = data.filter(client__exact=client)[0]
    data_new = []
    n = 0
    for i in data:
        n += 1
        i.rank = n
        # 筛选rank区间 - 1
        if i.rank >= down_strict and i.rank <= up_strict:
            data_new.append({'client': i.client, 'score': i.score, 'rank': i.rank})
            print('收录', i.client, i.score, i.rank)

    print(data_new)
    all_data = data_new + current_client_data
    return HttpResponse(json.dumps(all_data))

