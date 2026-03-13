
#teste automatizado
from django.test import TestCase
from .models import Estagiario

class EstagiarioModelTest(TestCase):

    def setUp(self):
        # cria um estagiário temporário apenas para o teste
        self.estagiario = Estagiario.objects.create(
            nome="Luciana Teste",
            email="luciana@teste.com",
            matricula="12345",
            curso="Software Engineering"
        )

    def test_estagiario_criado_com_sucesso(self):
        """Verifica se o nome salvo no banco é o mesmo que definimos"""
        estagiario = Estagiario.objects.get(id=self.estagiario.id)
        self.assertEqual(estagiario.nome, "Luciana Teste")