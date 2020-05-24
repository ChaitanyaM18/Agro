from django.db import models

class GovtDetails(models.Model):
    link = models.CharField(max_length=300)
    title = models.CharField(max_length=300,blank=True)
    description = models.CharField(max_length=800)

    def __str__(self):
        return str(self.link)
