# Generated by Django 4.0.1 on 2022-02-09 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_cart_caertdetails_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caertdetails',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.cart'),
        ),
    ]
