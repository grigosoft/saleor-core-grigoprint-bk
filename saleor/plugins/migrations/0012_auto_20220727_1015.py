# Generated by Django 3.2.5 on 2022-07-27 10:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prodottoPersonalizzato', '0004_auto_20220628_1451'),
        ('accountGrigo', '0024_auto_20220723_1244'),
        ('plugins', '0011_auto_20220727_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='ferie',
            name='approvate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ferie',
            name='data_fine',
            field=models.DateField(default='2022-05-05'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ferie',
            name='data_inizio',
            field=models.DateField(default='2022-05-05'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ferie',
            name='info_approvazione',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='ferie',
            name='motivazione',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='ferie',
            name='ore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='notifica',
            name='completata',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notifica',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notifica',
            name='mittente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_NULL, related_name='notifiche', to='accountGrigo.userextra'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifica',
            name='scadenza',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notifica',
            name='testo',
            field=models.TextField(default='testo default'),
        ),
        migrations.AddField(
            model_name='notifica',
            name='titolo',
            field=models.TextField(default='Nuova notifica'),
        ),
        migrations.AddField(
            model_name='settore',
            name='denominazione',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settore',
            name='info',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='tempipersonalizzazionesettore',
            name='data',
            field=models.DateField(default='2022-05-05'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tempipersonalizzazionesettore',
            name='ore_lavoro',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tempipersonalizzazionesettore',
            name='personalizzazione',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tempi_settore', to='prodottoPersonalizzato.personalizzazione'),
            preserve_default=False,
        ),
    ]
