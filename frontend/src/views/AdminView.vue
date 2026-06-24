<template>
  <div class="admin">
    <div class="admin-wrap">
      <div class="admin-header">
        <h1>📊 Admin Dashboard</h1>
        <p class="admin-sub">View and manage all site analysis submissions.</p>
        <div class="admin-actions">
          <select v-model="statusFilter" class="filter-select">
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
          <button class="btn btn-primary" @click="fetchSubmissions">🔄 Refresh</button>
          <button class="btn btn-secondary" @click="exportCsv">⬇️ Export CSV</button>
        </div>
      </div>

      <!-- Stats row -->
      <div class="stats-row">
        <div class="stat-card card" v-for="s in stats" :key="s.label">
          <span class="stat-num">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>

      <!-- Table -->
      <div class="table-wrap card">
        <div v-if="loading" class="table-loading">
          <div class="spinner"></div>
          <span>Loading submissions...</span>
        </div>
        <div v-else-if="error" class="table-error">⚠️ {{ error }}</div>
        <div v-else-if="filteredSubmissions.length === 0" class="table-empty">
          No submissions found.
        </div>
        <table v-else class="submissions-table">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>Email</th>
              <th>Area (ha)</th>
              <th>Status</th>
              <th>Submitted</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sub in filteredSubmissions" :key="sub.id" @click="selectedSub = sub">
              <td>{{ sub.project_name }}</td>
              <td>{{ sub.email }}</td>
              <td>{{ sub.area_hectares?.toFixed(2) }}</td>
              <td>
                <span class="badge" :class="statusBadge(sub.status)">{{ sub.status }}</span>
              </td>
              <td>{{ formatDate(sub.created_at) }}</td>
              <td>
                <button class="btn-link" @click.stop="selectedSub = sub">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Detail Modal -->
      <div class="modal-overlay" v-if="selectedSub" @click.self="selectedSub = null">
        <div class="modal card">
          <div class="modal-header">
            <h2>{{ selectedSub.project_name }}</h2>
            <button class="modal-close" @click="selectedSub = null">✕</button>
          </div>
          <div class="modal-body">
            <div class="detail-grid">
              <div class="detail-item">
                <span class="d-label">Email</span>
                <span>{{ selectedSub.email }}</span>
              </div>
              <div class="detail-item">
                <span class="d-label">Status</span>
                <span class="badge" :class="statusBadge(selectedSub.status)">{{ selectedSub.status }}</span>
              </div>
              <div class="detail-item">
                <span class="d-label">Area</span>
                <span>{{ selectedSub.area_hectares?.toFixed(2) }} ha</span>
              </div>
              <div class="detail-item">
                <span class="d-label">Submitted</span>
                <span>{{ formatDate(selectedSub.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="d-label">Completed</span>
                <span>{{ selectedSub.completed_at ? formatDate(selectedSub.completed_at) : '—' }}</span>
              </div>
              <div class="detail-item" v-if="selectedSub.error_message">
                <span class="d-label">Error</span>
                <span class="error-text">{{ selectedSub.error_message }}</span>
              </div>
            </div>
            <div class="analysis-data" v-if="selectedSub.analysis_data">
              <h3>Analysis Data</h3>
              <pre>{{ JSON.stringify(selectedSub.analysis_data, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const submissions = ref([])
const loading = ref(false)
const error = ref('')
const statusFilter = ref('')
const selectedSub = ref(null)

const filteredSubmissions = computed(() => {
  if (!statusFilter.value) return submissions.value
  return submissions.value.filter(s => s.status === statusFilter.value)
})

const stats = computed(() => [
  { label: 'Total', value: submissions.value.length },
  { label: 'Pending', value: submissions.value.filter(s => s.status === 'pending').length },
  { label: 'Completed', value: submissions.value.filter(s => s.status === 'completed').length },
  { label: 'Failed', value: submissions.value.filter(s => s.status === 'failed').length }
])

function statusBadge(status) {
  return {
    pending: 'badge-info',
    processing: 'badge-warning',
    completed: 'badge-success',
    failed: 'badge-error'
  }[status] || 'badge-info'
}

function formatDate(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleString()
}

async function fetchSubmissions() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get('/api/admin/submissions')
    submissions.value = res.data
  } catch (e) {
    error.value = 'Could not load submissions. Make sure the API key is set or check server connection.'
  } finally {
    loading.value = false
  }
}

async function exportCsv() {
  try {
    const res = await axios.get('/api/admin/export', { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = 'plantaah_submissions.csv'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('Export failed.')
  }
}

onMounted(fetchSubmissions)
</script>

<style scoped>
.admin {
  padding: 24px;
}
.admin-wrap {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.admin-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.admin-header h1 { font-size: 1.8rem; color: var(--green-dark); }
.admin-sub { color: var(--text-mid); }
.admin-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 4px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 14px;
  border: 2px solid var(--cream-dark);
  border-radius: 8px;
  font-size: 0.9rem;
  background: var(--white);
  cursor: pointer;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
@media (max-width: 600px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }

.stat-card {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.stat-num { font-size: 2rem; font-weight: 800; color: var(--green-mid); }
.stat-label { font-size: 0.85rem; color: var(--text-mid); }

.table-wrap { overflow-x: auto; }
.table-loading, .table-error, .table-empty {
  padding: 48px;
  text-align: center;
  color: var(--text-mid);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.spinner {
  width: 28px; height: 28px;
  border: 3px solid var(--cream-dark);
  border-top-color: var(--green-mid);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.submissions-table {
  width: 100%;
  border-collapse: collapse;
}
.submissions-table th, .submissions-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--cream-dark);
  font-size: 0.9rem;
}
.submissions-table th {
  background: var(--cream);
  font-weight: 700;
  color: var(--text-dark);
}
.submissions-table tr:hover td { background: #f9f9f6; cursor: pointer; }

.btn-link {
  background: none;
  border: none;
  color: var(--green-mid);
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}
.btn-link:hover { text-decoration: underline; }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.modal {
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--cream-dark);
}
.modal-header h2 { font-size: 1.2rem; }
.modal-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--text-mid);
}
.modal-body { padding: 24px; display: flex; flex-direction: column; gap: 20px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.d-label { font-size: 0.78rem; color: var(--text-mid); font-weight: 600; text-transform: uppercase; }
.error-text { color: #dc3545; font-size: 0.85rem; }
.analysis-data h3 { margin-bottom: 8px; font-size: 1rem; }
.analysis-data pre {
  background: var(--cream);
  padding: 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  overflow-x: auto;
  max-height: 200px;
}
</style>
