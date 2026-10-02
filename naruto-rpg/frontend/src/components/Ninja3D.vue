<script setup>
import { computed } from 'vue'
import { TresCanvas } from '@tresjs/core'
import { GLTFModel, OrbitControls } from '@tresjs/cientos'

const props = defineProps({
  modelPath: String,
  isEnemy: Boolean,
  isAttacking: Boolean,
  isHit: Boolean
})

const NINJA_SETTINGS = {
  naruto:  { scale: [1.7, 1.7, 1.7],       position: [0, -1.35, 0],     rotationY: -Math.PI / 2 },
  sasuke:  { scale: [0.024, 0.024, 0.024], position: [0, -1.35, 0],     rotationY: -Math.PI / 2 },
  kakashi: { scale: [0.38, 0.38, 0.38],   position: [0, -1.35, 0],     rotationY: -Math.PI / 2 },
  sakura:  { scale: [1.8, 1.8, 1.8],       position: [0, -1.35, 0],     rotationY: -Math.PI / 2 }, 
  pain:    { scale: [1.8, 1.8, 1.8],       position: [0, -1.35, 0],     rotationY: Math.PI / 2 }
}

const currentNinja = computed(() => {
  if (!props.modelPath) return 'naruto'
  const pathParts = props.modelPath.toLowerCase().split('/')
  for (const part of pathParts) {
    if (NINJA_SETTINGS[part]) return part
  }
  return 'naruto'
})

const config = computed(() => {
  return NINJA_SETTINGS[currentNinja.value] || { scale: [1, 1, 1], position: [0, -0.9, 0], rotationY: 0 }
})

const finalRotationY = computed(() => {
  const baseRotation = props.isEnemy ? -Math.PI / 2 : Math.PI / 2
  return baseRotation + config.value.rotationY
})

const onModelReady = (model) => {
  model.traverse((child) => {
    if (child.isMesh) {
      child.frustumCulled = false
    }
  })
}
</script>

<template>
  <div 
    class="ninja-3d-wrapper" 
    :class="{
      'dash-right': isAttacking && !isEnemy,
      'dash-left': isAttacking && isEnemy,
      'hit-shake': isHit
    }"
  >
    <TresCanvas clear-color="transparent" alpha>
      <TresPerspectiveCamera :position="[0, 0, 3.8]" :look-at="[0, 0, 0]" />

      <OrbitControls />

      <TresAmbientLight :intensity="2.5" />
      <TresDirectionalLight :position="[3, 5, 3]" :intensity="3" />
      <TresDirectionalLight :position="[-3, 3, -3]" :intensity="1.5" />

      <TresGroup 
        :scale="config.scale" 
        :position="config.position" 
        :rotation="[0, finalRotationY, 0]"
      >
        <Suspense>
          <GLTFModel 
            v-if="modelPath"
            :key="modelPath" 
            :path="modelPath" 
            @load="onModelReady"
          />
        </Suspense>
      </TresGroup>
    </TresCanvas>
  </div>
</template>

<style scoped>
.ninja-3d-wrapper {
  width: 260px;
  height: 320px;
  transition: transform 0.3s ease;
}

.dash-right { animation: attackDashRight 0.4s ease-in-out; }
.dash-left { animation: attackDashLeft 0.4s ease-in-out; }
.hit-shake { animation: takeDamage 0.3s ease-in-out; }

@keyframes attackDashRight {
  0% { transform: translateX(0); }
  50% { transform: translateX(200px) scale(1.1); }
  100% { transform: translateX(0); }
}

@keyframes attackDashLeft {
  0% { transform: translateX(0); }
  50% { transform: translateX(-200px) scale(1.1); }
  100% { transform: translateX(0); }
}

@keyframes takeDamage {
  0% { transform: translateX(-10px); filter: brightness(2) drop-shadow(0 0 10px red); }
  50% { transform: translateX(10px); }
  100% { transform: translateX(0); filter: none; }
}
</style>