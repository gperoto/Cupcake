from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import OrdemForm, RegistrarClienteForm, EntrarClienteForm
from.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LojaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        carrinho_id = request.session.get("carrinho_id")
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            if request.user.is_authenticated and request.user.cliente:
                carrinho_obj.cliente = request.user.cliente
                carrinho_obj.save()
        return super().dispatch(request, *args, **kwargs)

class HomeView(LojaMixin, TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todosprodutos = Produto.objects.all().order_by("-id")
        paginator = Paginator(todosprodutos,6)
        page_number = self.request.GET.get('page')
        produto_list = paginator.get_page(page_number)
        context['produtos']= produto_list
        return context

        
class produtoslistaView(LojaMixin, TemplateView):
    template_name = "lista-de-produtos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias']= Categoria.objects.all()
        return context

class produtosinfoView(LojaMixin, TemplateView):
    template_name = "produto.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug= url_slug)
        context['produto']= produto
        return context

class addcarrinhoView(LojaMixin, TemplateView):
    template_name = "addcarrinho.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs['prod_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carrinho_id = self.request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            porduto_no_carrinho = carrinho_obj.carrinhoproduto_set.filter(produto=produto_obj)
            if porduto_no_carrinho.exists():
                carrinhoproduto = porduto_no_carrinho.last()
                carrinhoproduto.quantidade += 1
                carrinhoproduto.subtotal += produto_obj.preco
                carrinhoproduto.save()
                carrinho_obj.total += produto_obj.preco
                carrinho_obj.save()
            else:
                carrinhoproduto = CarrinhoProduto.objects.create(
                    carrinho = carrinho_obj,
                    produto = produto_obj,
                    quantidade = 1,
                    avaliacao = produto_obj.preco,
                    subtotal = produto_obj.preco,
                )
                carrinho_obj.total += produto_obj.preco
                carrinho_obj.save()            
        else:
            carrinho_obj = Carrinho.objects.create(total=0)
            self.request.session['carrinho_id']=carrinho_obj.id
            carrinhoproduto = CarrinhoProduto.objects.create(
                    carrinho = carrinho_obj,
                    produto = produto_obj,
                    avaliacao = produto_obj.preco,
                    quantidade = 1,
                    subtotal = produto_obj.preco,
                )
            carrinho_obj.total += produto_obj.preco
            carrinho_obj.save()
        return context

class gerenciarcarrinhoView(LojaMixin, View):    
    def get(self,request,*args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_obj = CarrinhoProduto.objects.get(id=cp_id)
        carrinho_obj = cp_obj.carrinho

        if acao =="inc":
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.avaliacao
            cp_obj.save()
            carrinho_obj.total += cp_obj.avaliacao
            carrinho_obj.save()
        elif acao =="dcr":
            cp_obj.quantidade -= 1
            cp_obj.subtotal -= cp_obj.avaliacao
            cp_obj.save()
            carrinho_obj.total -= cp_obj.avaliacao
            carrinho_obj.save()
            if cp_obj.quantidade == 0:
                cp_obj.delete()
        elif acao =="rmv":
            carrinho_obj.total -= cp_obj.subtotal
            carrinho_obj.save()
            cp_obj.delete()

        return redirect("cake:meucarrinho")
    

class limparcarrinhoView(LojaMixin, View):  
    def get(self,request,*args, **kwargs):
        carrinho_id = request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
            carrinho.carrinhoproduto_set.all().delete()
            carrinho.total=0
            carrinho.save()
        return redirect("cake:meucarrinho")
       
class meucarrinhoView(LojaMixin, TemplateView):
    template_name = "meucarrinho.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get("carrinho_id", None)

        if carrinho_id:
            try:
                carrinho = Carrinho.objects.get(id=carrinho_id)
            except Carrinho.DoesNotExist:
                carrinho = None
        else:
            carrinho = None

        context['carrinho'] = carrinho
        return context

@method_decorator(login_required(login_url='cake:entrarcliente'), name='dispatch')
class checkoutView(LojaMixin, CreateView):
    template_name = "checkout.html"
    form_class = OrdemForm
    success_url = reverse_lazy("cake:home")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho_obj = None
        context['carrinho'] = carrinho_obj
        return context

    def form_valid(self, form):
        carrinho_id = self.request.session.get("carrinho_id")
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            form.instance.carrinho = carrinho_obj
            form.instance.subtotal = carrinho_obj.total
            form.instance.total = carrinho_obj.total
            form.instance.pedido_status = "Pedido Recebido"
            
            # Inclua outros campos do formulário aqui, se necessário
            form.instance.metodo_pagamento = self.request.POST.get('metodo_pagamento')
            if form.instance.metodo_pagamento == 'cartao':
                form.instance.numero_cartao = self.request.POST.get('numero_cartao')
                form.instance.nome_cartao = self.request.POST.get('nome_cartao')
                form.instance.validade_cartao = self.request.POST.get('validade_cartao')
                form.instance.cvv_cartao = self.request.POST.get('cvv_cartao')
            del self.request.session['carrinho_id']
        else:
            return redirect("cake:home")
        return super().form_valid(form)


class registrarclienteView(CreateView):
    template_name = "registrar.html"
    form_class = RegistrarClienteForm
    success_url = reverse_lazy("cake:entrarcliente")

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
            email=form.cleaned_data.get("email")
        )
        form.instance.user = user
        form.save()
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return redirect(self.success_url)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
   

class sairclienteView(View):
    def get(self,request):
        logout(request)
        return redirect("cake:home")
    
    
class entrarclienteView(FormView):
    template_name = "entrarcliente.html"
    form_class = EntrarClienteForm
    success_url = reverse_lazy("cake:home")

    def form_valid(self, form):
        unome = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=unome,password=pword)
        if usr is not None and Cliente.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error":"Usuário ou senha incorreto"})
        return super().form_valid(form)
    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class sobreView(LojaMixin, TemplateView):
    template_name = "sobre.html"

class contatoView(LojaMixin, TemplateView):
    template_name = "contato.html"


class perfilclienteView(TemplateView):
    template_name = "clienteperfil.html"

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        pedidos = OrdemPedido.objects.filter(carrinho__cliente=cliente).order_by("-id")
        context ['pedidos'] = pedidos

        return context
    

class perfilpedidodetalheView(DetailView):
    template_name = "perfilpedidodetalhe.html"
    model = OrdemPedido
    context_object_name="pedido_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            try:
                pedido = OrdemPedido.objects.get(id=order_id)
                if request.user.cliente != pedido.carrinho.cliente:
                    return redirect("cake:perfilcliente")
            except OrdemPedido.DoesNotExist:
                return redirect("cake:perfilcliente")
        else:
            return redirect("/entrar/?next=/perfil/") 
        return super().dispatch(request, *args, **kwargs)
    
class AdminReqMixin(object):

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/adminlogin/")
        return super().dispatch(request, *args, **kwargs)
    
class adminloginView(FormView):
    template_name = "adminpaginas/adminlogin.html"
    form_class = EntrarClienteForm
    success_url = reverse_lazy("cake:adminhome")

    def form_valid(self, form):
        unome = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=unome,password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error":"Usuário ou senha incorreto"})
        return super().form_valid(form)

class adminhomeView(AdminReqMixin, TemplateView):
    template_name = "adminpaginas/adminhome.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            context["PedidosPendentes"] = OrdemPedido.objects.filter(pedido_status="Pedido Recebido").order_by("-id")
            return context
    
    

class adminpedidoView(AdminReqMixin, DetailView):
    template_name = "adminpaginas/adminpedido.html"
    model = OrdemPedido

    context_object_name = "pedido_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todosstatus"] = PEDIDO_STATUS

        return context

class admintodospedidosView(AdminReqMixin, ListView):
    template_name = "adminpaginas/admintodospedidos.html"
    queryset = OrdemPedido.objects.all().order_by("-id")

    context_object_name = "todospedidos"


class adminpedidomudarView(AdminReqMixin, ListView):
    def post(self, request, *args, **kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = OrdemPedido.objects.get(id=pedido_id)
        novo_status = request.POST.get("status")
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()


        return redirect(reverse_lazy("cake:adminpedido", kwargs={"pk":self.kwargs["pk"]}))
    
class pesquisarView(TemplateView):
    template_name = "pesquisar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Produto.objects.filter(Q(titulo__icontains=kw) | Q(descricao__icontains=kw))
        context["results"] = results

        return context
