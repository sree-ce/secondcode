# Generated by Django 4.0.1 on 2022-02-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_order_delivered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
