# Generated by Django 4.0.5 on 2022-06-20 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DynamicTextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=10)),
                ('value', models.TextField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dynamic_text_fields', to='contents.content')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
