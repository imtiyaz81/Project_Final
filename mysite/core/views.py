from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets

from .serializers import TicketSerializer, ProcessSerializer, HeaderSerializer, ResultSerializer
from core.models import Ticket, Process, Header, Results


# Create your views here.

class TicketList(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ProcessList(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class HeaderList(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer


class ResultList(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultSerializer

