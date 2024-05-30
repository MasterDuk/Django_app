from django import forms
from django.core import validators
from django.contrib.auth.models import Group
from .models import Product, Order

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',

# 1 variant
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 30}),
#         validators=[validators.RegexValidator(
#            regex=r"great",
#            message="Field must contain word 'great'",
#         )],
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    images = forms.ImageField(                             # не работает так в 5.0
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    )



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'user', 'product'


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()