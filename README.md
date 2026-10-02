# 🍃 Naruto RPG Battle — Full Stack Application ⚡

> Aplicação web full stack 2D baseada em turnos, desenvolvida com arquitetura desacoplada (Decoupled Architecture), com foco em lógica de progressão de níveis independente, consumo de APIs RESTful e experiência de utilizador imersiva.

---

## 🏛️ Arquitetura do Sistema

O projeto adota uma separação estrita de responsabilidades entre o cliente e o servidor:

* **Frontend (SPA):** Desenvolvido em **Vue 3** com a *Composition API*, utilizando **Pinia** para gestão de estado global e persistência de dados em memória por personagem.
* **Backend (API REST):** Desenvolvido em **Python** com **Django** e **Django REST Framework (DRF)**, responsável pelo processamento de regras de negócio, cálculo de dano por turnos e escalonamento de Inteligência Artificial.

---

## 🚀 Tecnologias Utilizadas

### **Frontend**
* **Vue 3** (`<script setup>`)
* **Pinia** (State Management & Multi-character persistent tracking)
* **Axios** (HTTP Client)
* **CSS3** (Animações *keyframes* customizadas, design responsivo e HUDs dinâmicos)

### **Backend**
* **Python 3.10+**
* **Django & Django REST Framework (DRF)**
* **Django CORS Headers** (Segurança e integração cross-origin)

---

## ✨ Principais Desafios Técnicos Resolvidos

1. **Gestão de Estado Isolada (`allNinjasProgress`):**
   * *Problema:* A evolução de nível e XP costumava resetar ao alternar entre personagens na seleção.
   * *Solução:* Implementação de um dicionário indexado por ID de ninja na store do Pinia, permitindo que múltiplos personagens evoluam de forma totalmente independente e mantenham o seu progresso durante toda a sessão.
2. **IA Competitiva e Balanceada:**
   * Escalocamento dinâmico de atributos no backend para o oponente controlado pelo computador, garantindo um nível de desafio constante (+20% de poder de ataque).
3. **Feedback Audiovisual e Combat Text:**
   * Integração de animações de investida (*dash*), trepidação em caso de dano (*hit-shake*) e textos de dano flutuantes gerados dinamicamente em tempo real.
