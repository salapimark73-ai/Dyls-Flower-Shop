from django import forms

from .models import Flower


class FlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = [
            'flower_name',
            'flower_type',
            'price',
            'quantity',
            'color',
            'description',
        ]
        widgets = {
            'flower_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Garden Rose',
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'quantity': forms.NumberInput(attrs={
                'min': '0',
                'placeholder': '0',
            }),
            'color': forms.TextInput(attrs={
                'placeholder': 'e.g. Crimson',
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a short note about this flower...',
            }),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity
