# Generated by Django 2.1.1 on 2018-11-28 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20181127_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidedesign',
            name='hdr_tag',
            field=models.CharField(blank=True, choices=[('start_codon', 'Within 96 before or after start codon (N-terminus)'), ('stop_codon', 'Within 96 before or after stop codon (C-terminus)'), ('per_target', 'Within 96 before or after, terminus specified per target ("N" or "C")')], help_text='Where to insert the tag in each gene', max_length=40, null=True, verbose_name='HDR tag terminus'),
        ),
    ]