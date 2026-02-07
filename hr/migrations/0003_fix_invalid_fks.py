# Data migration to fix invalid foreign keys

from django.db import migrations


def fix_invalid_fks(apps, schema_editor):
    """Set invalid candidate_id references to NULL"""
    if schema_editor.connection.vendor == 'sqlite':
        with schema_editor.connection.cursor() as cursor:
            # Fix ShortlistedCandidate records with invalid candidate_id
            cursor.execute("""
                UPDATE hr_shortlistedcandidate 
                SET candidate_id = NULL 
                WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication) 
                AND candidate_id IS NOT NULL
            """)
            
            # Fix SelectedCandidate records with invalid candidate_id
            cursor.execute("""
                UPDATE hr_selectedcandidate 
                SET candidate_id = NULL 
                WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication)
                AND candidate_id IS NOT NULL
            """)


def reverse_fix(apps, schema_editor):
    """No reverse operation needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_create_candidate_app'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_fks, reverse_fix),
    ]
