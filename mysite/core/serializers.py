from rest_framework import serializers, exceptions
from core.models import Ticket, Process, Header, Results


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('procees_from', 'ticket_id', 'change_request')

class HeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Header
        fields = ('Source', 'Destination', 'Status', 'StatusText')


class ProcessSerializer(serializers.ModelSerializer):

    ticket_process = TicketSerializer()

    class Meta:
        model = Process
        fields = ('xmlns_process', 'ticket_process')
        depth = 2

    def create(self, validated_data):
        p_data = validated_data.pop('ticket_process')
        ticket = Ticket.objects.create(**p_data)
        process = Process.objects.create(ticket_process=ticket, **validated_data)
        return process

    def update(self, instance, validated_data):
        tickets_data = validated_data.get('ticket_process')
        tickets_data.procees_from = tickets_data.get('procees_from')
        tickets_data.ticket_id = tickets_data.get('ticket_id')
        tickets_data.change_request = tickets_data.get('change_request')
        #ticket = Ticket.objects.filter(id=instance).update(**tickets_data)
        return Process

class ResultSerializer(serializers.ModelSerializer):
    Header = HeaderSerializer()
    Process = ProcessSerializer()
    class Meta:
        model = Results
        fields = [
            'Header',
            'Process',
        ]
        depth = 1

    def create(self, validated_data):
        Process_data = validated_data.pop('Process')
        header_data = validated_data.pop('Header')
        h_data = Header.objects.create(**header_data)
        Process_serializer = ProcessSerializer(data=Process_data)
        if Process_serializer.is_valid():
            Process_serializer.save()

        results = Results.objects.create(Process=Process_serializer.instance, Header=h_data, **validated_data)
        return results

    def update(self, instance, validated_data):
        Header_data = validated_data.get('Header')
        Process_data = validated_data.get('Process')
        Process_serializer = ProcessSerializer(instance, data=Process_data)
        if Process_serializer.is_valid():
            Process_serializer.save()

        instance.Header.Source = Header_data.get(
            'Source',
            instance.Header.Source
        )
        instance.Header.Destination = Header_data.get(
            'Destination',
            instance.Header.Destination
        )
        instance.Header.Status = Header_data.get(
            'Status',
            instance.Header.Status
        )
        instance.Header.StatusText = Header_data.get(
            'StatusText',
            instance.Header.StatusText
        )
        instance.Process.xmlns_process = Process_data.get(
            'xmlns_process',
            instance.Process.xmlns_process
        )
        instance.Header.save()
        instance.Process.save()
        instance.save()
        return instance
