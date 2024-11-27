from django.urls import path
from.views import *

app_name = "cake"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", sobreView.as_view(), name="sobre"),
    path("contato/", contatoView.as_view(), name="contato"),
    path("lista-de-produtos/", produtoslistaView.as_view(), name="lista-de-produtos"),
    path("produto/<slug:slug>/", produtosinfoView.as_view(), name="produtoinfo"),
    path("addcarrinho-<int:prod_id>/", addcarrinhoView.as_view(), name="addcarrinho"),
    path("meucarrinho/", meucarrinhoView.as_view(), name="meucarrinho"),
    path("gerenciarcarrinho/<int:cp_id>/", gerenciarcarrinhoView.as_view(), name="gerenciarcarrinho"),
    path("limparcarrinho/", limparcarrinhoView.as_view(), name="limparcarrinho"),
    path("checkout/", checkoutView.as_view(), name="checkout"),
    path("registrar/", registrarclienteView.as_view(), name="registrarcliente"),
    path("sair/", sairclienteView.as_view(), name="saircliente"),
    path("entrar/", entrarclienteView.as_view(), name="entrarcliente"),
    path("perfil/", perfilclienteView.as_view(), name="perfilcliente"),
    path("perfil/pedido-<int:pk>/", perfilpedidodetalheView.as_view(), name="perfilpedidodetalhe"),
    path("pesquisar/", pesquisarView.as_view(), name="pesquisar"),

    path("adminlogin/", adminloginView.as_view(), name="adminlogin"),
    path("adminhome/", adminhomeView.as_view(), name="adminhome"),
    path("adminpedido/<int:pk>/", adminpedidoView.as_view(), name="adminpedido"),
    path("admintodospedidos/", admintodospedidosView.as_view(), name="admintodospedidos"),
    path("adminpedidomudar-<int:pk>/", adminpedidomudarView.as_view(), name="adminpedidomudar"),
]
