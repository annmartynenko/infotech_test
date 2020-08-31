from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from chat.models import Message
from django.views.generic.edit import FormView
from chat.forms import Registration
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class MesssageDetailView(DetailView):
    model = Message


class MesssageCreateView(CreateView):
    model = Message
    fields = ['text', 'image']

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        print(self.request.user)
        if self.request.user.is_authenticated:
            object.owner = self.request.user
        object.save()
        return super(CreateView, self).form_valid(form)


class MesssageUpdateView(UpdateView):
    model = Message
    fields = ['text', 'image']

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(UpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class MesssageDeleteView(DeleteView):
    model = Message

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(DeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class MesssageListView(ListView):
    model = Message

    def get(self, request, *args, **kwargs):
        stuff = self.get_queryset()
        if request.GET.get('sort') == 'old_to_new':
            stuff = stuff.order_by('created_at')
        elif request.GET.get('sort') == 'new_to_old':
            stuff = stuff.order_by('created_at').reverse()
        elif request.GET.get('sort') == 'last_day':
            stuff = stuff.filter(created_at__range=(timezone.now() - timedelta(hours=24), timezone.now()))
        elif request.GET.get('sort') == 'current_user' and self.request.user.is_authenticated:
            stuff = stuff.filter(owner=self.request.user)
        return render(request, 'chat/message_list.html', {'message_list': stuff})


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = Registration
    success_url = 'messages'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        password = form.clean_password2()
        name = form.cleaned_data.get("name")
        print(name + ' ' + password)
        user = authenticate(self.request, username=name, password=password)
        if user is None:
            us1 = User.objects.create_user(name, None, password)
            us1.save()
        else:
            messages.error(self.request, 'User already exits!')
        return super().form_valid(form)
