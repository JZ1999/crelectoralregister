# Generated by Django 2.2.1 on 2019-05-09 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distelec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codele', models.CharField(max_length=6)),
                ('provincia', models.CharField(max_length=26)),
                ('canton', models.CharField(max_length=26)),
                ('distrito', models.CharField(max_length=26)),
            ],
        ),
        migrations.CreateModel(
            name='PatronElectoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=9)),
                ('codele', models.CharField(max_length=6)),
                ('sexo', models.IntegerField()),
                ('fechacaduc', models.CharField(max_length=8)),
                ('junta', models.CharField(max_length=5)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido1', models.CharField(max_length=26)),
                ('apellido2', models.CharField(max_length=26)),
            ],
        ),
    ]
