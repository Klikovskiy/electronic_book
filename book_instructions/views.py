from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.views.generic.list import MultipleObjectMixin

from book_instructions.forms import (CreatePrescriptionForm,
                                     EditPrescriptionForm, CreateOrdersForm,
                                     CreateOrderExecutionsForm,
                                     UpdateOrderExecutionsForm,
                                     CreateOrdersDispatcherForm,
                                     CreateDispatcherPrescriptionForm)
from book_instructions.models import (Prescription, Subdivision,
                                      Services, Orders, OrderExecutions,
                                      PrescriptionTypes, Region, )
from book_instructions.utils import sending_engineer, paginator
from book_user.models import BookUser


class HomePage(LoginRequiredMixin, View):
    """
    Главная страница по умолчанию.
    """
    login_url = 'book_user:login'

    def get(self, request, *args, **kwargs):
        services_menu = Services.objects.all()
        return render(request, 'instructions/home_news.html',
                      context={'services_menu': services_menu})


class GetServices(PermissionRequiredMixin,
                  LoginRequiredMixin,
                  DetailView,
                  MultipleObjectMixin):
    """
    Служба и вывод в ней предписаний.
    """

    permission_required = 'book_instructions.view_services'
    model = Services
    template_name = 'instructions/prescription/view_services.html'
    context_object_name = 'view_services'
    allow_empty = True
    paginate_by = 20

    def get_context_data(self, **kwargs):
        _search_vals = {}
        region_request = self.request.GET.get('region')
        type_request = self.request.GET.get('type')
        star_date_request = self.request.GET.get('star_date')
        end_date_request = self.request.GET.get('end_date')

        if (region_request or type_request
                or star_date_request
                or end_date_request):
            if region_request:
                # участок
                region = Region.objects.get(pk=int(region_request)).pk
                _search_vals['region_id'] = region
            if type_request:
                # тип
                presc_types = PrescriptionTypes.objects.get(
                    pk=int(type_request)).pk
                _search_vals['type_prescription_id'] = presc_types
            if (self.request.GET.get('star_date')
                    and self.request.GET.get('end_date')):
                _search_vals['date_create__range'] = [
                    self.request.GET.get('star_date'),
                    self.request.GET.get('end_date')]

            prescriptions = Prescription.objects.filter(**_search_vals,
                                                        services_id=
                                                        self.kwargs['pk'])

        else:
            prescriptions = Prescription.objects.filter(
                subdivision_id=self.request.user.subdivision_id,
                region__in=self.request.user.subdivision.region.all(),
                type_prescription_id__in=self.request.user.position.types.all(),
                services_id=self.kwargs['pk'],

            )
        # Вычисляет статусы закрытия ордеров.
        status_executions = {}
        for related in prescriptions:
            related_need = len(related.related_prescription.all())
            related_counter = 0
            for order in related.related_prescription.all():
                for executions in order.order_execution.all():
                    if 'CHECK' in (executions.execution_status or 'FINALIZE'
                                   in executions.execution_status):
                        break
                    else:
                        related_counter = related_counter + 1
            if related_counter == related_need and related_counter > 0:
                status_executions[related.pk] = True
            else:
                status_executions[related.pk] = False

        context = {
            'prescription_list': prescriptions,
            'services_pk': self.kwargs['pk'],
            'status_executions': status_executions,
            'regions': Subdivision.objects.get(
                pk=self.request.user.subdivision.pk).region.all(),
            'types': PrescriptionTypes.objects.all(),

        }
        context.update(kwargs)
        return super().get_context_data(**context, object_list=prescriptions)


class GetServicesChief(PermissionRequiredMixin,
                       LoginRequiredMixin,
                       DetailView,
                       MultipleObjectMixin):
    """
    Служба и вывод предписаний для главы.
    """

    permission_required = 'book_instructions.view_services'
    model = Services
    template_name = 'instructions/prescription/view_services_chief.html'
    context_object_name = 'view_services_chief'
    allow_empty = True
    paginate_by = 20

    def get_context_data(self, **kwargs):
        _search_vals = {}
        region_request = self.request.GET.get('region')
        type_request = self.request.GET.get('type')
        subdivision_request = self.request.GET.get('subdivision')
        star_date_request = self.request.GET.get('star_date')
        end_date_request = self.request.GET.get('end_date')
        if (region_request or type_request
                or subdivision_request
                or star_date_request
                or end_date_request):
            if region_request:
                # участок
                region = Region.objects.get(pk=int(region_request)).pk
                _search_vals['region_id'] = region
            if type_request:
                # тип
                presc_types = PrescriptionTypes.objects.get(
                    pk=int(type_request)).pk
                _search_vals['type_prescription_id'] = presc_types
            if subdivision_request:
                # подразделение
                subdivision = Subdivision.objects.get(
                    pk=int(subdivision_request)).pk
                _search_vals['subdivision_id'] = subdivision
            if self.request.GET.get('star_date') and self.request.GET.get(
                    'end_date'):
                _search_vals['date_create__range'] = [
                    self.request.GET.get('star_date'),
                    self.request.GET.get('end_date')
                ]
            prescriptions = Prescription.objects.filter(**_search_vals,
                                                        services_id=
                                                        self.kwargs['pk'])
        else:
            prescriptions = Prescription.objects.filter(
                services_id=self.kwargs['pk'])

        # Вычисляет статусы закрытия ордеров.
        status_executions = {}
        for related in prescriptions:
            related_need = len(related.related_prescription.all())
            related_counter = 0
            for order in related.related_prescription.all():
                for executions in order.order_execution.all():
                    if 'CHECK' in (executions.execution_status or 'FINALIZE'
                                   in executions.execution_status):
                        break
                    else:
                        related_counter = related_counter + 1
            if related_counter == related_need and related_counter > 0:
                status_executions[related.pk] = True
            else:
                status_executions[related.pk] = False
        context = {
            'prescription_list': prescriptions,
            'services_pk': self.kwargs['pk'],
            'status_executions': status_executions,
            'regions': Region.objects.all(),
            'types': PrescriptionTypes.objects.all(),
            'subdivisions': Subdivision.objects.all(),
        }
        context.update(kwargs)
        return super().get_context_data(**context, object_list=prescriptions)


class PrescriptionList(PermissionRequiredMixin,
                       LoginRequiredMixin,
                       ListView):
    """
    Предписания.
    """

    permission_required = 'book_instructions.view_prescription'
    model = Prescription
    template_name = 'instructions/prescription/all_prescription.html'
    context_object_name = 'prescription_list'

    login_url = 'book_user:login'
    paginate_by = 20


class CreatePrescription(PermissionRequiredMixin,
                         LoginRequiredMixin,
                         CreateView):
    """
    Создание нового предписания.
    """

    permission_required = 'book_instructions.add_prescription'
    form_class = CreatePrescriptionForm
    template_name = 'instructions/prescription/create_prescription.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_services',
                            kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = {
            'subdivision': Subdivision.objects.get(
                pk=self.kwargs['pk']),
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.subdivision = Subdivision.objects.get(
            pk=self.request.user.subdivision_id)

        obj.services = Services.objects.get(id=self.kwargs['pk'])
        sending_engineer(request=self.request,
                         user=BookUser.objects.get(
                             pk=obj.subdivision.subdivision_engineer_id),
                         message_title='Поступило новое предписание',
                         message_tex=f'Предписание - {obj.prescription_name}, '
                                     f'Участок - {obj.region}, '
                                     f'Тип - {obj.type_prescription}'
                         )

        return super(CreatePrescription, self).form_valid(form)


class EditPrescription(PermissionRequiredMixin,
                       LoginRequiredMixin,
                       UpdateView):
    """
    Редактирование предписания.
    """

    permission_required = 'book_instructions.change_prescription'
    form_class = EditPrescriptionForm
    model = Prescription
    template_name = 'instructions/prescription/edit_prescription.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_services',
                            kwargs={'pk': self.kwargs['service_id']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class DelPrescription(PermissionRequiredMixin,
                      LoginRequiredMixin,
                      DeleteView):
    """
    Удалить предписание.
    """

    permission_required = 'book_instructions.delete_prescription'
    model = Prescription
    template_name = 'instructions/prescription/confirm_del.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_services',
                            kwargs={'pk': self.kwargs['service_id']})

    def get_context_data(self, **kwargs):
        context = {
            'services_pk': self.kwargs['service_id'],
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class GetPrescription(PermissionRequiredMixin,
                      LoginRequiredMixin,
                      DetailView,
                      MultipleObjectMixin):
    """
    Просмотр предписания.
    """

    permission_required = 'book_instructions.view_prescription'
    model = Prescription
    template_name = 'instructions/prescription/view_prescription.html'
    context_object_name = 'view_prescription'
    allow_empty = True
    paginate_by = 20

    def get_context_data(self, **kwargs):
        orders = Orders.objects.filter(prescription_id=self.kwargs['pk'])
        context = {
            'subdivision_engineer_id': Subdivision.objects.get(
                pk=kwargs["object"].subdivision_id).subdivision_engineer_id,

        }
        context.update(kwargs)
        return super().get_context_data(**context, object_list=orders)


class CreateOrders(PermissionRequiredMixin,
                   LoginRequiredMixin,
                   CreateView):
    """
    Создание нового распоряжения.
    """

    permission_required = 'book_instructions.add_orders'
    form_class = CreateOrdersForm
    template_name = 'instructions/orders/create_orders.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.prescription = Prescription.objects.get(
            pk=self.kwargs['orders_id'])
        sending_engineer(request=self.request,
                         user=obj.responsible_person,
                         message_title='Поступило новое распоряжение',
                         message_tex=f'Тип - {obj.name}, '
                                     f'Предписание - {obj.prescription}, '
                                     f'Контрольная дата - {obj.control_date}'
                         )
        return super(CreateOrders, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request,
                       'type_id': self.kwargs['type_id'],
                       'subdivision_id': self.kwargs['pk'],
                       }, )
        return kwargs

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_prescription',
                            kwargs={'pk': self.kwargs['orders_id']})


@login_required
@permission_required(
    'book_instructions.change_orders',
    'book_instructions.view_orders', raise_exception=True)
def orders_acquainted(request, orders_id, presc_id):
    """
    Ставит отметку о том, что пользователь ознакомился с распоряжением.
    """
    get_orders = get_object_or_404(Orders, pk=orders_id)
    if request.user.pk == get_orders.responsible_person_id:
        orders = Orders.objects.filter(pk=orders_id)
        orders.update(familiarization_date=datetime.now())
        orders.update(familiarization=True)
    return redirect('book_instructions:view_prescription', pk=presc_id)


@login_required
@permission_required([
    'book_instructions.view_orderexecutions',
    'book_instructions.change_orderexecutions',
], raise_exception=True)
def executions_finalize(request, executions_id, order_id):
    """
    Меняет статус отчета на "Доработать"
    """
    executions_stat = OrderExecutions.objects.get(pk=executions_id)
    user_id = Orders.objects.get(
        pk=executions_stat.order_execution_id).responsible_person_id
    subdivision_id = BookUser.objects.get(pk=user_id).subdivision_id
    if Subdivision.objects.get(
            pk=subdivision_id).subdivision_engineer_id == request.user.id:
        executions_stat = OrderExecutions.objects.filter(pk=executions_id)
        executions_stat.update(execution_status='FINALIZE')
    return redirect('book_instructions:view_order_executions',
                    pk=executions_id, order_id=order_id)


@login_required
@permission_required([
    'book_instructions.view_orderexecutions',
    'book_instructions.change_orderexecutions',
], raise_exception=True)
def executions_ready(request, executions_id, order_id):
    """
    Меняет статус отчета на "Выполнено"
    """
    executions_stat = OrderExecutions.objects.get(pk=executions_id)
    user_id = Orders.objects.get(
        pk=executions_stat.order_execution_id).responsible_person_id
    subdivision_id = BookUser.objects.get(pk=user_id).subdivision_id
    if Subdivision.objects.get(
            pk=subdivision_id).subdivision_engineer_id == request.user.id:
        executions_stat = OrderExecutions.objects.filter(pk=executions_id)
        executions_stat.update(execution_status='READY')
    return redirect('book_instructions:view_order_executions',
                    pk=executions_id, order_id=order_id)


class CreateOrderExecutions(PermissionRequiredMixin,
                            LoginRequiredMixin,
                            CreateView):
    """
    Создание отчета о выполнении распоряжения.
    """

    permission_required = 'book_instructions.add_orderexecutions'
    form_class = CreateOrderExecutionsForm
    template_name = 'instructions/prescription/create_order_executions.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            order_executions = OrderExecutions.objects.get(
                order_execution_id=self.kwargs['order_id'])
            if order_executions:
                return redirect('book_instructions:view_order_executions',
                                pk=order_executions.pk,
                                order_id=self.kwargs['order_id'])
        except ObjectDoesNotExist:
            pass
        context = {
            'orders': Orders.objects.get(pk=self.kwargs['order_id']),
        }
        context.update(kwargs)
        return super(CreateOrderExecutions, self).dispatch(request, *args,
                                                           **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.order_execution = Orders.objects.get(pk=self.kwargs['order_id'])
        if obj.orde_exec_media or obj.order_execution_description:
            return super(CreateOrderExecutions, self).form_valid(form)
        return super(CreateOrderExecutions, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_prescription',
                            kwargs={'pk': self.kwargs['presc_id']})


class GetOrderExecutions(PermissionRequiredMixin,
                         LoginRequiredMixin,
                         DetailView):
    """
    Просмотр отчета распоряжения.
    """

    permission_required = 'book_instructions.view_orderexecutions'
    model = OrderExecutions
    template_name = 'instructions/prescription/view_order_executions.html'
    context_object_name = 'view_order_executions'
    allow_empty = True

    def get_context_data(self, **kwargs):
        executions_stat = OrderExecutions.objects.get(pk=self.kwargs['pk'])
        user_id = Orders.objects.get(
            pk=executions_stat.order_execution_id).responsible_person_id
        subdivision_id = BookUser.objects.get(pk=user_id).subdivision_id
        request_user_id = self.request.user.id
        if Subdivision.objects.get(
                pk=subdivision_id).subdivision_engineer_id == request_user_id:
            finalize_button = True
        else:
            finalize_button = False
        if user_id == request_user_id:
            edit_button = True
        else:
            edit_button = False

        context = {
            'finalize_button': finalize_button,
            'edit_button': edit_button,
            'orders_executions_pk': self.kwargs['pk']

        }
        context.update(kwargs)
        return super().get_context_data(**context)


class EditOrderExecutions(PermissionRequiredMixin,
                          LoginRequiredMixin,
                          UpdateView):
    """
    Доработка/редактирование отчета.
    """

    permission_required = 'book_instructions.change_orderexecutions'
    model = OrderExecutions
    form_class = UpdateOrderExecutionsForm
    template_name = 'instructions/prescription/edit_order_executions.html'

    def render_to_response(self, context, **response_kwargs):
        if self.object.execution_status == 'READY':
            print(self.kwargs)
            return redirect('book_instructions:view_order_executions',
                            pk=self.kwargs['pk'],
                            order_id=self.kwargs['presc_id'])
        return super(EditOrderExecutions, self).render_to_response(
            context, **response_kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.order_execution = Orders.objects.get(pk=self.kwargs['presc_id'])
        obj.execution_status = 'CHECK'
        return super(EditOrderExecutions, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_order_executions',
                            kwargs={'pk': self.kwargs['pk'],
                                    'order_id': self.kwargs['presc_id'], })


class DispatcherServices(PermissionRequiredMixin,
                         LoginRequiredMixin,
                         ListView,
                         MultipleObjectMixin):
    """
    Предписания диспетчера.
    """

    permission_required = 'book_instructions.view_dispatchers'
    model = Prescription
    template_name = 'instructions/dispatchers/view_dispatchers.html'
    context_object_name = 'view_dispatchers'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        dispatcher = Prescription.objects.filter(
            dispatcher_user=self.request.user.dispatcher_user)
        context = {
            'page_dispatcher': paginator(self.request, dispatcher),
        }
        context.update(kwargs)

        return super().get_context_data(**context)


class EditDispatcherPrescription(PermissionRequiredMixin,
                                 LoginRequiredMixin,
                                 UpdateView):
    """
    Редактирование предписания диспетчера.
    """

    permission_required = 'book_instructions.change_dispatchers'
    form_class = EditPrescriptionForm
    model = Prescription
    template_name = 'instructions/prescription/edit_prescription.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_dispatchers')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class DelDispatcherPrescription(PermissionRequiredMixin,
                                LoginRequiredMixin,
                                DeleteView):
    """
    Удалить предписание диспетчера.
    """

    permission_required = 'book_instructions.delete_dispatchers'
    model = Prescription
    template_name = 'instructions/dispatchers/confirm_del.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_dispatchers')


class GetDispatcherPrescription(PermissionRequiredMixin,
                                LoginRequiredMixin,
                                DetailView,
                                MultipleObjectMixin):
    """
    Просмотр предписания диспетчера.
    """

    permission_required = 'book_instructions.view_dispatchers'
    model = Prescription
    template_name = 'instructions/dispatchers/view_prescription_dispatchers.html'
    context_object_name = 'view_prescription_dispatchers'
    allow_empty = True
    paginate_by = 20

    def get_context_data(self, **kwargs):
        orders = Orders.objects.filter(prescription_id=self.kwargs['pk'])

        context = {
            'subdivision_engineer_id': (self.request.user.dispatcher_user
                                        .subdivision.get()
                                        .subdivision_engineer_id),

        }
        context.update(kwargs)
        return super().get_context_data(**context, object_list=orders)


@login_required
@permission_required(
    'book_instructions.change_orders',
    'book_instructions.view_orders', raise_exception=True)
def orders_acquainted_dispatcher(request, orders_id, presc_id):
    """
    Ставит отметку о том, что диспетчер ознакомился с распоряжением.
    """
    get_orders = get_object_or_404(Orders, pk=orders_id)
    if request.user.pk == get_orders.responsible_person_id:
        orders = Orders.objects.filter(pk=orders_id)
        orders.update(familiarization_date=datetime.now())
        orders.update(familiarization=True)
    return redirect('book_instructions:view_prescription_dispatchers',
                    pk=presc_id)


class CreateDispatcherOrders(PermissionRequiredMixin,
                             LoginRequiredMixin,
                             CreateView):
    """
    Создание нового распоряжения диспетчеру.
    """

    permission_required = 'book_instructions.add_orders'
    form_class = CreateOrdersDispatcherForm
    template_name = 'instructions/dispatchers/create_orders.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.prescription = Prescription.objects.get(pk=self.kwargs['pk'])
        return super(CreateDispatcherOrders, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_dispatchers')


class CreateDispatcherPrescription(PermissionRequiredMixin,
                                   LoginRequiredMixin,
                                   CreateView):
    """
    Создание нового предписания диспетчеру.
    """

    permission_required = 'book_instructions.add_dispatchers'
    form_class = CreateDispatcherPrescriptionForm
    template_name = 'instructions/dispatchers/create_dispatchers_prescription.html'

    def get_success_url(self):
        return reverse_lazy('book_instructions:view_dispatchers')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        sending_engineer(request=self.request,
                         user=BookUser.objects.get(
                             pk=obj.dispatcher_user.services_person_id)
                         ,
                         message_title='Поступило новое предписание',
                         message_tex=f'Предписание - {obj.prescription_name}, '
                                     f'Участок - {obj.region}, '
                                     f'Тип - {obj.type_prescription}'
                         )

        return super(CreateDispatcherPrescription, self).form_valid(form)
