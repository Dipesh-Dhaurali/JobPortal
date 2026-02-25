import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0001_initial'),
        ('hr', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateapplication',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.jobpost'),
        ),
        migrations.AddField(
            model_name='candidateapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='myapplyjoblist',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='candidate.candidateapplication'),
        ),
        migrations.AddField(
            model_name='myapplyjoblist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='candidateapplication',
            unique_together={('user', 'job')},
        ),
    ]
