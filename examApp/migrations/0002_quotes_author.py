# Generated by Django 2.2.4 on 2020-08-24 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='author',
            field=models.CharField(max_length=45, null=True),
        ),
    ]