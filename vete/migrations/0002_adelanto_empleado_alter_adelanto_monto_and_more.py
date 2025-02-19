# Generated by Django 5.0.4 on 2024-10-09 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vete', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adelanto',
            name='empleado',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='adelantos', to='vete.empleado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adelanto',
            name='Monto',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='sueldo',
            field=models.IntegerField(default=None),
        ),
        migrations.DeleteModel(
            name='EmpAde',
        ),
    ]
