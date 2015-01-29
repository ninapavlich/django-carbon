# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atoms', '__first__'),
        ('clientset', '0008_auto_20150129_0426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientmedia',
            name='admin_note',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='allow_overwrite',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='clean_filename_on_upload',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='hierarchy',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='id',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='image',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='order',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='path',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='path_generated',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='path_override',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='permanent_redirect',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='template',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='temporary_redirect',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='title',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='clientmedia',
            name='version',
        ),
        migrations.AddField(
            model_name='clientmedia',
            name='secureimagemolecule_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='atoms.SecureImageMolecule'),
            preserve_default=False,
        ),
    ]
