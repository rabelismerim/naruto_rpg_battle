import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api'

export const useBattleStore = defineStore('battle', {
  state: () => ({
    ninjas: [],
    playerNinja: null,
    enemyNinja: null,
    battleLogs: [],
    isBattleOver: false,
    winner: null,
    loading: false,
    gainedXp: 0,
    leveledUp: false,
    // Dicionário independente para guardar o progresso de CADA ninja pelo seu ID
    allNinjasProgress: {}
  }),

  actions: {
    async fetchNinjas() {
      try {
        const response = await axios.get(`${API_URL}/ninjas/`)
        this.ninjas = response.data
      } catch (error) {
        console.error("Erro ao buscar ninjas:", error)
      }
    },

    selectPlayer(ninja) {
      // Se este ninja já tem progresso guardado, usamos os dados evoluídos dele
      const saved = this.allNinjasProgress[ninja.id]

      const level = saved ? saved.level : (ninja.level || 1)
      const xp = saved ? saved.xp : (ninja.xp || 0)
      const xpNext = saved ? saved.xp_to_next_level : (ninja.xp_to_next_level || 100)
      const maxHp = saved ? saved.max_hp : ninja.max_hp
      const maxChakra = saved ? saved.max_chakra : ninja.max_chakra

      this.playerNinja = {
        ...ninja,
        max_hp: maxHp,
        max_chakra: maxChakra,
        current_hp: maxHp,
        current_chakra: maxChakra,
        level: level,
        xp: xp,
        xp_to_next_level: xpNext
      }
    },

    selectEnemy(ninja) {
      this.enemyNinja = {
        ...ninja,
        current_hp: ninja.max_hp,
        current_chakra: ninja.max_chakra,
        attack: Math.floor((ninja.attack || 20) * 1.2) // IA desafiante (+20% ataque)
      }
    },

    async executeTurn(actionType, jutsuId = null) {
      if (!this.playerNinja || !this.enemyNinja || this.isBattleOver) return

      try {
        const payload = {
          action: actionType,
          jutsu_id: jutsuId,
          player: this.playerNinja,
          enemy: this.enemyNinja
        }

        const response = await axios.post(`${API_URL}/battle/turn/`, payload)
        const data = response.data

        this.playerNinja = data.player
        this.enemyNinja = data.enemy

        const turnLogs = data.log || data.logs || []
        this.battleLogs.unshift(...turnLogs)

        if (data.winner) {
          this.isBattleOver = true
          this.winner = data.winner

          if (this.winner === 'player') {
            this.gainedXp = 60 // 60 XP por vitória
            this.playerNinja.xp += this.gainedXp
            this.leveledUp = false

            // Loop de Level Up caso atinja o limite
            while (this.playerNinja.xp >= this.playerNinja.xp_to_next_level) {
              this.playerNinja.xp -= this.playerNinja.xp_to_next_level
              this.playerNinja.level += 1
              this.playerNinja.xp_to_next_level = Math.floor(this.playerNinja.xp_to_next_level * 1.4)
              
              this.playerNinja.max_hp += 25
              this.playerNinja.max_chakra += 15
              this.leveledUp = true
            }

            // Restaura a vida completa após vencer
            this.playerNinja.current_hp = this.playerNinja.max_hp
            this.playerNinja.current_chakra = this.playerNinja.max_chakra

            // ATUALIZA E GUARDA O PROGRESSO ESPECÍFICO DESTE NINJA NO DICIONÁRIO GLOBAL
            this.allNinjasProgress[this.playerNinja.id] = {
              level: this.playerNinja.level,
              xp: this.playerNinja.xp,
              xp_to_next_level: this.playerNinja.xp_to_next_level,
              max_hp: this.playerNinja.max_hp,
              max_chakra: this.playerNinja.max_chakra
            }
          }
        }
      } catch (error) {
        console.error('Erro ao processar turno:', error)
      }
    },

    resetBattle() {
      // Limpa a batalha atual, permitindo escolher outro oponente ou outro player mantendo as evoluções
      this.enemyNinja = null
      this.battleLogs = []
      this.isBattleOver = false
      this.winner = null
      this.gainedXp = 0
      this.leveledUp = false
    }
  }
})