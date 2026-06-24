<template>
  <div id="app-root">
    <header class="app-header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">🌱</span>
          <span class="logo-text">Plantaah</span>
        </div>
        <nav class="header-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="nav-btn"
            :class="{ active: currentView === tab.id }"
            @click="currentView = tab.id"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <AnalyzerView v-if="currentView === 'analyzer'" />
      <AdminView v-else-if="currentView === 'admin'" />
    </main>

    <footer class="app-footer">
      <p>© 2026 Plantaah · Eco-Farming Context Analyzer · <a href="#">Privacy Policy</a></p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AnalyzerView from './views/AnalyzerView.vue'
import AdminView from './views/AdminView.vue'

const currentView = ref('analyzer')
const tabs = [
  { id: 'analyzer', label: '🗺️ Analyzer' },
  { id: 'admin', label: '📊 Admin' }
]
</script>

<style scoped>
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--green-dark);
  color: var(--white);
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon { font-size: 1.8rem; }
.logo-text {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: var(--green-pale);
}

.header-nav {
  display: flex;
  gap: 4px;
}

.nav-btn {
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.75);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-btn:hover, .nav-btn.active {
  background: rgba(255,255,255,0.15);
  color: var(--white);
}

.app-main {
  flex: 1;
}

.app-footer {
  background: var(--green-dark);
  color: rgba(255,255,255,0.6);
  text-align: center;
  padding: 16px;
  font-size: 0.85rem;
}

.app-footer a {
  color: var(--green-pale);
  text-decoration: none;
}
</style>
