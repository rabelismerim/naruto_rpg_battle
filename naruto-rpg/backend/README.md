```markdown
# 🍃 Naruto RPG Battle — Backend API ⚙️

Servidor REST API construído em **Django** e **Django REST Framework (DRF)** responsável por gerir a lógica de turnos de batalha, dados dos ninjas, jutsus e escalonamento de inteligência artificial (IA).

---

## 🚀 Tecnologias Utilizadas
* **Python** (versão 3.10 ou superior)
* **Django** (Framework Web)
* **Django REST Framework (DRF)** (Criação de endpoints RESTful)
* **Django CORS Headers** (Permissão de requisições seguras entre o frontend e o backend)

---

## 📡 Endpoints da API

* `GET /api/ninjas/` — Lista todos os ninjas disponíveis com os respetivos atributos e jutsus.
* `GET /api/jutsus/` — Lista todos os jutsus disponíveis no sistema.
* `POST /api/battle/turn/` — Processa a lógica de um turno de combate (cálculo de dano do jogador, verificação de chakra, contra-ataque da IA e verificação de condições de vitória).

---

## 🛠️ Como Executar o Backend

# 🍃 Naruto RPG Battle — Backend API ⚙️

Servidor REST API construído em **Django** e **Django REST Framework (DRF)** responsável por gerir a lógica de turnos de batalha, dados dos ninjas, jutsus e escalonamento de inteligência artificial (IA).

---

## 🚀 Tecnologias Utilizadas
* **Python** (versão 3.10 ou superior)
* **Django** (Framework Web)
* **Django REST Framework (DRF)** (Criação de endpoints RESTful)
* **Django CORS Headers** (Permissão de requisições seguras entre o frontend e o backend)

---

## 📡 Endpoints da API

* `GET /api/ninjas/` — Lista todos os ninjas disponíveis com os respetivos atributos e jutsus.
* `PATCH /api/ninjas/{id}/` — Atualiza o progresso de nível, XP e atributos do ninja.
* `GET /api/jutsus/` — Lista todos os jutsus disponíveis no sistema.
* `POST /api/battle/turn/` — Processa a lógica de um turno de combate (cálculo de dano do jogador, verificação de chakra, contra-ataque da IA e verificação de condições de vitória).

---

## 🛠️ Como Executar o Backend

1. Certifique-se de que tem o **Python** instalado.
2. Navegue até à pasta do backend e crie o ambiente virtual, ative-o, instale as dependências e inicie o servidor executando os comandos abaixo:

```bash
python -m venv venv

# Para ativar no Windows:
venv\Scripts\activate

# Para ativar no macOS/Linux:
source venv/bin/activate

# Instalar as dependências:
pip install -r requirements.txt

# Executar migrações da base de dados:
python manage.py makemigrations
python manage.py migrate

# Iniciar o servidor:
python manage.py runserver