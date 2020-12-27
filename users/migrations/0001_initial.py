# Generated by Django 3.1.4 on 2020-12-27 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('surnames', models.CharField(blank=True, max_length=30)),
                ('birthday', models.DateField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('verified', models.BooleanField(default=False)),
                ('friends', models.ManyToManyField(blank=True, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Friend_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='users.user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='users.user')),
            ],
        ),
    ]
