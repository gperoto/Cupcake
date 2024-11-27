from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="produtos")
    preco = models.PositiveIntegerField()
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Carrinho:" +str(self.id)

class CarrinhoProduto(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Carrinho:" +str(self.carrinho.id) + "CarrinhoProduto:" +str(self.id)

PEDIDO_STATUS = (
    ("Pedido Recebido","Pedido Recebido"),
    ("Pedido Processando","Pedido Processando"),
    ("Pedido Cancelado","Pedido Cancelado"),
    ("Pedido Caminho","Pedido Caminho"),
    ("Pedido Completado","Pedido Completado"),
)

class OrdemPedido(models.Model):
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    cep = models.PositiveIntegerField()
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    telefone = models.CharField(max_length=12)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)
    criado_em = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=50, null=True, blank=True) 
    numero_cartao = models.CharField(max_length=20, null=True, blank=True) 
    nome_cartao = models.CharField(max_length=100, null=True, blank=True) 
    validade_cartao = models.CharField(max_length=5, null=True, blank=True) 
    cvv_cartao = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return "OrdemPedido" + str(self.id)

class Pagamento(models.Model):
    pedido = models.OneToOneField(OrdemPedido, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pendente')

    def __str__(self):
        return f'Pagamento {self.id} - {self.metodo}'


