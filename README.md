# 🏥 Sistema de Gestão para Clínica Escola de Fisioterapia

## 📋 Sobre o Projeto
Este software foi desenvolvido como parte da disciplina de **Atividade Extensionista do curso de Engenharia de Software (UNINTER)**. O projeto visa automatizar processos administrativos e clínicos, unindo a gestão acadêmica à segurança de dados em um ambiente de saúde.

## 🛠️ Tecnologias Utilizadas
* **Backend:** Python 3.x + Django Framework
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Banco de Dados:** SQLite
* **Ícones:** Bootstrap Icons

## 🔐 Funcionalidades e Diferenciais Técnicos

### 1. Controle de Acesso Inteligente (RBAC)
O sistema diferencia as jornadas de usuário para garantir a privacidade dos dados:

* **Perfil Gestor:** Painel analítico com métricas de pacientes, agendamentos e controle total de estagiários.
* **Perfil Estagiário:** Interface otimizada para produtividade e registros de evolução.

### 2. Módulo de Segurança e Auditoria
* Registro automático de tentativas de acesso a URLs restritas.
* Dashboard de alertas de segurança.
* Exportação CSV de relatórios.

### 3. Gestão Clínica
* Gerenciamento de prontuários de pacientes.
* Registro de evoluções fisioterapêuticas.
* Controle de agendamentos.

---

## ⚙️ Como executar o projeto

1. Clone o repositório

```bash
git clone https://github.com/LucianaDev-37/clinica-fisioterapia.git
```

2. Entre na pasta do projeto

```bash
cd clinica-fisioterapia
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

4. Execute as migrações

```bash
python manage.py migrate
```

5. Inicie o servidor

```bash
python manage.py runserver
```

---

## 📸 Demonstração do Sistema

## 📸 Demonstração do Sistema

### Tela de Login
![Login](https://raw.githubusercontent.com/LucianaDev-37/clinica-fisioterapia/main/clinica_fisioterapia/images/login.png)

### Dashboards do Sistema

| Gestor | Estagiário |
|-------|------------|
| ![Gestor](https://raw.githubusercontent.com/LucianaDev-37/clinica-fisioterapia/main/clinica_fisioterapia/images/gestor.png) | ![Estagiario](https://raw.githubusercontent.com/LucianaDev-37/clinica-fisioterapia/main/clinica_fisioterapia/images/estagiario.png) |

### Gestão de Pacientes
![Pacientes](https://raw.githubusercontent.com/LucianaDev-37/clinica-fisioterapia/main/clinica_fisioterapia/images/pacientes.png)
---

## 🚀 Próximos Passos (Roadmap)

* Integração de assistente de consulta com IA.
* Implementação de modais de confirmação para exclusões.

---

**Desenvolvido por:** Luciana da Silva Reis  
Engenharia de Software - UNINTER