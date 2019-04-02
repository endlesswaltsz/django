import json
import time

from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ImageGuardMiddleware(MiddlewareMixin):
    pass
    # def process_request(self, request):
    #     lis = request.path.split('/')
    #     if lis[1] == 'media':
    #         if request.META.get('HTTP_REFERER') == 'http://172.96.198.74/':
    #             return
    #         time = request.session.get('time')
    #         if time:
    #             if time < 3:
    #                 request.session['time'] += 1
    #                 return
    #             return HttpResponse('没有')
    #         request.session['time'] = 1


class VisitFrequencyLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET':
            return
        frequency = request.session.get('frequency')
        if frequency:
            frequency.append(time.time())
            if len(frequency) < 4:
                request.session['frequency'] = frequency
            else:
                if frequency[-1] - frequency[0] < 60:
                    frequency.pop(-1)
                    request.session['frequency'] = frequency
                    return HttpResponse(json.dumps({'status': 'error', 'msg': '提交过于频繁'}, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                frequency.pop(0)
                request.session['frequency'] = frequency
            return
        request.session['frequency'] = [time.time(), ]
