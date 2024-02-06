from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
)

from src.services.lucky_draw.models import Event, Participant, Result
# from faker_data import initialization
from src.services.users.models import User
from src.web.admins.filters import UserFilter, EventFilter

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        events = Event.objects.all()
        running_events = Event.objects.filter(status='published')

        context['events_running'] = running_events
        context['e_total'] = events.count()
        context['e_pending'] = events.filter(status='draft').count()
        context['e_running'] = running_events.count()
        context['e_completed'] = events.filter(status='completed').count()
        context['e_cancelled'] = events.filter(status='cancelled').count()

        return context


""" USERS """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})


"""  """


@method_decorator(admin_decorators, name='dispatch')
class EventListView(ListView):
    queryset = Event.objects.all()
    template_name = 'admins/event_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        _filter = EventFilter(self.request.GET, queryset=self.queryset)
        context['filter_form'] = _filter.form

        paginator = Paginator(_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['object_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'admins/event_form.html'

    def get_success_url(self):
        return reverse('admins:event-detail', kwargs={'pk': self.object.id})


@method_decorator(admin_decorators, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    template_name = 'admins/event_form.html'

    def get_success_url(self):
        return reverse('admins:event-detail', kwargs={'pk': self.object.id})


@method_decorator(admin_decorators, name='dispatch')
class EventDetailView(DetailView):
    model = Event
    template_name = 'admins/event_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'admins/event_delete_confirm.html'

    def get_success_url(self):
        return reverse('admins:event-list')


""" LUCKY DRAW """


@method_decorator(admin_decorators, name="dispatch")
class LuckyDrawView(View):
    template_name = 'admins/lucky_draw.html'

    def get(self, request, pk, *args, **kwargs):
        context = {}

        obj = get_object_or_404(Event.objects.filter(status__in=['draft', 'published']), pk=pk)
        names = Participant.objects.filter(event=obj).values_list('token_number', flat=True)
        result, created = Result.objects.get_or_create(event=obj)

        if not names:
            messages.error(request, "No participants added to this event.")
            return redirect("admins:event-detail", pk)

        names = list(names)
        winner = result.participant

        context['names'] = list(names)
        context['seconds'] = 1 * 1000
        context['object'] = obj
        context['result'] = winner.token_number if winner else 0

        return render(request=request, template_name=self.template_name, context=context)


@csrf_exempt
def spin_json_view(request, event_id, token_number):
    message = "Something went wrong"
    error = True

    obj = get_object_or_404(Event.objects.filter(status__in=['draft', 'published']), pk=event_id)
    participant = Participant.objects.filter(token_number=token_number, event=obj)

    # YES: participant available with this token in this event
    if participant:

        # GET result for this event
        participant = participant[0]
        result, created = Result.objects.get_or_create(event=obj)
        if result:

            # IF result is missing
            if not result.participant:

                result.participant = participant
                result.save()

                error = False
                message = "Results updated"

            else:
                error = False
                message = "Already updated"

            obj.status = "completed"
            obj.save()

        else:
            message = "issue in result"
    else:
        message = "wrong token number"

    return JsonResponse({
        'success': error,
        'message': message
    })
