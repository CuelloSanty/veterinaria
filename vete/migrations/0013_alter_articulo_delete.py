# Generated by Django 5.0.4 on 2025-03-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vete', '0012_articulo_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='delete',
            field=models.BooleanField(default=False),
        ),
    ]
