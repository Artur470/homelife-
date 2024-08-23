from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    page_query_param = 'page'
    page_size = 15

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,  # Номер текущей страницы
            'count': self.page.paginator.count,  # Общее количество элементов
            'next': self.get_next_link(),  # Ссылка на следующую страницу
            'previous': self.get_previous_link(),  # Ссылка на предыдущую страницу
            'results': data  # Сами данные
        })
