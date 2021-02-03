from django.contrib import admin

from pessoas.models import Pessoa


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('nome', 'email')
    search_fields = ('nome',)
    list_per_page = 2
