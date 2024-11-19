from django import forms
from .models import Category, Product, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User 




#Formulario de categorias
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

#Formulario de productos
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

#Formulario de comentarios
class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

#Formulario de review
class ReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], label='Calificación')
    comment = forms.CharField(widget=forms.Textarea, label='Comentario')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        try:
            validate_password(password, self.instance)
        except forms.ValidationError as e:
            self.add_error('password1', e)
        return password