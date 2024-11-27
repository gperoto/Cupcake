from django.contrib import admin
from.models import *

admin.site.register([Admin, Cliente,Categoria,OrdemPedido,Produto,Carrinho,CarrinhoProduto])
