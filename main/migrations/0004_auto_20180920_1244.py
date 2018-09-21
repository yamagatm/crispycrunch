# Generated by Django 2.1.1 on 2018-09-20 19:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180918_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='fastqs',
        ),
        migrations.AddField(
            model_name='analysis',
            name='fastq_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='experiment',
            field=models.ForeignKey(help_text='The Crispycrunch experiment to be analyzed', on_delete=django.db.models.deletion.PROTECT, to='main.Experiment'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='s3_bucket',
            field=models.CharField(default='ryan.leenay-bucket', help_text='The Amazon S3 bucket that contains the FastQ files to be analyzed', max_length=80),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='s3_prefix',
            field=models.CharField(default='Greg_CXCR4_iPSC', help_text='The S3 directory that contains the FastQ files to be analyzed', max_length=160),
        ),
    ]
