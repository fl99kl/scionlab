# Generated by Django 3.0.7 on 2020-12-08 10:34

from django.db import migrations, models
import django.db.models.deletion


def migrate_key():
    return [
        migrations.AlterField(
            model_name='key',
            name='key',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='key',
            name='usage',
            field=models.CharField(choices=[('sensitive-voting', 'sensitive-voting'),
                                            ('regular-voting', 'regular-voting'),
                                            ('cp-root', 'cp-root'),
                                            ('cp-ca', 'cp-ca'),
                                            ('cp-as', 'cp-as')], editable=False, max_length=32),
        ),
    ]


def migrate_certificate():
    return [
        migrations.AddField(
            model_name='certificate',
            name='ca_cert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issued_certificates', to='scionlab.Certificate'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='scionlab.Key'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='certificate',
            field=models.TextField(editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='certificate',
            unique_together={('key', 'version')},
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='AS',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='type',
        ),
    ]


def migrate_trc():
    return [
        migrations.AddField(
            model_name='trc',
            name='base_version',
            field=models.PositiveIntegerField(default=1, editable=False),
        ),
        migrations.AddField(
            model_name='trc',
            name='core_ases',
            field=models.ManyToManyField(related_name='trcs_attesting_core_as', to='scionlab.AS'),
        ),
        migrations.AddField(
            model_name='trc',
            name='quorum',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='trc',
            name='serial_version',
            field=models.PositiveIntegerField(default=1, editable=False),
        ),
        migrations.AddField(
            model_name='trc',
            name='signatures',
            field=models.ManyToManyField(related_name='trc_signatures', to='scionlab.Certificate'),
        ),
        migrations.AddField(
            model_name='trc',
            name='votes',
            field=models.ManyToManyField(related_name='trc_votes', to='scionlab.Certificate'),
        ),
        migrations.AlterField(
            model_name='trc',
            name='trc',
            field=models.TextField(editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='trc',
            unique_together={('isd', 'serial_version', 'base_version')},
        ),
        migrations.RemoveField(
            model_name='trc',
            name='version',
        ),
        migrations.RemoveField(
            model_name='trc',
            name='voting_offline',
        ),migrations.AddField(
            model_name='trc',
            name='certificates',
            field=models.ManyToManyField(related_name='trc_included', to='scionlab.Certificate'),
        ),
    ]


def create_as_pki(apps, schema_editor):
    from scionlab.models.core import ISD

    for isd in ISD.objects.all():
        isd.update_trc_and_certificates()


def bump_config(apps, schema_editor):
    # Host = apps.get_model('scionlab', 'Host')
    from scionlab.models.core import Host
    Host.objects.bump_config()


class Migration(migrations.Migration):

    dependencies = [
        ('scionlab', '0007_new_cppki'),
    ]

    operations = [
        *migrate_key(),
        *migrate_certificate(),
        *migrate_trc(),
        migrations.RunPython(create_as_pki),
        migrations.RunPython(bump_config),
    ]
