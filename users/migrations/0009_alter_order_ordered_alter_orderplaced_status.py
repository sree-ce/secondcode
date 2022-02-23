# Generated by Django 4.0.1 on 2022-02-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_caertdetails_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.CharField(blank=True, choices=[('Placed', 'Placed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='pending', max_length=50),
        ),
    ]
