# Generated by Django 2.1.1 on 2018-12-04 23:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20181127_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidedesign',
            name='genome',
            field=models.CharField(choices=[('hg38', 'Homo sapiens - Human - UCSC Dec. 2013 (GRCh38/hg38)'), ('mm10', 'Mus musculus - Mouse - UCSC Dec. 2011 (GRCm38/mm10)')], default='hg38', max_length=80),
        ),
        migrations.AlterField(
            model_name='primerdesign',
            name='max_amplicon_length',
            field=models.IntegerField(default=400, help_text='Amplicon = primer product. Length after HDR insertion.', validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(800)], verbose_name='Maximum amplicon length'),
        ),
    ]
