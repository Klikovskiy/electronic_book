from django import forms
from django.forms import ModelForm

from book_instructions.models import (Prescription, Region, PrescriptionTypes,
                                      Orders, Positions,
                                      OrderExecutions, OrderTypes, Dispatchers)
from book_user.models import BookUser


class CreatePrescriptionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreatePrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['region'].widget = forms.Select(
            attrs={'class': 'form-control', })
        self.fields['region'].queryset = Region.objects.filter(
            pk__in=self.request.user.subdivision.region.all())
        self.fields['type_prescription'].widget = forms.Select(
            attrs={'class': 'form-control', })
        self.fields['type_prescription'].queryset = Positions.objects.get(
            pk=self.request.user.position_id).types.all()

    prescription_name = forms.CharField(label='Название предписания',
                                        required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', }))

    prescription_media = forms.ImageField(label='Файл предписания',
                                          widget=forms.FileInput(
                                              attrs={
                                                  'class': 'file-upload-input',
                                                  'onchange': 'readURL(this);',
                                                  'accept': 'image/*', }))

    class Meta:
        model = Prescription
        fields = ('prescription_name', 'region',
                  'type_prescription', 'prescription_media')


class EditPrescriptionForm(ModelForm):
    """
    Форма редактирования предписания.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EditPrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['region'].widget = forms.Select(
            attrs={'class': 'form-control', })
        self.fields['region'].queryset = Region.objects.filter(
            pk__in=self.request.user.subdivision.region.all())

    prescription_name = forms.CharField(label='Название предписания',
                                        required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', }))

    type_prescription = forms.ModelChoiceField(
        label='Тип предписания',
        queryset=PrescriptionTypes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    prescription_media = forms.ImageField(
        label='Файл предписания',
    )

    class Meta:
        model = Prescription
        fields = ('prescription_name', 'region',
                  'type_prescription', 'prescription_media')

from django.db.models import Q
class CreateOrdersForm(ModelForm):
    """
    Форма создание нового распоряжения.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.type_id = kwargs.pop('type_id')
        self.subdivision_id = kwargs.pop('subdivision_id')
        super(CreateOrdersForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.Select(
            attrs={'class': 'form-control', })
        self.fields['name'].queryset = PrescriptionTypes.objects.get(
            pk=self.type_id).types.all()
        self.fields['responsible_person'].widget = forms.Select(
            attrs={'class': 'form-control', })
        self.fields['responsible_person'].queryset = BookUser.objects.filter(Q(subdivision_id=self.subdivision_id) | Q(pk__in=Dispatchers.objects.values_list('services_person',)))

    control_date = forms.DateField(
        label='Контрольная дата выполнения',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date',
                   'class': 'form-control picker__input', }),
        required=True)

    class Meta:
        model = Orders
        fields = ('name', 'control_date', 'responsible_person')


class CreateOrderExecutionsForm(ModelForm):
    """
    Форма создание отчета в распоряжении.
    """

    order_execution_description = forms.CharField(label='Текст отчета',
                                                  required=False,
                                                  widget=forms.Textarea(
                                                      attrs={
                                                          'class': 'form-control',
                                                          'style': 'height: 200px'}))

    orde_exec_media = forms.FileField(label='Файл отчета распоряжения',
                                      required=False,
                                      widget=forms.FileInput(
                                          attrs={
                                              'class': 'file-upload-input',
                                              'onchange': 'readURL(this);',
                                              'accept': '*', }))

    class Meta:
        model = OrderExecutions
        fields = ('orde_exec_media', 'order_execution_description')


class UpdateOrderExecutionsForm(ModelForm):
    """
    Форма обновления отчета в распоряжении.
    """
    order_execution_description = forms.CharField(label='Текст отчета',
                                                  required=False,
                                                  widget=forms.Textarea(
                                                      attrs={
                                                          'class': 'form-control',
                                                          'style': 'height: 200px'}))

    orde_exec_media = forms.FileField(label='Файл отчета распоряжения',
                                      required=False,
                                      widget=forms.FileInput(
                                          attrs={
                                              'class': 'form-control',
                                              'onchange': 'readURL(this);',
                                              'accept': '*', }))

    class Meta:
        model = OrderExecutions
        fields = ('orde_exec_media', 'order_execution_description')


class CreateOrdersDispatcherForm(ModelForm):
    """
    Форма создание нового распоряжения диспетчеру.
    """

    name = forms.ModelChoiceField(
        label='Название предписания',
        queryset=OrderTypes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    responsible_person = forms.ModelChoiceField(
        label='Ответственное лицо',
        queryset=BookUser.objects.filter(pk__in=Dispatchers.objects.values_list('services_person',)),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    control_date = forms.DateField(
        label='Контрольная дата выполнения',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date',
                   'class': 'form-control picker__input', }),
        required=True)

    class Meta:
        model = Orders
        fields = ('name', 'control_date', 'responsible_person')


class CreateDispatcherPrescriptionForm(ModelForm):
    prescription_name = forms.CharField(label='Название предписания',
                                        required=True,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', }))

    type_prescription = forms.ModelChoiceField(
        label='Тип предписания',
        queryset=PrescriptionTypes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    dispatcher_user = forms.ModelChoiceField(
        label='Какому диспетчеру',
        queryset=Dispatchers.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    region = forms.ModelChoiceField(
        label='Участок',
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', })
    )

    prescription_media = forms.ImageField(label='Файл предписания',
                                          widget=forms.FileInput(
                                              attrs={
                                                  'class': 'file-upload-input',
                                                  'onchange': 'readURL(this);',
                                                  'accept': 'image/*', }))

    class Meta:
        model = Prescription
        fields = ('prescription_name', 'region',
                  'type_prescription', 'prescription_media', 'dispatcher_user')
