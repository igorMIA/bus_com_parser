# Generated by Django 2.2.3 on 2019-07-25 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inception', '0006_auto_20190723_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerattributes',
            name='player',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.DeleteModel(
            name='PlayerAttributes',
        ),
    ]
