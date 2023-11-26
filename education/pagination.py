from rest_framework.pagination import PageNumberPagination


class EducationPaginator(PageNumberPagination):
    page_size = 3
