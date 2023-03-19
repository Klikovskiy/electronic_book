# Generated by Django 4.1.5 on 2023-02-08 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderExecutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_status', models.CharField(choices=[('CHECK', 'На проверке'), ('READY', 'Выполнено'), ('FINALIZE', 'Нужно доработать')], default='CHECK', max_length=50, verbose_name='Статус выполнения')),
                ('orde_exec_media', models.FileField(blank=True, null=True, upload_to='orde_exec/%Y/%m/%d/', verbose_name='Файл отчета распоряжения')),
                ('order_execution_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Текст отчета')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления записи')),
            ],
            options={
                'verbose_name': 'Выполнение распоряжения',
                'verbose_name_plural': 'Выполнение распоряжений',
                'ordering': ['date_update'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_date', models.DateField(verbose_name='Контрольная дата')),
                ('familiarization', models.BooleanField(default=False, null=True, verbose_name='Ознакомлен?')),
                ('familiarization_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата ознакомления')),
            ],
            options={
                'verbose_name': 'Распоряжение',
                'verbose_name_plural': 'Распоряжения',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='OrderTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_title', models.CharField(max_length=250, verbose_name='Название распоряжения')),
                ('order_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание распоряжения')),
            ],
            options={
                'verbose_name': 'Типы распоряжений',
                'verbose_name_plural': 'Типы распоряжений',
            },
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('position_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание должности')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ['name'],
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription_name', models.CharField(max_length=500, verbose_name='Название предписания')),
                ('prescription_media', models.ImageField(upload_to='prescription_media/%Y/%m/%d/', verbose_name='Файл предписания')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Предписание',
                'verbose_name_plural': 'Предписания',
                'ordering': ['date_create'],
            },
        ),
        migrations.CreateModel(
            name='PrescriptionTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription_type_name', models.CharField(max_length=250, verbose_name='Название предписания')),
                ('prescription_type_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание предписания')),
            ],
            options={
                'verbose_name': 'Типы предписания',
                'verbose_name_plural': 'Типы предписаний',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=500, verbose_name='Название участка')),
                ('region_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание участка')),
            ],
            options={
                'verbose_name': 'Участок',
                'verbose_name_plural': 'Участки',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('services_name', models.CharField(max_length=500, verbose_name='Название службы')),
            ],
            options={
                'verbose_name': 'Служба',
                'verbose_name_plural': 'Службы',
            },
        ),
        migrations.CreateModel(
            name='Subdivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subdivision_name', models.CharField(max_length=500, verbose_name='Название подразделения')),
                ('subdivision_description', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание подразделения')),
                ('region', models.ManyToManyField(related_name='subdivision_region', to='book_instructions.region', verbose_name='Участки')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
    ]
