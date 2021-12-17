# Generated by Django 3.2.6 on 2021-12-16 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20211216_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomeexpenseledgermodel',
            name='file',
        ),
        migrations.AddField(
            model_name='ledgerfile',
            name='ledger_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LedgerFile', to='accounting.incomeexpenseledgermodel'),
        ),
        migrations.AlterField(
            model_name='ledgerfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Income expense ledger file'),
        ),
    ]
