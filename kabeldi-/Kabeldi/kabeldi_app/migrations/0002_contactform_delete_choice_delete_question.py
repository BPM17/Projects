# Generated by Django 5.0.6 on 2024-07-19 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kabeldi_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('cellphone', models.CharField(max_length=12)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]