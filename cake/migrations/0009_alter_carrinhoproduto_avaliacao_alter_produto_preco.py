# Generated by Django 5.1.3 on 2024-11-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0008_alter_carrinhoproduto_avaliacao_alter_produto_preco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinhoproduto',
            name='avaliacao',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco',
            field=models.PositiveIntegerField(),
        ),
    ]