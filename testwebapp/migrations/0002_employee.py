# Generated by Django 2.0 on 2018-02-02 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testwebapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('pss', models.CharField(max_length=200)),
            ],
        ),
    ]
