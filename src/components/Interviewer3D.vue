<template>
    <div class="canvas-container" ref="containerRef">
      <!-- 3D 画布将挂载在这里 -->
      <div v-if="isLoading" class="loading-overlay">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在请面试官入座 ({{ loadProgress }}%)...</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount, shallowRef, watch } from 'vue'
  import * as THREE from 'three'
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
  import { Loading } from '@element-plus/icons-vue'
  import { useInterviewStore } from '../stores/interview'
  
  const interviewStore = useInterviewStore()
  
  const containerRef = ref(null)
  const isLoading = ref(true)
  const loadProgress = ref(0)
  
  const scene = shallowRef(null)
  const camera = shallowRef(null)
  const renderer = shallowRef(null)
  const avatar = shallowRef(null)
  const deskRef = shallowRef(null)
  
  let animationFrameId = null
  
  // === Web Audio API 频谱分析器变量 ===
  let audioContext = null
  let analyser = null
  let dataArray = null
  
  // === 面部控制器与目标值 ===
  const mouthControllers = {
    jawOpen: [],
    mouthSmile:[],
    mouthPucker: [],
    eyeBlink:[] // 眨眼数组
  }
  
  let targetJaw = 0
  let targetSmile = 0
  let targetPucker = 0
  let spineBone = null 
  
  // 眨眼系统的状态变量
  let nextBlinkTime = Date.now() + 2000 + Math.random() * 3000; 
  let currentBlinkWeight = 0; 
  let isBlinking = false;
  let blinkStartTime = 0;
  
  const lerp = (start, end, amt) => (1 - amt) * start + amt * end
  
  // === 1. 初始化 3D 影棚 ===
  const initScene = () => {
    const width = containerRef.value.clientWidth
    const height = containerRef.value.clientHeight
  
    scene.value = new THREE.Scene()
    // [保留你微调的颜色]
    scene.value.background = new THREE.Color('#d3d3d3')
    scene.value.fog = new THREE.Fog('#e4e7eb', 2, 8)
  
    // [保留你微调的机位]
    camera.value = new THREE.PerspectiveCamera(40, width / height, 0.1, 100)
    camera.value.position.set(0.2, 1.35, 1) 
    camera.value.lookAt(0, 1.45, 0) 
  
    renderer.value = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.value.setSize(width, height)
    renderer.value.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.value.outputColorSpace = THREE.SRGBColorSpace
    renderer.value.shadowMap.enabled = true
    renderer.value.shadowMap.type = THREE.PCFSoftShadowMap
    
    containerRef.value.appendChild(renderer.value.domElement)
  
    setupLighting()
    loadDesk()
  }
  
  // === 2. 演播室高级打光 ===
  const setupLighting = () => {
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5)
    scene.value.add(ambientLight)
  
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2)
    dirLight.position.set(1, 2, 3)
    dirLight.castShadow = true
    dirLight.shadow.mapSize.width = 1024
    dirLight.shadow.mapSize.height = 1024
    scene.value.add(dirLight)
  }
  
  const loadDesk = () => {
    const loader = new GLTFLoader()
    loader.load('./desk/scene.gltf', (gltf) => {
      const desk = gltf.scene
      desk.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })
      //[保留你微调的桌子位置和旋转]
      desk.position.set(0, 0.4, 0.2) 
      desk.scale.set(1.2, 1, 1.2) 
      desk.rotation.x = 0.08
      deskRef.value = desk
      scene.value.add(desk)
    }, undefined, (error) => {
      console.error('❌ 桌子模型加载失败:', error)
    })
  }
  
  // === 3. 请面试官入场，并进行骨骼正骨与神经搜索 ===
  const loadAvatar = () => {
    const loader = new GLTFLoader()
    loader.load('./interviewer.glb', 
      (gltf) => {
        const model = gltf.scene
        //[保留你微调的人物位置]
        model.position.set(0, 0.07, -0.45)
        model.rotation.x = 0.1
  
        let foundFace = false;
  
        model.traverse((child) => {
          if (child.isMesh || child.isSkinnedMesh) {
            child.castShadow = true
            child.receiveShadow = true
            
            // === 寻找面部表情基键 ===
            if (child.morphTargetDictionary) {
              foundFace = true;
              const dict = child.morphTargetDictionary
              
              // 找嘴巴
              if (dict['jawOpen'] !== undefined) mouthControllers.jawOpen.push({ mesh: child, index: dict['jawOpen'] })
              else if (dict['mouthOpen'] !== undefined) mouthControllers.jawOpen.push({ mesh: child, index: dict['mouthOpen'] })
              
              if (dict['mouthSmile'] !== undefined) mouthControllers.mouthSmile.push({ mesh: child, index: dict['mouthSmile'] })
              else if (dict['mouthSmileLeft'] !== undefined) mouthControllers.mouthSmile.push({ mesh: child, index: dict['mouthSmileLeft'] })
              
              if (dict['mouthPucker'] !== undefined) mouthControllers.mouthPucker.push({ mesh: child, index: dict['mouthPucker'] })
              
              // 找眼睛 (眨眼神经)
              if (dict['eyeBlinkLeft'] !== undefined) mouthControllers.eyeBlink.push({ mesh: child, index: dict['eyeBlinkLeft'] })
              if (dict['eyeBlinkRight'] !== undefined) mouthControllers.eyeBlink.push({ mesh: child, index: dict['eyeBlinkRight'] })
              if (dict['eyesClosed'] !== undefined) mouthControllers.eyeBlink.push({ mesh: child, index: dict['eyesClosed'] })
            }
          }
        })
  
        if (!foundFace) console.warn('⚠️ 严重警告：在这个模型身上没有找到任何表情控制器！')
  
        const getBone = (name) => model.getObjectByName(name) || model.getObjectByName('mixamorig' + name)
        
        const leftArm = getBone('LeftArm')
        const rightArm = getBone('RightArm')
        const leftForeArm = getBone('LeftForeArm')
        const rightForeArm = getBone('RightForeArm')
        const leftHand = getBone('LeftHand')
        const rightHand = getBone('RightHand')
        const neck = getBone('Neck')
        const head = getBone('Head')
        spineBone = getBone('Spine') || getBone('Spine1')
  
        //[保留你的完美骨骼参数]
        if (leftArm) { leftArm.rotation.set(1.4, 0, 0.4); } 
        if (rightArm) { rightArm.rotation.set(1.4, 0, -0.4); } 
        
        if (leftForeArm) { leftForeArm.rotation.set(0.5, 0.4, 1); }
        if (rightForeArm) { rightForeArm.rotation.set(0.5, -0.6, -1); }
        
        if (leftHand) { leftHand.rotation.set(0, 0.4, 0); }
        if (rightHand) { rightHand.rotation.set(0, -0.5, 0); }
  
        if (neck) { neck.rotation.x = 0.1; }
        if (head) { head.rotation.x = 0.4; }
        
        avatar.value = model
        scene.value.add(model)
        isLoading.value = false
      },
      (xhr) => {
        loadProgress.value = Math.round((xhr.loaded / xhr.total) * 100)
      },
      (error) => {
        console.error('❌ 面试官模型加载失败:', error)
        isLoading.value = false
      }
    )
  }
  
  const initAudioAnalyser = (mediaStreamTrack) => {
    if (!audioContext) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext
      audioContext = new AudioContextClass()
      analyser = audioContext.createAnalyser()
      analyser.fftSize = 512 
      dataArray = new Uint8Array(analyser.frequencyBinCount) 
    }
  
    if (audioContext.state === 'suspended') {
      audioContext.resume()
    }
  
    const stream = new MediaStream([mediaStreamTrack])
    const source = audioContext.createMediaStreamSource(stream)
    source.connect(analyser)
  }
  
  watch(() => interviewStore.remoteAudioTrack, (newTrack) => {
    if (newTrack && newTrack.mediaStreamTrack) {
      initAudioAnalyser(newTrack.mediaStreamTrack)
    }
  }, { deep: true, immediate: true }) 
  
  // === 5. 渲染循环与平滑驱动系统 ===
  const animate = () => {
    animationFrameId = requestAnimationFrame(animate)
    
    const now = Date.now();
  
    // 身体轻微呼吸
    if (spineBone) {
      spineBone.rotation.x = Math.sin(now * 0.0015) * 0.015
    }
  
    if (audioContext && audioContext.state === 'suspended' && interviewStore.aiIsSpeaking) {
      audioContext.resume()
    }
  
    // === 眨眼系统逻辑 ===
    if (!isBlinking && now > nextBlinkTime) {
      isBlinking = true;
      blinkStartTime = now;
    }
    if (isBlinking) {
      const elapsed = now - blinkStartTime;
      if (elapsed < 80) {
        currentBlinkWeight = elapsed / 80.0;
      } else if (elapsed < 200) {
        currentBlinkWeight = 1.0 - ((elapsed - 80) / 120.0);
      } else {
        isBlinking = false;
        currentBlinkWeight = 0;
        nextBlinkTime = now + 2000 + Math.random() * 3000;
      }
    }
  
    // === 音频驱动与音节律动逻辑 ===
    if (analyser && avatar.value && interviewStore.aiIsSpeaking) {
      analyser.getByteFrequencyData(dataArray)
      
      let sum = 0;
      const startBin = 2;
      const endBin = 30;
      for (let i = startBin; i < endBin; i++) {
        sum += dataArray[i];
      }
      const average = (sum / (endBin - startBin)) / 255.0;
  
      const maxOpen = 0.35; 
      const sensitivity = 2.0; 
  
      // 音节律动魔法：让嘴巴像蹦字一样自然张合
      const syllablePulse = 0.2 + 0.8 * Math.abs(Math.sin(now * 0.008));
  
      let baseVolume = average > 0.02 ? Math.min(maxOpen, average * sensitivity) : 0;
      targetJaw = baseVolume * syllablePulse;
    } else {
      targetJaw = 0;
    }
  
    // 执行驱动：嘴巴
    mouthControllers.jawOpen.forEach(({ mesh, index }) => {
      mesh.morphTargetInfluences[index] = lerp(mesh.morphTargetInfluences[index], targetJaw, 0.25)
    });
  
    // 执行驱动：眼睛
    mouthControllers.eyeBlink.forEach(({ mesh, index }) => {
      mesh.morphTargetInfluences[index] = lerp(mesh.morphTargetInfluences[index], currentBlinkWeight, 0.6)
    });
  
    if (renderer.value && scene.value && camera.value) {
      renderer.value.render(scene.value, camera.value)
    }
  }
    
  const handleResize = () => {
    if (!containerRef.value || !camera.value || !renderer.value) return
    const width = containerRef.value.clientWidth
    const height = containerRef.value.clientHeight
    camera.value.aspect = width / height
    camera.value.updateProjectionMatrix()
    renderer.value.setSize(width, height)
  }
  
  onMounted(() => {
    initScene()
    loadAvatar()
    animate()
    window.addEventListener('resize', handleResize)
  })
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
    if (animationFrameId) cancelAnimationFrame(animationFrameId)
    
    if (renderer.value) {
      renderer.value.dispose()
      renderer.value.forceContextLoss()
      renderer.value.domElement.remove()
    }
    if (audioContext && audioContext.state !== 'closed') {
      audioContext.close()
    }
    //[执行安全清理逻辑，资源释放完毕]
  })
  </script>

<style scoped>
.canvas-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 16px; /* 更贴合悬浮窗的圆角 */
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(240, 242, 245, 0.9); /* 浅色加载背景 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: var(--primary-color);
  font-size: 14px;
  font-weight: bold;
  z-index: 10;
}

.is-loading {
  font-size: 32px;
  margin-bottom: 12px;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  100% { transform: rotate(360deg); }
}
</style>