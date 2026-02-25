from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Type & Verification', 'verbose_name_plural': 'User Types & Verification'},
        ),
    ]
