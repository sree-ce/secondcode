# Generated by Django 4.0.1 on 2022-02-10 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminpanel', '0005_alter_product_price_alter_product_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='used',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='couponcode',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]