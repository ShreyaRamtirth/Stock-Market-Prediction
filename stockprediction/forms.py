from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True,max_length=200)
	phone = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "phone")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.phone = self.cleaned_data['phone']
		if commit:
			user.save()
		return user