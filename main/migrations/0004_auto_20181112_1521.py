# Generated by Django 2.1.1 on 2018-11-12 23:21

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181108_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidedesign',
            name='hdr_start_codon_tag_seq',
            field=models.CharField(blank=True, choices=[('ACCGAGCTCAACTTCAAGGAGTGGCAAAAGGCCTTTACCGATATGATGGGTGGCGGATTGGAAGTTTTGTTTCAAGGTCCAGGAAGTGGT', 'Neon Green - ACCGAGCTCAA...'), ('GACTACAAAGACGATGACGACAAG', 'FLAG - GACTACAAAGA...'), ('GACTACAAGGACCACGACGGTGACTACAAGGACCACGACATCGACTACAAGGACGACGACGACAAG', 'XFLAG - GACTACAAGGA...'), ('GGTAAGCCTATCCCTAACCCTCTCCTCGGTCTCGATTCTACG', 'V5 - GGTAAGCCTAT...'), ('TACCCATACGATGTTCCAGATTACGCT', 'HA - TACCCATACGA...'), (
                'GAACAAAAACTCATCTCAGAAGAGGATCTG', 'MYC - GAACAAAAACT...'), ('CGTGACCACATGGTCCTTCATGAGTATGTAAATGCTGCTGGGATTACAGGTGGCGGATTGGAAGTTTTGTTTCAAGGTCCAGGAAGTGGT', 'GFP11 - CGTGACCACAT...')], default=('ACCGAGCTCAACTTCAAGGAGTGGCAAAAGGCCTTTACCGATATGATGGGTGGCGGATTGGAAGTTTTGTTTCAAGGTCCAGGAAGTGGT', 'Neon Green - ACCGAGCTCAA...'), help_text='Sequence of tag to insert just after start codon', max_length=65536, validators=[utils.validators.validate_seq], verbose_name='Tag sequence for start codon'),
        ),
        migrations.AddField(
            model_name='guidedesign',
            name='hdr_stop_codon_tag_seq',
            field=models.CharField(blank=True, choices=[('GGTGGCGGATTGGAAGTTTTGTTTCAAGGTCCAGGAAGTGGTACCGAGCTCAACTTCAAGGAGTGGCAAAAGGCCTTTACCGATATGATG', 'Neon Green - GGTGGCGGATT...'), ('CTTGTCGTCATCGTCTTTGTAGTC', 'FLAG - CTTGTCGTCAT...'), ('CTTGTCGTCGTCGTCCTTGTAGTCGATGTCGTGGTCCTTGTAGTCACCGTCGTGGTCCTTGTAGTC', 'XFLAG - CTTGTCGTCGT...'), ('CGTAGAATCGAGACCGAGGAGAGGGTTAGGGATAGGCTTACC', 'V5 - CGTAGAATCGA...'), ('AGCGTAATCTGGAACATCGTATGGGTA', 'HA - AGCGTAATCTG...'), (
                'CAGATCCTCTTCTGAGATGAGTTTTTGTTC', 'MYC - CAGATCCTCTT...'), ('ACCACTTCCTGGACCTTGAAACAAAACTTCCAATCCGCCACCTGTAATCCCAGCAGCATTTACATACTCATGAAGGACCATGTGGTCACG', 'GFP11 - ACCACTTCCTG...')], default=('GGTGGCGGATTGGAAGTTTTGTTTCAAGGTCCAGGAAGTGGTACCGAGCTCAACTTCAAGGAGTGGCAAAAGGCCTTTACCGATATGATG', 'Neon Green - GGTGGCGGATT...'), help_text='Sequence of tag to insert just before stop codon', max_length=65536, validators=[utils.validators.validate_seq], verbose_name='Tag sequence for stop codon'),
        ),
    ]
