from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
# Create your views here.

from blog.form import RegisterForm, LoginForm, BlogForm
from blog.models import User, session, Blog

def is_login_sql_alchemy(username):
    try:
        logged = session.query(User).filter_by(username=username).exists()
        return True
    except:
        return False

class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            messages.info(request, "User added successfully!")
            return redirect(reverse('register'))
        else:
            return self.render_to_response(self.get_context_data(form=form))



class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        import ipdb; ipdb.set_trace()
        user = session.query(User).filter_by(username=form.cleaned_data['username']).one()
        login(self.request, user)
        return reverse('home')


class BlogListView(ListView):
    # queryset = session.query(Blog).all()
    context_object_name = 'blogs'
    template_name = 'blog_list.html'

    def get_queryset(self):
        return session.query(Blog).all()


class BlogFormView(FormView):
    template_name = 'blog_form.html'
    form_class = BlogForm

    def get_context_data(self, **kwargs):
        context_data = super(BlogFormView, self).get_context_data()
        if 'id' in self.kwargs:
            context_data.update({'edit': True, 'id': self.kwargs.get('id')})
        return context_data

    def get_initial(self):
        initial  = super(BlogFormView, self).get_initial()
        if 'id' in self.kwargs:
            blog = session.query(Blog).filter_by(id=self.kwargs['id']).one()
            initial.update({'title': blog.title, 'content': blog.content, 'author': blog.author_id})
        return initial

    def form_valid(self, form):
        if 'id' in self.kwargs:
            blog = session.query(Blog).filter_by(id=self.kwargs['id']).one()
        else:
            blog = Blog()
        blog.title = form.cleaned_data['title']
        blog.content = form.cleaned_data['content']
        blog.author = session.query(User).filter_by(id=form.cleaned_data['author']).one()
        session.add(blog)
        session.commit()
        return redirect(reverse('blog_list'))