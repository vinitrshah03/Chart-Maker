# Generated by Django 4.2.3 on 2024-03-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0003_bar_details_line_details_objects_bar_objects_line_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=50)),
                ('image_field', models.ImageField(upload_to='images')),
            ],
        ),
    ]
