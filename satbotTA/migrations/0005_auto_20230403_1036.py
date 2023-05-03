# Generated by Django 3.2.18 on 2023-04-03 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('satbotTA', '0004_auto_20230402_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='users', to='satbotTA.Course'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chats', to='satbotTA.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='instructors', to='satbotTA.user'),
        ),
        migrations.AlterField(
            model_name='incompletequestion',
            name='estimated_intent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incomplete_questions', to='satbotTA.intent'),
        ),
        migrations.AlterField(
            model_name='intent',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='intents', to='satbotTA.course'),
        ),
    ]