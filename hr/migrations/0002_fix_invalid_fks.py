from django.db import migrations

def fix_invalid_fks(apps, schema_editor):
    # Fix invalid foreign keys by setting them to NULL
    # This keeps all data safe - we're only fixing broken references
    with schema_editor.connection.cursor() as cursor:
        # Set invalid candidate_id values to NULL in hr_shortlistedcandidate
        cursor.execute("""
            UPDATE hr_shortlistedcandidate 
            SET candidate_id = NULL 
            WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication)
        """)
        
        # Set invalid candidate_id values to NULL in hr_selectedcandidate
        cursor.execute("""
            UPDATE hr_selectedcandidate 
            SET candidate_id = NULL 
            WHERE candidate_id NOT IN (SELECT id FROM hr_candidateapplication)
        """)

def reverse_fix(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_invalid_fks, reverse_fix),
    ]
