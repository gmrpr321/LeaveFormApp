# Generated by Django 4.2.4 on 2023-10-07 09:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('date_of_joining', models.DateField(null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_hod', models.BooleanField(default=False)),
                ('mentor', models.CharField(max_length=30, null=True)),
                ('class_incharge', models.CharField(max_length=30, null=True)),
                ('HOD', models.CharField(max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_study', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('date_from', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('date_to', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('section', models.CharField(max_length=2)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('student_dept', models.CharField(max_length=30, null=True)),
                ('parent_ph_no', models.CharField(max_length=10)),
                ('attendance_status', models.CharField(choices=[('LEAVE', 'LEAVE'), ('ON DUTY', 'ON DUTY')], max_length=20)),
                ('parent_consent', models.BooleanField(default=False)),
                ('staff_confirmation', models.BooleanField(default=False)),
                ('HOD_confirmation', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
