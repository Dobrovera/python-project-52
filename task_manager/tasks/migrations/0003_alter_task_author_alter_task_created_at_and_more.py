# Generated by Django 4.2 on 2023-06-08 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statuses', '0002_alter_status_status_name'),
        ('labels', '0001_initial'),
        ('tasks', '0002_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='task_author_user',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='task_executor_user',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(
                to='labels.label',
                verbose_name='Метка'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to='statuses.status',
                verbose_name='Статус'),
        ),
    ]
