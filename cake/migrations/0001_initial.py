# Generated by Django 5.1.3 on 2024-11-14 01:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=2)),
                ('bairro', models.CharField(max_length=200)),
                ('rua', models.CharField(max_length=200)),
                ('numero', models.PositiveIntegerField()),
                ('complemento', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=20)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cake.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='OrdemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordenado_por', models.CharField(max_length=200)),
                ('endereco_envio', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=12)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveIntegerField()),
                ('disconto', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('pedido_status', models.CharField(choices=[('Pedido Recebido', 'Pedido Recebido'), ('Pedido Processando', 'Pedido Processando'), ('Pedido Cancelado', 'Pedido Cancelado'), ('Pedido Caminho', 'Pedido Caminho'), ('Pedido Completado', 'Pedido Completado')], max_length=50)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('carro', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cake.carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='produtos')),
                ('preco', models.PositiveIntegerField()),
                ('avaliacao', models.PositiveIntegerField()),
                ('descricao', models.TextField()),
                ('return_devolucao', models.CharField(blank=True, max_length=300, null=True)),
                ('visualizacao', models.PositiveIntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='CarrinhoProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake.carrinho')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake.produto')),
            ],
        ),
    ]
