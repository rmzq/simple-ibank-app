# Generated by Django 3.1.6 on 2021-02-17 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210217_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riwayat',
            name='penerima',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terima', to='main.rekening'),
        ),
    ]
