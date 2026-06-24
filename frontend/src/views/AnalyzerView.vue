<template>
  <div class="analyzer">
    <!-- Hero Section -->
    <section class="hero" v-if="step === 'form'">
      <div class="hero-content">
        <h1 class="hero-title">Your Eco-Farming Guide<br><span class="highlight">in 5 Minutes</span></h1>
        <p class="hero-sub">Draw your property boundary on the map, enter your details, and receive a personalized 12-month eco-farming guide via email — no GIS expertise needed.</p>
      </div>
    </section>

    <!-- Main Content -->
    <div class="content-wrap">
      <!-- FORM STEP -->
      <div v-if="step === 'form'" class="main-layout">
        <!-- Left: Form -->
        <div class="form-panel card">
          <h2 class="panel-title">Site Details</h2>

          <div class="form-group">
            <label for="project-name">Project Name *</label>
            <input
              id="project-name"
              v-model="form.projectName"
              :class="{ error: errors.projectName }"
              type="text"
              placeholder="e.g. My Farm — Western Cape"
              @input="errors.projectName = ''"
            />
            <span class="error-msg" v-if="errors.projectName">{{ errors.projectName }}</span>
          </div>

          <div class="form-group">
            <label for="email">Email Address *</label>
            <input
              id="email"
              v-model="form.email"
              :class="{ error: errors.email }"
              type="email"
              placeholder="you@example.com"
              @input="errors.email = ''"
            />
            <span class="error-msg" v-if="errors.email">{{ errors.email }}</span>
          </div>

          <!-- Polygon Status -->
          <div class="polygon-status" :class="polygonStatusClass">
            <div class="status-row">
              <span class="status-icon">{{ polygonStatusIcon }}</span>
              <span class="status-text">{{ polygonStatusText }}</span>
            </div>
            <div v-if="polygon.area > 0" class="area-display">
              <strong>{{ polygon.area.toFixed(2) }} hectares</strong>
              <span v-if="polygon.area < 0.1" class="warn-text">⚠️ Area too small (min 0.1 ha)</span>
              <span v-else-if="polygon.area > 500" class="warn-text">⚠️ Area too large (max 500 ha)</span>
              <span v-else class="ok-text">✅ Valid site area</span>
            </div>
          </div>

          <div v-if="errors.polygon" class="error-msg">{{ errors.polygon }}</div>

          <button
            class="btn btn-primary submit-btn"
            :disabled="!canSubmit"
            @click="handleSubmit"
          >
            🚀 Submit for Analysis
          </button>

          <p class="privacy-note">Your email is used only to deliver your guide. See our <a href="#">Privacy Policy</a>.</p>
        </div>

        <!-- Right: Map -->
        <div class="map-panel card">
          <div class="map-header">
            <h2 class="panel-title">Draw Your Property Boundary</h2>
            <div class="map-instructions">
              <span>1. Click the polygon tool <strong>◻</strong></span>
              <span>2. Click to place at least 4 points</span>
              <span>3. Close the shape to finish</span>
            </div>
          </div>
          <MapComponent @polygon-drawn="onPolygonDrawn" @polygon-cleared="onPolygonCleared" />
        </div>
      </div>

      <!-- LOADING STEP -->
      <div v-else-if="step === 'loading'" class="loading-panel card">
        <div class="loading-inner">
          <div class="spinner-wrap">
            <div class="spinner"></div>
          </div>
          <h2>Analyzing Your Site...</h2>
          <p class="loading-sub">We're collecting topography, climate, and vegetation data for your property.</p>
          <div class="progress-steps">
            <div
              v-for="(msg, i) in progressMessages"
              :key="i"
              class="progress-step"
              :class="{ active: i === currentProgressIdx, done: i < currentProgressIdx }"
            >
              <span class="step-icon">{{ i < currentProgressIdx ? '✅' : i === currentProgressIdx ? '⏳' : '⭕' }}</span>
              <span>{{ msg }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- SUCCESS STEP -->
      <div v-else-if="step === 'success'" class="success-panel card">
        <div class="success-inner">
          <div class="success-icon">🌿</div>
          <h2>Your Guide is Being Generated!</h2>
          <p class="success-sub">Check <strong>{{ form.email }}</strong> in 5–10 minutes for your personalized eco-farming guide.</p>

          <div class="summary-grid">
            <div class="summary-card">
              <span class="s-icon">📍</span>
              <span class="s-label">Project</span>
              <span class="s-value">{{ form.projectName }}</span>
            </div>
            <div class="summary-card">
              <span class="s-icon">📐</span>
              <span class="s-label">Site Area</span>
              <span class="s-value">{{ polygon.area.toFixed(2) }} ha</span>
            </div>
            <div class="summary-card">
              <span class="s-icon">🗂️</span>
              <span class="s-label">Status</span>
              <span class="s-value">Processing</span>
            </div>
          </div>

          <div class="what-next">
            <h3>What to expect in your guide:</h3>
            <ul>
              <li>🌾 Crop recommendations based on your climate & soil</li>
              <li>💧 Water management strategy for your site</li>
              <li>📅 12-month planting calendar</li>
              <li>🌡️ Climate risk alerts & mitigation tips</li>
              <li>🗺️ Topography & vegetation analysis</li>
            </ul>
          </div>

          <button class="btn btn-primary" @click="resetForm">
            ➕ Analyze Another Site
          </button>
        </div>
      </div>

      <!-- ERROR STEP -->
      <div v-else-if="step === 'error'" class="error-panel card">
        <div class="error-inner">
          <div class="error-icon">⚠️</div>
          <h2>Something Went Wrong</h2>
          <p>{{ errorMessage }}</p>
          <button class="btn btn-primary" @click="step = 'form'">Try Again</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import MapComponent from '../components/MapComponent.vue'
import axios from 'axios'

const step = ref('form')
const errorMessage = ref('')
const currentProgressIdx = ref(0)

const form = reactive({
  projectName: '',
  email: ''
})

const polygon = reactive({
  coordinates: null,
  area: 0,
  pointCount: 0
})

const errors = reactive({
  projectName: '',
  email: '',
  polygon: ''
})

const progressMessages = [
  'Validating your site boundary...',
  'Fetching elevation & topography data...',
  'Analyzing climate patterns...',
  'Calculating vegetation index (NDVI)...',
  'Generating your eco-farming guide...',
  'Sending guide to your email...'
]

const polygonStatusClass = computed(() => {
  if (!polygon.coordinates) return 'status-empty'
  if (polygon.pointCount < 4) return 'status-warn'
  if (polygon.area < 0.1 || polygon.area > 500) return 'status-warn'
  return 'status-ok'
})

const polygonStatusIcon = computed(() => {
  if (!polygon.coordinates) return '🗺️'
  if (polygon.pointCount < 4) return '⚠️'
  if (polygon.area < 0.1 || polygon.area > 500) return '⚠️'
  return '✅'
})

const polygonStatusText = computed(() => {
  if (!polygon.coordinates) return 'No boundary drawn yet — use the map on the right'
  if (polygon.pointCount < 4) return `Only ${polygon.pointCount} points — minimum 4 required`
  return `Polygon with ${polygon.pointCount} points drawn`
})

const isPolygonValid = computed(() => {
  return polygon.coordinates && polygon.pointCount >= 4 && polygon.area >= 0.1 && polygon.area <= 500
})

const canSubmit = computed(() => {
  return form.projectName.trim().length >= 3 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) &&
    isPolygonValid.value
})

function onPolygonDrawn(data) {
  polygon.coordinates = data.coordinates
  polygon.area = data.area
  polygon.pointCount = data.pointCount
  errors.polygon = ''
}

function onPolygonCleared() {
  polygon.coordinates = null
  polygon.area = 0
  polygon.pointCount = 0
}

function validate() {
  let valid = true
  if (form.projectName.trim().length < 3) {
    errors.projectName = 'Project name must be at least 3 characters'
    valid = false
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    valid = false
  }
  if (!isPolygonValid.value) {
    errors.polygon = 'Please draw a valid boundary with at least 4 points (0.1–500 ha)'
    valid = false
  }
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  step.value = 'loading'
  currentProgressIdx.value = 0

  const interval = setInterval(() => {
    if (currentProgressIdx.value < progressMessages.length - 1) {
      currentProgressIdx.value++
    }
  }, 2000)

  try {
    const payload = {
      project_name: form.projectName,
      email: form.email,
      polygon: {
        type: 'Polygon',
        coordinates: [polygon.coordinates]
      },
      area_hectares: polygon.area
    }
    await axios.post('/api/submit-analysis', payload)
    clearInterval(interval)
    currentProgressIdx.value = progressMessages.length - 1
    setTimeout(() => { step.value = 'success' }, 500)
  } catch (err) {
    clearInterval(interval)
    errorMessage.value = err.response?.data?.detail || 'Analysis failed. Please try again.'
    step.value = 'error'
  }
}

function resetForm() {
  form.projectName = ''
  form.email = ''
  polygon.coordinates = null
  polygon.area = 0
  polygon.pointCount = 0
  errors.projectName = ''
  errors.email = ''
  errors.polygon = ''
  step.value = 'form'
}
</script>

<style scoped>
.analyzer {
  min-height: calc(100vh - 60px);
}

.hero {
  background: linear-gradient(135deg, var(--green-dark) 0%, var(--green-mid) 100%);
  color: var(--white);
  padding: 40px 24px 32px;
  text-align: center;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 12px;
}

.highlight {
  color: var(--green-pale);
}

.hero-sub {
  max-width: 600px;
  margin: 0 auto;
  opacity: 0.9;
  font-size: 1.05rem;
  line-height: 1.6;
}

.content-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.main-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
  align-items: start;
}

@media (max-width: 900px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
}

.form-panel {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--green-dark);
  margin-bottom: 4px;
}

.polygon-status {
  padding: 14px;
  border-radius: 8px;
  border: 2px solid;
}
.status-empty { border-color: var(--cream-dark); background: var(--cream); }
.status-warn { border-color: #f59e0b; background: #fffbeb; }
.status-ok { border-color: var(--green-light); background: #f0fdf4; }

.status-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  margin-bottom: 6px;
}

.area-display {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.9rem;
}
.warn-text { color: #92400e; }
.ok-text { color: #065f46; }

.submit-btn {
  width: 100%;
  justify-content: center;
  padding: 14px;
  font-size: 1.05rem;
}

.privacy-note {
  font-size: 0.8rem;
  color: var(--text-mid);
  text-align: center;
}
.privacy-note a { color: var(--green-mid); }

.map-panel {
  overflow: hidden;
}
.map-header {
  padding: 20px 20px 12px;
}
.map-instructions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 0.85rem;
  color: var(--text-mid);
  margin-top: 6px;
}
.map-instructions span {
  background: var(--cream);
  padding: 4px 10px;
  border-radius: 20px;
}

/* Loading */
.loading-panel, .success-panel, .error-panel {
  max-width: 640px;
  margin: 0 auto;
  padding: 48px 40px;
  text-align: center;
}

.loading-inner, .success-inner, .error-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner-wrap { margin-bottom: 8px; }
.spinner {
  width: 56px;
  height: 56px;
  border: 5px solid var(--cream-dark);
  border-top-color: var(--green-mid);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.loading-sub, .success-sub {
  color: var(--text-mid);
  font-size: 1rem;
}

.progress-steps {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.progress-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--cream);
  color: var(--text-mid);
  font-size: 0.9rem;
  transition: all 0.3s;
}
.progress-step.active {
  background: #f0fdf4;
  color: var(--green-dark);
  font-weight: 600;
}
.progress-step.done {
  color: #065f46;
}

.success-icon, .error-icon { font-size: 4rem; }

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  width: 100%;
}
.summary-card {
  background: var(--cream);
  border-radius: 8px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.s-icon { font-size: 1.5rem; }
.s-label { font-size: 0.78rem; color: var(--text-mid); }
.s-value { font-weight: 700; font-size: 0.95rem; }

.what-next {
  background: var(--cream);
  border-radius: 12px;
  padding: 20px 24px;
  text-align: left;
  width: 100%;
}
.what-next h3 {
  font-size: 1rem;
  margin-bottom: 12px;
  color: var(--green-dark);
}
.what-next ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.what-next li { font-size: 0.9rem; color: var(--text-mid); }
</style>
