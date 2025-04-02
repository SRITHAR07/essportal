# Generated by Django 5.0.11 on 2025-03-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ess', '0006_gennhraudit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.IntegerField(db_column='EmpID')),
                ('username', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='UserName', max_length=128)),
                ('fullname', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50)),
                ('plantcode', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50)),
                ('password', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='Password', max_length=128)),
                ('email', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='Email', max_length=128, null=True)),
                ('active', models.IntegerField()),
                ('comment', models.TextField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='Comment', null=True)),
                ('passwordquestion', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='PasswordQuestion', max_length=256, null=True)),
                ('passwordanswer', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='PasswordAnswer', max_length=128, null=True)),
                ('isapproved', models.BooleanField(blank=True, db_column='IsApproved', null=True)),
                ('lastactivitydate', models.DateTimeField(db_column='LastActivityDate')),
                ('lastlogindate', models.DateTimeField(db_column='LastLoginDate')),
                ('lastpasswordchangeddate', models.DateTimeField(db_column='LastPasswordChangedDate')),
                ('creationdate', models.DateTimeField(db_column='CreationDate')),
                ('islockedout', models.BooleanField(db_column='IsLockedOut')),
                ('lastlockedoutdate', models.DateTimeField(db_column='LastLockedOutDate')),
                ('failedpasswordattemptcount', models.IntegerField(db_column='FailedPasswordAttemptCount')),
                ('failedpasswordattemptwindowstart', models.DateTimeField(db_column='FailedPasswordAttemptWindowStart')),
                ('failedpasswordanswerattemptcount', models.IntegerField(db_column='FailedPasswordAnswerAttemptCount')),
                ('failedpasswordanswerattemptwindowstart', models.DateTimeField(db_column='FailedPasswordAnswerAttemptWindowStart')),
                ('usertype', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='Usertype', max_length=1)),
                ('orglevel', models.IntegerField(blank=True, db_column='Orglevel', null=True)),
                ('parentlevel', models.IntegerField(blank=True, db_column='Parentlevel', null=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='GennhrUsers',
        ),
    ]
