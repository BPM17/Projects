from django import forms

class Client(forms.Form):
    name = forms.CharField(label="Nombre", max_length=100, widget=forms.TextInput(attrs={'placeholder':'Name','class': 'input'}))
    telephone = forms.IntegerField(label="Teléfono", max_value=15,widget=forms.TextInput(attrs={'placeholder':'Cellphone','class': 'input'}))
    email = forms.EmailField(label="E-mail", max_length=100,widget=forms.TextInput(attrs={'placeholder':'E-mail','class': 'input'}))
    description = forms.CharField(label="Descripción", max_length=500,widget=forms.TextInput(attrs={'placeholder':'What can we do for you?','class': 'input'}))