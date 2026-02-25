import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='candidateApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(choices=[('SEE', 'SEE (Secondary Education Examination)'), ('SLC', 'SLC (School Leaving Certificate)'), ('PLUS2', '+2 (Higher Secondary)'), ('DIPLOMA', 'Diploma'), ('BACHELOR', 'Bachelor'), ('MASTERS', 'Masters')], default='BACHELOR', max_length=20)),
                ('passingYear', models.CharField(choices=[('currently_running', 'Currently Running'), ('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000'), ('1999', '1999'), ('1998', '1998'), ('1997', '1997'), ('1996', '1996'), ('1995', '1995'), ('1994', '1994'), ('1993', '1993'), ('1992', '1992'), ('1991', '1991'), ('1990', '1990')], default='currently_running', max_length=20)),
                ('yearOfExp', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('resume', models.FileField(upload_to='resume')),
                ('support_documents', models.FileField(blank=True, help_text='Optional: Academic documents (PDF only, max 5MB)', null=True, upload_to='support_docs')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('shortlisted', 'shortlisted'), ('rejected', 'rejected'), ('selected', 'selected')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.FileField(blank=True, null=True, upload_to='candidate_photos/')),
                ('job_preference_title', models.CharField(help_text='e.g., Document Officer', max_length=200)),
                ('preferred_job_level', models.CharField(choices=[('top', 'Top Level'), ('senior', 'Senior Level'), ('mid', 'Mid Level'), ('junior', 'Junior/Entry Level'), ('internship', 'Internship')], max_length=20)),
                ('preferred_job_type', models.CharField(choices=[('fulltime', 'Full Time'), ('parttime', 'Part Time')], max_length=20)),
                ('work_experience', models.IntegerField(default=0)),
                ('education_level', models.CharField(choices=[('see', 'SEE (Secondary Education Examination)'), ('slc', 'SLC (School Leaving Certificate)'), ('plus2', '+2 (Higher Secondary)'), ('diploma', 'Diploma'), ('bachelor', 'Bachelor'), ('masters', 'Masters')], max_length=20)),
                ('course_or_program', models.CharField(help_text='e.g., BIM', max_length=200)),
                ('gpa_percentage_type', models.CharField(choices=[('gpa_4', 'GPA (out of 4)'), ('gpa_10', 'GPA (out of 10)'), ('percentage', 'Percentage (out of 100)')], max_length=10)),
                ('gpa_percentage_value', models.FloatField()),
                ('school_college_name', models.CharField(max_length=200)),
                ('graduation_year', models.CharField(choices=[('currently_running', 'Currently Running'), ('2030', '2030'), ('2029', '2029'), ('2028', '2028'), ('2027', '2027'), ('2026', '2026'), ('2025', '2025'), ('2024', '2024'), ('2023', '2023'), ('2022', '2022'), ('2021', '2021'), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013'), ('2012', '2012'), ('2011', '2011'), ('2010', '2010'), ('2009', '2009'), ('2008', '2008'), ('2007', '2007'), ('2006', '2006'), ('2005', '2005'), ('2004', '2004'), ('2003', '2003'), ('2002', '2002'), ('2001', '2001'), ('2000', '2000'), ('1999', '1999'), ('1998', '1998'), ('1997', '1997'), ('1996', '1996'), ('1995', '1995'), ('1994', '1994'), ('1993', '1993'), ('1992', '1992'), ('1991', '1991'), ('1990', '1990'), ('1989', '1989'), ('1988', '1988'), ('1987', '1987'), ('1986', '1986'), ('1985', '1985'), ('1984', '1984'), ('1983', '1983'), ('1982', '1982'), ('1981', '1981'), ('1980', '1980'), ('1979', '1979'), ('1978', '1978'), ('1977', '1977'), ('1976', '1976'), ('1975', '1975'), ('1974', '1974'), ('1973', '1973'), ('1972', '1972'), ('1971', '1971'), ('1970', '1970'), ('1969', '1969'), ('1968', '1968'), ('1967', '1967'), ('1966', '1966'), ('1965', '1965'), ('1964', '1964'), ('1963', '1963'), ('1962', '1962'), ('1961', '1961'), ('1960', '1960'), ('1959', '1959'), ('1958', '1958'), ('1957', '1957'), ('1956', '1956'), ('1955', '1955'), ('1954', '1954'), ('1953', '1953'), ('1952', '1952'), ('1951', '1951'), ('1950', '1950'), ('1949', '1949'), ('1948', '1948'), ('1947', '1947'), ('1946', '1946'), ('1945', '1945'), ('1944', '1944'), ('1943', '1943'), ('1942', '1942'), ('1941', '1941'), ('1940', '1940'), ('1939', '1939'), ('1938', '1938'), ('1937', '1937'), ('1936', '1936'), ('1935', '1935'), ('1934', '1934'), ('1933', '1933'), ('1932', '1932'), ('1931', '1931'), ('1930', '1930'), ('1929', '1929'), ('1928', '1928'), ('1927', '1927'), ('1926', '1926'), ('1925', '1925'), ('1924', '1924'), ('1923', '1923'), ('1922', '1922'), ('1921', '1921'), ('1920', '1920'), ('1919', '1919'), ('1918', '1918'), ('1917', '1917'), ('1916', '1916'), ('1915', '1915'), ('1914', '1914'), ('1913', '1913'), ('1912', '1912'), ('1911', '1911'), ('1910', '1910'), ('1909', '1909'), ('1908', '1908'), ('1907', '1907'), ('1906', '1906'), ('1905', '1905'), ('1904', '1904'), ('1903', '1903'), ('1902', '1902'), ('1901', '1901'), ('1900', '1900')], default='currently_running', max_length=20)),
                ('skills', models.TextField(help_text='e.g., Public Speaking, Computer Operation')),
                ('languages', models.TextField(help_text='e.g., Nepali, English')),
                ('social_account_name_1', models.CharField(blank=True, max_length=100, null=True)),
                ('social_account_url_1', models.URLField(blank=True, null=True)),
                ('social_account_name_2', models.CharField(blank=True, max_length=100, null=True)),
                ('social_account_url_2', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyApplyJobList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateYouApply', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Job Application Tracker',
                'verbose_name_plural': 'Job Application Trackers',
            },
        ),
        migrations.CreateModel(
            name='CandidateAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_status', models.CharField(choices=[('active', 'Active'), ('suspended', 'Suspended'), ('pending', 'Pending Verification'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('reason_for_suspension', models.TextField(blank=True, null=True)),
                ('suspended_at', models.DateTimeField(blank=True, null=True)),
                ('suspended_by', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Candidate Account',
                'verbose_name_plural': 'Candidate Accounts',
                'ordering': ('-created_at',),
            },
        ),
    ]
