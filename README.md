# Naruto RPG Battle — Backend API

API REST responsável pelos dados dos ninjas e jutsus e pelo processamento dos turnos de batalha. O servidor foi desenvolvido com Python, Django e Django REST Framework.

## Telas do aplicativo

### Seleção do personagem principal

![Tela de seleção do personagem principal](screenshots/selecao-personagens.png)

### Seleção do oponente

Depois de escolher o personagem principal, o jogador escolhe quem enfrentará na batalha.

![Tela para escolher o segundo personagem, oponente controlado pela IA](screenshots/selecao-oponente.png)

### Batalha e dano recebido

| Batalha em andamento | HP diminuindo após um ataque |
| --- | --- |
| ![Pain contra Naruto no início da batalha](screenshots/batalha.png) | ![Efeito de dano e barras de HP atualizadas](screenshots/dano-recebido.png) |

### Resultado da batalha

| Vitória e recompensa de XP | Derrota |
| --- | --- |
| ![Tela de vitória com XP e level up](screenshots/vitoria.png) | ![Tela de derrota após o personagem perder todo o HP](screenshots/derrota.png) |

## Tecnologias

- Python 3.10 ou superior
- Django
- Django REST Framework
- Django CORS Headers
- SQLite para desenvolvimento local

## Funcionalidades da API

- Lista ninjas, atributos, progresso e jutsus disponíveis.
- Atualiza os dados de progresso de um ninja.
- Processa ataques, consumo de chakra, contra-ataques da IA e resultado da batalha.

## Progressão de nível e XP

- Cada vitória concede **60 XP** ao ninja usado pelo jogador.
- Ao atingir o XP necessário, o ninja sobe de nível. O limite inicial é **100 XP** e aumenta em 40% a cada nível, arredondado para baixo.
- O XP que ultrapassa o limite fica acumulado para o próximo nível. O sistema verifica níveis consecutivos, caso o XP acumulado seja suficiente.
- Cada nível aumenta o HP máximo em **25 pontos** e o chakra máximo em **15 pontos**.
- Depois da vitória, o HP e o chakra são restaurados ao máximo. O progresso de cada ninja é acompanhado separadamente durante a sessão.

## Endpoints

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/api/ninjas/` | Lista os ninjas e seus jutsus. |
| `GET` | `/api/ninjas/{id}/` | Consulta um ninja. |
| `PATCH` | `/api/ninjas/{id}/` | Atualiza atributos ou progresso do ninja. |
| `GET` | `/api/jutsus/` | Lista os jutsus. |
| `POST` | `/api/battle/turn/` | Processa uma ação e retorna o estado do turno. |

## Executar localmente

No terminal, acesse esta pasta (`naruto-rpg/backend`) e execute:

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux: use `source .venv/bin/activate` no lugar do comando acima

# Instalar as dependências
pip install -r battle/requirements.txt

# Preparar o banco de dados
python manage.py migrate

# (Opcional) Popular o banco com os ninjas e jutsus iniciais
python manage.py seed_data

# Iniciar a API em http://127.0.0.1:8000/
python manage.py runserver
```

O comando `seed_data` recria os registros iniciais de ninjas e jutsus. Execute-o quando quiser repor esses dados.

## Estrutura

```text
backend/
├── battle/       # Modelos, endpoints, serializers e migrações
├── core/         # Configurações e rotas principais do Django
├── screenshots/  # Capturas do aplicativo para esta documentação
└── manage.py
```

## Projeto

- [Frontend Vue](../frontend/README.md)
- [README principal](../../README.md)
