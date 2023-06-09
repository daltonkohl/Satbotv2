# Generated by Django 3.2.18 on 2023-04-02 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('satbotTA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_title', models.CharField(max_length=255)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='satbotTA.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Class',
        ),
        migrations.AlterModelOptions(
            name='intent',
            options={'ordering': ['intent']},
        ),
        migrations.AddField(
            model_name='chat',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='satbotTA.course'),
        ),
        migrations.AddField(
            model_name='intent',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='satbotTA.course'),
        ),
    ]
