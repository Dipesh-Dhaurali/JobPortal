from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            UPDATE hr_shortlistedcandidate 
            SET candidate_id = NULL 
            WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="""
            UPDATE hr_selectedcandidate 
            SET candidate_id = NULL 
            WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
