from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .models import (Subdivision, Positions, Region, PrescriptionTypes,
                     Prescription, Orders, OrderTypes, OrderExecutions,
                     Services, Dispatchers)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name', 'get_name', 'get_email')

    def get_name(self, obj):
        middle_name = (f'{obj.chief.last_name} '
                       f'{obj.chief.first_name}')
        return middle_name

    get_name.admin_order_field = 'user_name'
    get_name.short_description = 'Начальник участка'

    def get_email(self, obj):
        return obj.chief.email

    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email начальника'

    empty_value_display = '-пусто-'


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_name', 'get_name', 'get_email',
                    'services', 'subdivision', 'date_create')
    list_filter = ('region', 'type_prescription',
                   'date_create', 'subdivision')

    def get_name(self, obj):
        middle_name = (f'{obj.author.last_name} '
                       f'{obj.author.first_name}')
        return middle_name

    get_name.admin_order_field = 'user_name'
    get_name.short_description = 'Автор предписания'

    def get_email(self, obj):
        return obj.author.email

    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email автора'

    empty_value_display = '-пусто-'


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_name', 'get_email',
                    'prescription', 'familiarization', 'control_date')

    def get_name(self, obj):
        middle_name = (f'{obj.responsible_person.last_name} '
                       f'{obj.responsible_person.first_name}')
        return middle_name

    get_name.admin_order_field = 'user_name'
    get_name.short_description = 'Ответственное  лицо'

    def get_email(self, obj):
        return obj.responsible_person.email

    get_email.admin_order_field = 'email'
    get_email.short_description = 'Email автора'


class OrderExecutionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'execution_status', 'order_execution',
                    'date_update')


admin.site.unregister(Group)
admin.site.register(Region, RegionAdmin)  # Участок
admin.site.register(Positions, GroupAdmin)  # Должность
admin.site.register(Subdivision, )  # Подразделения
admin.site.register(PrescriptionTypes, )  # Типы предписаний
admin.site.register(Prescription, PrescriptionAdmin)  # Предписания
admin.site.register(Orders, OrdersAdmin)  # Распоряжения
admin.site.register(OrderTypes, )  # Распоряжения
admin.site.register(OrderExecutions,
                    OrderExecutionsAdmin)  # Выполнение распоряжения
admin.site.register(Services, )  # Службы
admin.site.register(Dispatchers, )
