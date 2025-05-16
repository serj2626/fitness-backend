from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ListResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "current": self.page.number,
            "next": self.page.next_page_number() if self.page.has_next() else None,
            "previous": self.page.previous_page_number() if self.page.has_previous() else None,
            "count": self.page.paginator.count,
            "results": data
        })