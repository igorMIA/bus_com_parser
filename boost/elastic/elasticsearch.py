import math
from django.urls import reverse
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from .utils import escape_reserved_characters

MAIN_INDEX_NAME = 'main_index'
PAGE_SIZE = 10


class Elastic:

    def __init__(self):
        self.es = Elasticsearch(['http://elasticsearch:9200'])
        self._create_main_index_if_not_exists()

    def _create_main_index_if_not_exists(self):
        """
        method that creates new elastic index if not existed
        :return:
        """
        ic = IndicesClient(self.es)
        if not ic.exists(MAIN_INDEX_NAME):
            ic.create(MAIN_INDEX_NAME)

    def index_document(self, body, elastic_id):
        """
        method that puts prepared(like dict) data to elastic inded
        :param body: {'key': value}
        :param elastic_id:
        :return:
        """
        self.es.index(MAIN_INDEX_NAME, body, id=elastic_id)

    def get_all_documents(self, page=1):
        """
        for debugging purposes only
        :param page:
        :return:
        """
        body = self._get_pagineted_query(self._build_match_all_query, page)
        return self._prepare_response(self.es.search(index=MAIN_INDEX_NAME, body=body), page)

    def search_documents(self, query, page=1):
        """
        method for pagineted search in elastic index
        :param query:
        :param page:
        :return:
        """
        body = self._get_pagineted_query(self._build_query, page, query)
        return self._prepare_response(self.es.search(index=MAIN_INDEX_NAME, body=body), page)

    @staticmethod
    def _build_query(query, size, start=0):
        """
        method for creating search body
        :param query:
        :param size: size of return dataset
        :param start: offset
        :return: template for search query
        """
        return {
            "query": {
                "query_string": {
                    "query": f"{escape_reserved_characters(query)}"
                }
            },
            "size": f'{size}',
            "from": f'{start}',
        }

    @staticmethod
    def _build_match_all_query(query, size, start=0):
        """
        method for creating search body
        for debugging purposes only
        :param query:
        :param size: size of return dataset
        :param start: offset
        :return: template for search query
        """
        return {
            "query": {
                "match_all": {}
            },
            "size": f'{size}',
            "from": f'{start}',
        }

    @staticmethod
    def _get_pagineted_query(template, page, query=None):
        """
        build paginated body for search
        :param template:
        :param page:
        :param query:
        :return:
        """
        page = (page - 1) * PAGE_SIZE
        if page < 0:
            return template(query, PAGE_SIZE, 0)
        return template(query, PAGE_SIZE, page)

    def _prepare_response(self, elasic_reponse, page):
        """
        works with response from elastic and get in paginated
        :param elasic_reponse:
        :param page:
        :return: paginated data
        Note:
        pagination only works with response that contains less then 10000 documents
        """
        pages = math.ceil(elasic_reponse['hits']['total']['value'] / PAGE_SIZE) - 1
        if pages < 0:
            pages = 0

        pagineted_data = {
            'count': elasic_reponse['hits']['total']['value'],
            'pages': pages,
            'current_page': page,
            'previous': reverse('search_api', kwargs={'page': page - 1 if page > 0 else 0}),
            'next': reverse('search_api', kwargs={'page': page + 1 if page < pages else page}),
            'results': elasic_reponse['hits']['hits']
        }
        return pagineted_data
