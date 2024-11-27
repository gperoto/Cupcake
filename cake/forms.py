from django import forms
from.models import OrdemPedido, Cliente
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

class OrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemPedido
        fields = [
            'ordenado_por', 'cep', 'cidade', 'estado', 'rua', 'numero', 
            'telefone', 'email', 'metodo_pagamento', 'numero_cartao', 
            'nome_cartao', 'validade_cartao', 'cvv_cartao'
        ]


class RegistrarClienteForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), label="Nome de Usuário")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirme a Senha")
    email = forms.CharField(widget=forms.EmailInput())
    nome = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Cliente
        fields=["username", "password1", "password2", "email", "nome"]
    
    def clean_username(self):
        unome = self.cleaned_data.get("username")
        if User.objects.filter(username=unome).exists():
            raise forms.ValidationError("Este usuário já existe")
        return unome

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem")

        return cleaned_data

    
class EntrarClienteForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())