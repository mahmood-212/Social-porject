# Generated by Django 3.1 on 2022-03-01 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_personalpost'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='personalpost',
            unique_together=set(),
        ),
    ]
