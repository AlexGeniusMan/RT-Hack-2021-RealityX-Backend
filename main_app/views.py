from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import random


class TestView(APIView):
    """
    Returns exposition information
    """

    @staticmethod
    def post(request):
        return Response('ok')

