from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    """
    Участок.
    """

    region_name = models.CharField(
        verbose_name='Название участка',
        max_length=500,
        blank=False,
    )

    region_description = models.TextField(
        verbose_name='Описание участка',
        max_length=1500,
        null=True,
        blank=True,
    )

    chief = models.ForeignKey('book_user.BookUser',
                              on_delete=models.CASCADE,
                              verbose_name='Начальник участка',
                              blank=False)

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'


class PositionsManager(models.Manager):
    def get_query_set(self):
        return super(PositionsManager, self).get_query_set().filter(
            student__enrolled=True).distinct()


class Positions(Group):
    """
    Должность.
    """
    position_description = models.TextField(
        verbose_name='Описание должности',
        max_length=1500,
        null=True,
        blank=True,
    )

    types = models.ManyToManyField('PrescriptionTypes',
                                   verbose_name='Типы предписаний',
                                   related_name='prescription_types')

    objects = models.Manager()
    has_students = PositionsManager()

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Subdivision(models.Model):
    """
    Подразделения.
    """

    subdivision_name = models.CharField(
        verbose_name='Название подразделения',
        max_length=500,
        blank=False,
    )

    subdivision_description = models.TextField(
        verbose_name='Описание подразделения',
        max_length=1500,
        null=True,
        blank=True,
    )

    subdivision_engineer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                             on_delete=models.CASCADE,
                                             verbose_name='Инженер подразделения',
                                             related_name='engineer')

    subdivision_specialist = models.ForeignKey(Positions,
                                               on_delete=models.CASCADE,
                                               null=True,
                                               blank=True,
                                               verbose_name='Специалист',
                                               related_name='specialist')

    region = models.ManyToManyField(Region, verbose_name='Участки',
                                    related_name='subdivision_region')

    def __str__(self):
        return self.subdivision_name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class PrescriptionTypes(models.Model):
    """
    Типы предписаний.
    """

    prescription_type_name = models.CharField(
        verbose_name='Название предписания',
        max_length=250,
        blank=False,
    )

    prescription_type_description = models.TextField(
        verbose_name='Описание предписания',
        max_length=1500,
        null=True,
        blank=True,
    )

    types = models.ManyToManyField('OrderTypes',
                                   verbose_name='Доступные типы распоряжений',
                                   related_name='order_types')

    def __str__(self):
        return self.prescription_type_name

    class Meta:
        verbose_name = 'Типы предписания'
        verbose_name_plural = 'Типы предписаний'


class Prescription(models.Model):
    """
    Предписания.
    """

    prescription_name = models.CharField(
        verbose_name='Название предписания',
        max_length=500,
        blank=False
    )
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               verbose_name='Участок')

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name='Кто составил предписание')

    prescription_media = models.ImageField(verbose_name='Файл предписания',
                                           upload_to='prescription_media/%Y/%m/%d/')

    # Зависят от должности.
    type_prescription = models.ForeignKey(PrescriptionTypes,
                                          on_delete=models.CASCADE,
                                          verbose_name='Тип предписания')

    subdivision = models.ForeignKey(Subdivision,
                                    on_delete=models.CASCADE,
                                    verbose_name='Подразделение',
                                    blank=True,
                                    null=True,
                                    )

    services = models.ForeignKey('Services',
                                 on_delete=models.CASCADE,
                                 verbose_name='К какой службе',
                                 blank=True,
                                 null=True,
                                 )

    date_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')

    def __str__(self):
        return self.prescription_name

    class Meta:
        verbose_name = 'Предписание'
        verbose_name_plural = 'Предписания'
        ordering = ['date_create']


class Orders(models.Model):
    """
    Распоряжения.
    """

    name = models.ForeignKey('OrderTypes',
                             on_delete=models.CASCADE,
                             verbose_name='Тип распоряжения')
    prescription = models.ForeignKey('Prescription',
                                     on_delete=models.CASCADE,
                                     verbose_name='Предписание',
                                     null=False,
                                     related_name='related_prescription')
    control_date = models.DateField(verbose_name='Контрольная дата', )
    responsible_person = models.ForeignKey('book_user.BookUser',
                                           on_delete=models.CASCADE,
                                           verbose_name='Ответственное  лицо',
                                           null=False, )
    familiarization = models.BooleanField(default=False,
                                          verbose_name='Ознакомлен?',
                                          null=True, )
    familiarization_date = models.DateTimeField(
        verbose_name='Дата ознакомления',
        null=True,
        blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Распоряжение'
        verbose_name_plural = 'Распоряжения'
        ordering = ['-pk']


class OrderTypes(models.Model):
    """
    Типы распоряжений и описание.
    """

    order_title = models.CharField(
        verbose_name='Название распоряжения',
        max_length=250,
        blank=False,
    )

    order_description = models.TextField(
        verbose_name='Описание распоряжения',
        max_length=1500,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.order_title

    class Meta:
        verbose_name = 'Типы распоряжений'
        verbose_name_plural = 'Типы распоряжений'


class OrderExecutions(models.Model):
    """
    Выполнение распоряжения.
    """

    class StatusOrderExecution(models.TextChoices):
        WORK_CHECK = 'CHECK', _('На проверке')
        WORK_READY = 'READY', _('Выполнено')
        WORK_FINALIZE = 'FINALIZE', _('Нужно доработать')

    execution_status = models.CharField(
        verbose_name='Статус выполнения',
        max_length=50,
        choices=StatusOrderExecution.choices,
        default=StatusOrderExecution.WORK_CHECK,
    )
    orde_exec_media = models.FileField(verbose_name='Файл отчета распоряжения',
                                       upload_to='orde_exec/%Y/%m/%d/',
                                       null=True,
                                       blank=True)

    order_execution = models.ForeignKey('Orders',
                                        on_delete=models.CASCADE,
                                        verbose_name='Распоряжение',
                                        null=True,
                                        blank=True,
                                        related_name='order_execution')

    order_execution_description = models.TextField(
        verbose_name='Текст отчета',
        max_length=1500,
        null=True,
        blank=True,
    )

    date_update = models.DateTimeField(verbose_name='Дата обновления записи',
                                       auto_now=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Выполнение распоряжения'
        verbose_name_plural = 'Выполнение распоряжений'
        ordering = ['date_update']


class Services(models.Model):
    """
    Службы.
    """

    services_name = models.CharField(
        verbose_name='Название службы',
        max_length=500,
        blank=False
    )

    subdivision = models.ForeignKey(Subdivision,
                                    on_delete=models.CASCADE,
                                    verbose_name='Подразделение',
                                    related_name='services_subdivision')

    services_person = models.ForeignKey('book_user.BookUser',
                                        on_delete=models.CASCADE,
                                        verbose_name='Начальник службы',
                                        null=False, )

    def __str__(self):
        return self.services_name

    class Meta:
        verbose_name = 'Служба'
        verbose_name_plural = 'Службы'


class Dispatchers(models.Model):
    """
    Диспетчера.
    """

    order_title = models.CharField(
        verbose_name='Название диспетчера',
        max_length=250,
        blank=False,
    )

    services_person = models.OneToOneField(
        'book_user.BookUser',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=False,
        related_name='dispatcher_user'
    )
    subdivision = models.ManyToManyField(
        Subdivision,
        verbose_name='Подразделение инженера'
    )

    def __str__(self):
        return self.order_title

    class Meta:
        verbose_name = 'Диспетчер'
        verbose_name_plural = 'Диспетчера'
