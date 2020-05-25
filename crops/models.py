from django.db import models

class States(models.Model):
    state_name = models.CharField(max_length=300,unique=True,error_messages ={"unique":"This State already exists"})
    state_image = models.ImageField(upload_to='assets/media/')

    def __str__(self):
        return str(self.state_name)

class StateCrops(models.Model):
    state = models.ForeignKey(States, related_name="states", on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=600,blank=True)
    crop_image = models.ImageField(upload_to='assets/media/')
    crop_description = models.TextField(max_length=None)
    fertilizers = models.TextField(max_length=None)
