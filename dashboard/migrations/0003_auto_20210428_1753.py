# Generated by Django 3.1.7 on 2021-04-28 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20210424_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfile',
            old_name='file_name',
            new_name='file_loc',
        ),
        migrations.AddField(
            model_name='userfile',
            name='name',
            field=models.TextField(null=True),
        ),
    ]