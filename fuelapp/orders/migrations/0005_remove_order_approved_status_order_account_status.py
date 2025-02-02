# Generated by Django 5.1.2 on 2024-10-30 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_order_approved_status_order_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="approved_status",
        ),
        migrations.AddField(
            model_name="order",
            name="account_status",
            field=models.CharField(
                choices=[("open", "Open"), ("closed", "Closed")],
                default="open",
                max_length=20,
            ),
        ),
    ]
