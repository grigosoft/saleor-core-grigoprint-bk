# Generated by Django 3.2.5 on 2022-01-20 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0053_auto_20210719_1048'),
        ('accountGrigo', '0007_usergrigo_is_rappresentante'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraInfo',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='account.user')),
                ('denominazione', models.TextField(blank=True, null=True)),
                ('id_danea', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('account.user',),
        ),
    ]
