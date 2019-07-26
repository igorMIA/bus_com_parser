from rest_framework.response import Response
from rest_framework.views import APIView
from elastic.elasticsearch import Elastic


class BusStationView(APIView):

    def get(self, request, page):
        es = Elastic()
        response = es.get_all_documents(page)
        return Response(response)

    def post(self, request, page):
        es = Elastic()
        query = request.POST.get('query')
        if query:
            response = es.search_documents(query)
        else:
            response = {
                'message': 'Error. Not valid query, please try again'
            }
        return Response(response)
