# Generated by Django 2.0.1 on 2018-01-29 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('minutes', models.IntegerField(null=True)),
            ],
        ),
    ]
