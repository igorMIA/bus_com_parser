from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from elastic.elasticsearch import Elastic


class BusStationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, page):
        """
        get all documents from elastic search
        for debugging purposes only
        :param request:
        :param page:
        :return:
        """
        es = Elastic()
        response = es.get_all_documents(page)
        return Response(response)

    def post(self, request, page):
        """
        get all documents that match query
        :param request:
        :param page:
        :return:
        """
        es = Elastic()
        query = request.POST.get('query')
        if query:
            response = es.search_documents(query)
        else:
            response = {
                'message': 'Error. Not valid query, please try again'
            }
        return Response(response)
