from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='required_experience',
            field=models.CharField(
                choices=[
                    ('no-experience', 'No experience required'),
                    ('6-months', '6 months'),
                    ('1-year', '1 year'),
                    ('2-years', '2 years'),
                    ('3-years', '3 years'),
                    ('4-years', '4 years'),
                    ('5-plus-years', '5+ years'),
                    ('others', 'Others')
                ],
                default='no-experience',
                help_text='Select required years of experience',
                max_length=50
            ),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='required_experience_custom',
            field=models.CharField(
                blank=True,
                help_text='Custom experience requirement (e.g., 1.5 years)',
                max_length=100,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='required_education',
            field=models.CharField(
                choices=[
                    ('no-education', 'No education required'),
                    ('see', 'SEE'),
                    ('slc', 'SLC'),
                    ('plus2', '+2'),
                    ('diploma', 'Diploma'),
                    ('bachelor', 'Bachelor'),
                    ('master', 'Master'),
                    ('phd', 'PhD')
                ],
                default='no-education',
                help_text='Select required education level',
                max_length=50
            ),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='required_skills',
            field=models.TextField(
                blank=True,
                help_text='Comma-separated skills (e.g., Python, SQL, Communication)',
                null=True
            ),
        ),
    ]
