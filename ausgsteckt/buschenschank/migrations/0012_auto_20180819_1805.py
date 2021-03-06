# Generated by Django 2.1 on 2018-08-19 16:05

import buschenschank.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('buschenschank', '0011_region_wikipedia_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date_start', models.DateField(help_text='First opened day', verbose_name='Start date')),
                ('date_end', models.DateField(help_text='Last opened day', verbose_name='End date')),
                ('buschenschank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buschenschank.Buschenschank', verbose_name='Buschenschank')),
            ],
            options={
                'verbose_name': 'Open date',
                'verbose_name_plural': 'Open dates',
                'ordering': ('date_end', 'date_start', 'buschenschank'),
            },
            bases=(models.Model, buschenschank.models.AdminURLMixin),
        ),
        migrations.AlterField(
            model_name='region',
            name='wikipedia_page',
            field=models.CharField(blank=True, help_text='Used to load description if none set', max_length=50, null=True, verbose_name='Wikipedia page'),
        ),
    ]
