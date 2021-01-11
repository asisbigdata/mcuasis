from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import func
from urllib.parse import parse_qsl

#from func3api.models import company
from super.models import company
from django.db.models import Q
from django.shortcuts import render

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@系網':
                        func.sendCarousel0(event)

                    elif mtext == '@董監事資訊':
                        func.sendCarousel1(event)
    
                    elif mtext == '@PM2.5':
                        func.sendCarousel2(event)
    
                    elif mtext == '@證券':
                        func.sendCarousel3(event)
						
					elif mtext == '@加權指數':
                        func.sendCarousel4(event)
						
					elif mtext == '@CPI':
                        func.sendCarousel5(event)
    
                    
    
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                if backdata.get('action') == 'buy':
                    func.sendBack_buy(event, backdata)
                elif backdata.get('action') == 'sell':
                    func.sendBack_sell(event, backdata)

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
    
def selecct_list(request):
	cComid = request.POST.get('cComid',False)
	cPosition = request.POST.get('cPosition',False)
	cName = request.POST.get('cName',False)
	cSharemoney = request.POST.get('cSharemoney',False)
	if cSharemoney == '0':
		select_all = company.objects.filter( Q(cComid__icontains=cComid) & Q(cPosition__icontains=cPosition) & Q(cSharemoney__icontains=cSharemoney))
	else:
		select_all = company.objects.filter( Q(cComid__icontains=cComid) & Q(cPosition__icontains=cPosition) & Q(cSharemoney=cSharemoney))
	return render(request,'select_all.html', {'select_all': select_all})
    

def listall(request):  
	companys = company.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
	return render(request, "listall.html", locals())