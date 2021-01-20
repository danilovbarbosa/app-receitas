from django.contrib import admin

from receitas.models import Receita

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'pessoa', 'categoria', 'rendimento')
    list_display_links = ('id', 'nome_receita')
    search_fields = ('nome_receita', 'pessoa__nome',)
    list_filter = ('categoria',)
    list_per_page = 2
