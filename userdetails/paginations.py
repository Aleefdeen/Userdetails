from rest_framework.pagination import PageNumberPagination


class UserDetailsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"
    max_limit = 50
    ordering = "id"