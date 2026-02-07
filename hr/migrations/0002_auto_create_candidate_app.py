# Generated migration to create candidateApplication model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='candidateApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('selected', 'Selected'), ('rejected', 'Rejected')], default='applied', max_length=20)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_applications', to='hr.jobpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
