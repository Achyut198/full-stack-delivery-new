# Generated by Django 5.1.2 on 2024-10-23 20:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0002_issue_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='name',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='owner_name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='plate_number',
            field=models.CharField(default=0, max_length=10, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('issue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repairs.issue')),
            ],
        ),
    ]