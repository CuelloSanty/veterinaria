# Generated by Django 5.0.4 on 2024-10-10 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vete', '0002_adelanto_empleado_alter_adelanto_monto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedore',
            fields=[
                ('cuit', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('img', models.URLField(blank=True, max_length=655, null=True)),
                ('marca', models.CharField(max_length=30)),
                ('peso', models.DecimalField(blank=True, decimal_places=3, default=None, max_digits=5, null=True)),
                ('talle', models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=2, null=True)),
                ('vencimiento', models.DateField(blank=True, default=None, null=True)),
                ('unidad', models.CharField(choices=[('Bol', 'Bolsa'), ('Caj', 'Caja'), ('Sob', 'Sobre'), ('Com', 'Comprimido'), ('Uni', 'Unidad'), ('Kil', 'Kilos'), ('Gra', 'Gramos'), ('Mil', 'Mililitros'), ('Lit', 'Litros'), ('Otro', 'Otro')], default='Alim', max_length=5)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_minimo', models.IntegerField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('Med', 'Medicamento'), ('Alim', 'Alimento'), ('Acc', 'Accesorio')], default='Med', max_length=5)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Articulos', to='vete.proveedore')),
            ],
        ),
    ]
