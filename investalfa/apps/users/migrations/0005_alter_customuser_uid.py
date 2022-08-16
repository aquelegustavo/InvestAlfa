# Generated by Django 4.1 on 2022-08-16 00:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_id_customuser_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]