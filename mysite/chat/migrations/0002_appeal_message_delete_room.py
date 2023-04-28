# Generated by Django 4.2 on 2023-04-28 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название обращения')),
                ('priority', models.CharField(choices=[('св', 'Самый высокий'), ('вы', 'Высокий'), ('ср', 'Средний'), ('ни', 'Низкий')], default='Низкий', max_length=3)),
                ('text_appeal', models.TextField()),
                ('is_activate', models.BooleanField(verbose_name='Активно ли обращение')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('appeal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.appeal')),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]