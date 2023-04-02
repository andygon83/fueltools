# Generated by Django 4.1.7 on 2023-03-27 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('icao', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('iata', models.CharField(default='AAA', max_length=3)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='FuelPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supplier', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('note', models.TextField()),
                ('other_variable', models.DecimalField(decimal_places=2, max_digits=10)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fueler_price.airport')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='CustomerAirport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fueler_price.airport')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fueler_price.customer')),
            ],
        ),
    ]