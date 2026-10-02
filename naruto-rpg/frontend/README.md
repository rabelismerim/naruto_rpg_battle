# 🍃 Naruto RPG Battle — Frontend 🎮

Interface gráfica do jogo de RPG turn-based 2D inspirado no universo de Naruto, desenvolvida com **Vue 3**, **Pinia** e **Axios**.

---

## 🚀 Tecnologias Utilizadas
* **Vue 3** (Composition API com `<script setup>`)
* **Pinia** (Gestão de estado global, persistência e tracking individual de nível/XP por personagem)
* **Axios** (Comunicação com a API REST do Django)
* **CSS3 Moderno** (Animações *keyframes* fluidas, layout responsivo e HUDs personalizados)

---

## ✨ Funcionalidades do Frontend
* **Tela de Seleção Dinâmica:** Exibição dos cards de ninjas com atualização em tempo real do nível de cada personagem de forma independente (`allNinjasProgress`).
* **Palco de Batalha 2D Imersivo:** 
  * Avatares dinâmicos com animações de investida (*dash*) e trepidação ao sofrer dano (*hit-shake*).
  * Efeitos flutuantes de dano (*floating combat text*) exibidos em tempo real.
  * Barras de progresso dinâmicas de HP e de XP por nível.
* **Sistema de Áudio Integrado:** Banda sonora de fundo temática e efeitos sonoros dedicados para vitória, derrota e ações.
* **Painel de Ações Táticas:** Execução de Taijutsu básico ou Jutsus especiais baseados no consumo de Chakra.

---

## 🛠️ Como Executar o Frontend

1. Certifique-se de que tem o **Node.js** instalado na sua máquina.
2. Na pasta do frontend, instale as dependências:
   ```bash
   npm install

3. npm run server