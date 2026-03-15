from django.contrib import admin
from .models import Estagiario, AuditoriaAcesso, LogAlteracao

# Configuração para ver os logs de acesso (tentativas de intrusão)
@admin.register(AuditoriaAcesso)
class AuditoriaAcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pagina_tentada', 'data_hora', 'sucesso')
    list_filter = ('sucesso', 'data_hora') # Filtro lateral para ver só os "NEGADOS"
    search_fields = ('usuario__username', 'pagina_tentada')
    readonly_fields = ('usuario', 'pagina_tentada', 'data_hora', 'sucesso') # Logs não se editam!

# Configuração para ver quem mudou dados (histórico de alterações)
@admin.register(LogAlteracao)
class LogAlteracaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tabela', 'acao', 'data_hora')
    list_filter = ('acao', 'tabela', 'data_hora')
    search_fields = ('usuario__username', 'tabela', 'valor_novo')
    readonly_fields = ('usuario', 'tabela', 'registro_id', 'acao', 'data_hora', 'valor_antigo', 'valor_novo')

# Registro simples do Estagiário
admin.site.register(Estagiario)