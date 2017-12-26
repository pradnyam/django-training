import bcrypt
from django import forms
from .models import User, session

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class':'form-control'})

class RegisterForm(BaseForm):
    first_name = forms.CharField(label="First Name", max_length=20, required=True)
    last_name = forms.CharField(label="Last Name", max_length=20, required=True)
    username = forms.CharField(label="User Name", max_length=20, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    re_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_username(self):
        user_names = [user.username for user in session.query(User).all()]
        if self.cleaned_data['username'] in user_names:
            raise forms.ValidationError('User Name already taken!')
        return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['re_password']:
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data

    def save(self):
        hash_password = bcrypt.hashpw(self.data['password'].encode('utf-8'), bcrypt.gensalt(12))
        user = User(name="{} {}".format(self.data['first_name'], self.data['last_name']),
                    username=self.data['username'],
                    password=hash_password)
        session.add(user)
        session.commit()


class LoginForm(BaseForm):
    username = forms.CharField(label="User Name", max_length=20, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            user = session.query(User).filter_by(username=self.cleaned_data['username']).one()
            if user.check_password(self.cleaned_data['password']):
                return self.cleaned_data
            else:
                raise forms.ValidationError('Invalid User name or password provided')
        else:
            raise forms.ValidationError('Please provide credentials to log in')



class BlogForm(BaseForm):
    title = forms.CharField(label="Title", max_length=20, required=True)
    author = forms.ChoiceField(label="Author", choices=[(user.id, user.name) for user in session.query(User).all()])
    content = forms.CharField(label="Content", widget=forms.Textarea)

