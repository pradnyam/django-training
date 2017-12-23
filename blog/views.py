from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib import messages
# Create your views here.

from .form import RegisterForm

class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            messages.info(request, "User added successfully!")
            return redirect('/')
        else:
            return self.render_to_response(self.get_context_data(form=form))
