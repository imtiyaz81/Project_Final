from django.db import models

# Create your models here.
class Ticket(models.Model):
    procees_from = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=100)
    change_request = models.CharField(max_length=100)

    def __str__(self):
        return self.procees_from


class Header(models.Model):
    Source = models.CharField(max_length=100)
    Destination = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    StatusText = models.CharField(max_length=100)
    #ticket_header = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.Source

class Process(models.Model):
    xmlns_process = models.CharField(max_length=100,null=True)
    ticket_process = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.xmlns_process

class Results(models.Model):
    Header = models.ForeignKey(Header, on_delete=models.CASCADE)
    Process = models.ForeignKey(Process, on_delete=models.CASCADE)

    def __int__(self):
        return self.Process