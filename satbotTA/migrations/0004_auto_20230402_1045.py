# Generated by Django 3.2.18 on 2023-04-02 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satbotTA', '0003_auto_20230402_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['course_title']},
        ),
        migrations.RenameField(
            model_name='course',
            old_name='class_title',
            new_name='course_title',
        ),
    ]
