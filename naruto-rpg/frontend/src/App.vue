<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useBattleStore } from './stores/useBattleStore'

const battleStore = useBattleStore()
const attackingSide = ref(null)
const hitSide = ref(null)

// Lista reativa para controlar os textos de dano flutuante na tela
const floatingTexts = ref([])

// Gestão de Áudio
const bgMusic = new Audio('/audio/Naruto - The Rising Fighting Spirit.mp3')
bgMusic.loop = true
bgMusic.volume = 0.4

const victorySound = new Audio('/audio/street-fighter-ii-you-win-perfect.mp3')
victorySound.volume = 0.6

const defeatSound = new Audio('/audio/you-loose.mp3')
defeatSound.volume = 0.6

onMounted(async () => {
  await battleStore.fetchNinjas()
})

const playBattleMusic = () => {
  bgMusic.currentTime = 0
  bgMusic.play().catch(() => {})
}

const stopMusic = () => {
  bgMusic.pause()
  bgMusic.currentTime = 0
}

// Função para disparar o texto flutuante de dano no alvo correto
const triggerFloatingText = (targetSide, amount, isCrit = false) => {
  const id = Date.now() + Math.random()
  floatingTexts.value.push({
    id,
    side: targetSide, // 'player' ou 'enemy'
    text: isCrit ? `CRITICAL! -${amount}` : `-${amount}`,
    isCrit
  })

  // Remove o elemento do array após a animação terminar (800ms)
  setTimeout(() => {
    floatingTexts.value = floatingTexts.value.filter(item => item.id !== id)
  }, 800)
}

const handleAction = async (actionType, jutsuId = null) => {
  if (battleStore.isBattleOver) return

  // Guarda o HP do inimigo antes do turno para calcular o dano causado
  const enemyHpBefore = battleStore.enemyNinja.current_hp

  attackingSide.value = 'player'
  
  setTimeout(() => {
    hitSide.value = 'enemy'
  }, 200)

  await battleStore.executeTurn(actionType, jutsuId)

  // Calcula quanto dano o inimigo sofreu neste turno
  const damageDealt = enemyHpBefore - battleStore.enemyNinja.current_hp
  if (damageDealt > 0) {
    triggerFloatingText('enemy', damageDealt)
  }

  if (battleStore.isBattleOver) {
    stopMusic()
    if (battleStore.winner === 'player') {
      victorySound.play().catch(() => {})
    } else {
      defeatSound.play().catch(() => {})
    }
  }

  setTimeout(() => {
    attackingSide.value = null
    hitSide.value = null
  }, 450)
}

const selectEnemyWithMusic = (ninja) => {
  battleStore.selectEnemy(ninja)
  playBattleMusic()
}

const resetGame = () => {
  stopMusic()
  victorySound.pause()
  victorySound.currentTime = 0
  defeatSound.pause()
  defeatSound.currentTime = 0
  battleStore.resetBattle()
}

onUnmounted(() => {
  stopMusic()
})
</script>

<template>
  <div class="game-container">
    <header class="header">
      <h1>🍃 NARUTO RPG BATTLE 💥</h1>
    </header>

    <!-- 1. TELA DE SELEÇÃO -->
    <div v-if="!battleStore.playerNinja || !battleStore.enemyNinja" class="selection-screen">
      <div class="selection-box">
        <h3>1. Escolha o seu Ninja (Player Principal)</h3>
        <div class="ninja-grid" v-if="battleStore.ninjas.length > 0">
          <div 
            v-for="ninja in battleStore.ninjas" 
            :key="'p-' + ninja.id"
            class="ninja-card"
            :class="{ active: battleStore.playerNinja?.id === ninja.id }"
            @click="battleStore.selectPlayer(ninja)"
          >
            <img :src="`/avatars/${ninja.name.toLowerCase().split(' ')[0]}.png`" class="card-avatar" />
            <h4>{{ ninja.name }}</h4>
            <!-- Exibe o nível correto guardado no dicionário de progresso independente do ninja -->
            <span>Lv. {{ battleStore.allNinjasProgress[ninja.id]?.level || ninja.level || 1 }}</span>
          </div>
        </div>
        <p v-else style="text-align: center; color: #a1a1aa; margin-top: 10px;">A carregar ninjas do servidor...</p>
      </div>

      <div class="selection-box" v-if="battleStore.playerNinja">
        <h3>2. Escolha o Oponente (IA)</h3>
        <div class="ninja-grid" v-if="battleStore.ninjas.length > 0">
          <div 
            v-for="ninja in battleStore.ninjas" 
            :key="'e-' + ninja.id"
            class="ninja-card enemy-card"
            :class="{ active: battleStore.enemyNinja?.id === ninja.id }"
            @click="selectEnemyWithMusic(ninja)"
          >
            <img :src="`/avatars/${ninja.name.toLowerCase().split(' ')[0]}.png`" class="card-avatar" />
            <h4>{{ ninja.name }}</h4>
            <span>Lv. {{ battleStore.allNinjasProgress[ninja.id]?.level || ninja.level || 1 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. PALCO DE BATALHA COM AVATARES 2D + DANOS FLUTUANTES -->
    <div v-else class="battle-wrapper">
      
      <!-- BANNER DE FIM DE JOGO COM XP E LEVEL UP -->
      <div v-if="battleStore.isBattleOver" class="game-over-banner" :class="battleStore.winner">
        <h2>
          {{ battleStore.winner === 'player' 
            ? `🏆 VITÓRIA! ${battleStore.playerNinja.name} VENCEU! 🏆` 
            : `💀 DERROTA... ${battleStore.enemyNinja.name} VENCEU! 💀` 
          }}
        </h2>
        <div v-if="battleStore.winner === 'player'" class="xp-reward-box">
          <p class="xp-text">✨ Experiência ganha: +{{ battleStore.gainedXp }} XP</p>
          <p class="level-info">Nível Atual: <strong>{{ battleStore.playerNinja.level }}</strong> (XP: {{ battleStore.playerNinja.xp }} / {{ battleStore.playerNinja.xp_to_next_level }})</p>
          <p v-if="battleStore.leveledUp" class="level-up-alert">🎉 LEVEL UP! O teu ninja ficou mais forte! 🎉</p>
        </div>
      </div>

      <div class="battle-stage">
        <!-- PLAYER 2D -->
        <div class="character-slot">
          <div class="hud-over-head">
            <span class="ninja-name">{{ battleStore.playerNinja.name }} (Lv. {{ battleStore.playerNinja.level }})</span>
            
            <!-- BARRA DE HP -->
            <div class="hp-bar">
              <div 
                class="fill" 
                :style="{ width: Math.max(0, (battleStore.playerNinja.current_hp / battleStore.playerNinja.max_hp * 100)) + '%' }"
              ></div>
            </div>
            <small>HP: {{ battleStore.playerNinja.current_hp }}/{{ battleStore.playerNinja.max_hp }}</small>

            <!-- BARRA DE XP -->
            <div class="xp-bar-container">
              <div 
                class="xp-fill" 
                :style="{ width: Math.min(100, (battleStore.playerNinja.xp / battleStore.playerNinja.xp_to_next_level * 100)) + '%' }"
              ></div>
            </div>
            <small class="xp-small">XP: {{ battleStore.playerNinja.xp }}/{{ battleStore.playerNinja.xp_to_next_level }}</small>
          </div>

          <div 
            class="avatar-container"
            :class="{
              'dash-right': attackingSide === 'player',
              'hit-shake': hitSide === 'player'
            }"
          >
            <img 
              :src="`/avatars/${battleStore.playerNinja.name.toLowerCase().split(' ')[0]}.png`" 
              class="battle-avatar player-avatar" 
              :class="{ 'grayscale-avatar': battleStore.playerNinja.current_hp <= 0 }"
              alt="Player Avatar"
            />
            
            <div 
              v-for="item in floatingTexts.filter(f => f.side === 'player')" 
              :key="item.id" 
              class="floating-damage"
            >
              {{ item.text }}
            </div>
          </div>
        </div>

        <!-- VS -->
        <div class="vs-indicator">VS</div>

        <!-- INIMIGO (IA) 2D -->
        <div class="character-slot">
          <div class="hud-over-head">
            <span class="ninja-name">{{ battleStore.enemyNinja.name }} (Lv. {{ battleStore.allNinjasProgress[battleStore.enemyNinja.id]?.level || battleStore.enemyNinja.level || 1 }})</span>
            <div class="hp-bar">
              <div 
                class="fill enemy-fill" 
                :style="{ width: Math.max(0, (battleStore.enemyNinja.current_hp / battleStore.enemyNinja.max_hp * 100)) + '%' }"
              ></div>
            </div>
            <small>HP: {{ battleStore.enemyNinja.current_hp }}/{{ battleStore.enemyNinja.max_hp }}</small>
          </div>

          <div 
            class="avatar-container"
            :class="{
              'dash-left': attackingSide === 'enemy',
              'hit-shake': hitSide === 'enemy'
            }"
          >
            <img 
              :src="`/avatars/${battleStore.enemyNinja.name.toLowerCase().split(' ')[0]}.png`" 
              class="battle-avatar enemy-avatar" 
              :class="{ 'grayscale-avatar': battleStore.enemyNinja.current_hp <= 0 }"
              alt="Enemy Avatar"
            />

            <div 
              v-for="item in floatingTexts.filter(f => f.side === 'enemy')" 
              :key="item.id" 
              class="floating-damage"
            >
              {{ item.text }}
            </div>
          </div>
        </div>
      </div>

      <!-- PAINEL DE CONTROLES / PODERES -->
      <div class="action-panel">
        <h3>Painel de Ações</h3>
        
        <div class="action-buttons">
          <button class="btn btn-attack" :disabled="battleStore.isBattleOver" @click="handleAction('ATTACK')">
            👊 Taijutsu (Ataque Normal)
          </button>

          <button 
            v-for="jutsu in battleStore.playerNinja.jutsus" 
            :key="jutsu.id"
            class="btn btn-jutsu"
            :disabled="battleStore.isBattleOver"
            @click="handleAction('JUTSU', jutsu.id)"
          >
            🔥 {{ jutsu.name }} (Dano: {{ jutsu.base_damage }})
          </button>

          <button class="btn btn-reset" @click="resetGame">
            🔄 Escolher Outro Oponente
          </button>
        </div>

        <div class="battle-log" v-if="battleStore.battleLogs?.length">
          <p v-for="(log, idx) in battleStore.battleLogs" :key="idx">{{ log }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Trebuchet MS', sans-serif;
}

body {
  background: #111116;
  color: #fff;
  padding: 20px;
}

.game-container {
  max-width: 900px;
  margin: 0 auto;
}

.header h1 {
  text-align: center;
  color: #ff9900;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(255, 153, 0, 0.4);
}

.selection-box {
  background: #1e1e24;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #333;
}

.ninja-grid {
  display: flex;
  gap: 15px;
  margin-top: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.ninja-card {
  background: #2a2a32;
  border: 2px solid #3a3a46;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  width: 130px;
}

.card-avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ff9900;
  margin-bottom: 8px;
}

.ninja-card:hover, .ninja-card.active {
  border-color: #ff9900;
  transform: translateY(-3px);
  background: #32323c;
  box-shadow: 0 4px 12px rgba(255, 153, 0, 0.2);
}

.game-over-banner {
  background: rgba(0, 0, 0, 0.95);
  border: 3px solid #ff9900;
  text-align: center;
  padding: 15px;
  border-radius: 12px 12px 0 0;
  animation: fadeIn 0.5s ease-in-out;
}

.game-over-banner h2 {
  color: #fbbf24;
  font-size: 1.4rem;
  text-shadow: 0 0 12px rgba(251, 191, 36, 0.7);
}

.xp-reward-box {
  margin-top: 10px;
  background: rgba(255, 153, 0, 0.15);
  border: 1px dashed #ff9900;
  padding: 8px;
  border-radius: 6px;
}

.xp-text {
  color: #fbbf24;
  font-weight: bold;
}

.level-info {
  font-size: 0.9rem;
  color: #d1d5db;
  margin-top: 3px;
}

.level-up-alert {
  color: #22c55e;
  font-weight: bold;
  margin-top: 5px;
  font-size: 1rem;
  animation: pulse 1s infinite alternate;
}

.battle-stage {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 380px;
  background: linear-gradient(to bottom, #1a1a24 0%, #2a2a38 70%, #3a3a4a 100%);
  border: 3px solid #ff9900;
  border-top: none;
  padding: 20px;
  position: relative;
}

.vs-indicator {
  font-size: 1.8rem;
  font-weight: 900;
  color: #ff9900;
  text-shadow: 0 0 10px rgba(255, 153, 0, 0.8);
  letter-spacing: 2px;
}

.character-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hud-over-head {
  background: rgba(0, 0, 0, 0.85);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ff9900;
  text-align: center;
  margin-bottom: 12px;
  width: 190px;
}

.ninja-name {
  font-weight: bold;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 4px;
}

.hp-bar {
  background: #333;
  height: 8px;
  border-radius: 4px;
  margin: 4px 0;
  overflow: hidden;
}

.hp-bar .fill {
  background: #22c55e;
  height: 100%;
  transition: width 0.3s ease;
}

.hp-bar .enemy-fill {
  background: #ef4444;
}

.xp-bar-container {
  background: #222;
  height: 6px;
  border-radius: 3px;
  margin: 6px 0 2px 0;
  overflow: hidden;
  border: 1px solid #444;
}

.xp-fill {
  background: #3b82f6;
  height: 100%;
  transition: width 0.4s ease;
}

.xp-small {
  font-size: 0.75rem;
  color: #60a5fa;
}

.avatar-container {
  position: relative;
  transition: transform 0.3s ease;
}

.battle-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ff9900;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
  background: #222;
  transition: filter 0.4s ease;
}

.enemy-avatar {
  transform: scaleX(-1);
  border-color: #ef4444;
}

.grayscale-avatar {
  filter: grayscale(100%) brightness(0.6);
  border-color: #555 !important;
}

.floating-damage {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ef4444;
  font-size: 1.6rem;
  font-weight: 900;
  text-shadow: 0 0 6px #000, 0 0 10px rgba(239, 68, 68, 0.8);
  pointer-events: none;
  animation: floatUpAndFade 0.8s ease-out forwards;
  z-index: 10;
}

@keyframes floatUpAndFade {
  0% {
    opacity: 1;
    transform: translate(-50%, -20px) scale(0.8);
  }
  50% {
    transform: translate(-50%, -60px) scale(1.2);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -90px) scale(1);
  }
}

.dash-right { animation: attackDashRight 0.4s ease-in-out; }
.dash-left { animation: attackDashLeft 0.4s ease-in-out; }
.hit-shake { animation: takeDamage 0.3s ease-in-out; }

@keyframes attackDashRight {
  0% { transform: translateX(0); }
  50% { transform: translateX(80px) scale(1.1); }
  100% { transform: translateX(0); }
}

@keyframes attackDashLeft {
  0% { transform: translateX(0); }
  50% { transform: translateX(-80px) scale(1.1); }
  100% { transform: translateX(0); }
}

@keyframes takeDamage {
  0% { transform: translateX(-10px); filter: brightness(2) drop-shadow(0 0 10px red); }
  50% { transform: translateX(10px); }
  100% { transform: translateX(0); filter: none; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  from { transform: scale(1); }
  to { transform: scale(1.05); }
}

.action-panel {
  background: #1e1e24;
  border: 3px solid #ff9900;
  border-top: none;
  border-radius: 0 0 12px 12px;
  padding: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 15px;
}

.btn {
  padding: 12px 18px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-attack {
  background: #eab308;
  color: #000;
}

.btn-attack:hover:not(:disabled) {
  background: #ca8a04;
}

.btn-jutsu {
  background: #3b82f6;
  color: #fff;
}

.btn-jutsu:hover:not(:disabled) {
  background: #2563eb;
}

.btn-reset {
  background: #4b5563;
  color: #fff;
  margin-left: auto;
}

.battle-log {
  margin-top: 15px;
  background: #111116;
  padding: 10px;
  border-radius: 6px;
  max-height: 100px;
  overflow-y: auto;
  font-size: 0.85rem;
  color: #a1a1aa;
}
</style>