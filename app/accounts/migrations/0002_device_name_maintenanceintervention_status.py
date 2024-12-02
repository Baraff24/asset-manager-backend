# Generated by Django 5.1.2 on 2024-12-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.CharField(default='Dispositivo Sconosciuto', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maintenanceintervention',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', max_length=50),
        ),
    ]