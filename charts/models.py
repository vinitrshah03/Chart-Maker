from django.db import models

# Create your models here.
class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    occupation = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return (self.username + "" + self.email + "" +self.password+""+ self.full_name+""+self.occupation)

class objects_line(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.FloatField()

    def delete_all_records():
        objects_line.objects.all().delete()

class line_details(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.CharField(max_length=30)
    obj3 = models.CharField(max_length=30)
    obj4 = models.CharField(max_length=30)

    def delete_all_records():
        line_details.objects.all().delete()

class bar_details(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.CharField(max_length=30)
    obj3 = models.CharField(max_length=30)
    def delete_all_records():
        bar_details.objects.all().delete()

class objects_bar(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.FloatField()
    obj3 = models.CharField(max_length=30)
    def delete_all_records():
        objects_bar.objects.all().delete()

class pie_details(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.IntegerField()
    def delete_all_records():
        pie_details.objects.all().delete()

class objects_pie(models.Model):
    obj1 = models.CharField(max_length=30)
    obj2 = models.FloatField()
    obj3 = models.CharField(max_length=30)
    def delete_all_records():
        objects_pie.objects.all().delete()

class AllImageModel(models.Model):
    uname = models.CharField(max_length=50)
    image_field = models.ImageField(upload_to='images')
    timestamp = models.DateTimeField(auto_now_add=True)


class ImageModel(models.Model):
    image_field = models.ImageField(upload_to='images')
    timestamp = models.DateTimeField(auto_now_add=True)

    def delete_all_except_latest():
        # Get the latest record based on the timestamp
        latest_record = ImageModel.objects.latest('timestamp')

        # Delete all records except the latest one
        ImageModel.objects.exclude(pk=latest_record.pk).delete()


