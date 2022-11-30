from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(({'placeholder': 'Prénom'}))
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nom de Famille'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Numéro de Téléphone'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['address_line_1'].widget.attrs.update({'placeholder': 'Adresse 1'})
        self.fields['address_line_2'].widget.attrs.update({'placeholder': 'Adresse 2'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Pays'})
        self.fields['state'].widget.attrs.update({'placeholder': 'Région'})
        self.fields['city'].widget.attrs.update({'placeholder': 'Ville'})
        self.fields['order_note'].widget.attrs.update({'placeholder': 'Demande Spécifique'})

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']

        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom de Famille',
            'phone': 'Numéro de téléphone',
            'email': 'Email',
            'address_line_1': 'Adresse 1',
            'address_line_2': 'Adresse 2',
            'country': 'Pays',
            'state': 'Région',
            'city': 'Ville',
            'order_note': 'Demande Spécifique',
        }


