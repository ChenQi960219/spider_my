import requests
from ..http.response import Response


class Downloader(object):

    def get_response(self, request):
        if request.method.upper() == 'GET':
            rs = requests.get(request.url, params=request.params, headers=request.headers)

        elif request.method.upper() == 'POST':
            rs = requests.post(request.url, data=request.data, headers=request.headers)

        else:
            raise Exception('只支持GET和POST请求')

        return Response(rs.url, rs.status_code, headers=rs.headers, body=rs.content)