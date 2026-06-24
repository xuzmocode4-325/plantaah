<template>
  <div class="map-wrap">
    <div id="map" ref="mapEl"></div>
    <div class="map-controls">
      <button v-if="hasPolygon" class="btn btn-danger clear-btn" @click="clearPolygon">
        🗑️ Clear Boundary
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['polygon-drawn', 'polygon-cleared'])
const mapEl = ref(null)
const hasPolygon = ref(false)

let map = null
let drawnItems = null

function calculateArea(latLngs) {
  const R = 6371000
  const n = latLngs.length
  let area = 0
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n
    const xi = latLngs[i].lng * Math.PI / 180
    const yi = latLngs[i].lat * Math.PI / 180
    const xj = latLngs[j].lng * Math.PI / 180
    const yj = latLngs[j].lat * Math.PI / 180
    area += xi * Math.sin(yj) - xj * Math.sin(yi)
  }
  area = Math.abs(area / 2) * R * R
  return area / 10000
}

onMounted(() => {
  // Use globally loaded Leaflet (from CDN script tag in index.html)
  const L = window.L

  if (!L) {
    console.error('Leaflet not loaded')
    return
  }

  map = L.map(mapEl.value, {
    center: [-33.9249, 18.4241],
    zoom: 10
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map)

  drawnItems = new L.FeatureGroup()
  map.addLayer(drawnItems)

  const drawControl = new L.Control.Draw({
    draw: {
      polygon: {
        allowIntersection: false,
        showArea: true,
        shapeOptions: {
          color: '#2d6a4f',
          fillColor: '#52b788',
          fillOpacity: 0.25,
          weight: 3
        }
      },
      polyline: false,
      rectangle: {
        shapeOptions: {
          color: '#2d6a4f',
          fillColor: '#52b788',
          fillOpacity: 0.25,
          weight: 3
        }
      },
      circle: false,
      circlemarker: false,
      marker: false
    },
    edit: {
      featureGroup: drawnItems,
      edit: true,
      remove: true
    }
  })
  map.addControl(drawControl)

  map.on(L.Draw.Event.CREATED, (e) => {
    drawnItems.clearLayers()
    const layer = e.layer
    drawnItems.addLayer(layer)

    const latLngs = layer.getLatLngs ? layer.getLatLngs()[0] : []
    const coords = latLngs.map(ll => [ll.lng, ll.lat])
    if (coords.length > 0) coords.push(coords[0])

    const area = calculateArea(latLngs)
    hasPolygon.value = true

    emit('polygon-drawn', {
      coordinates: coords,
      area,
      pointCount: latLngs.length
    })
  })

  map.on(L.Draw.Event.EDITED, (e) => {
    e.layers.eachLayer((layer) => {
      const latLngs = layer.getLatLngs()[0]
      const coords = latLngs.map(ll => [ll.lng, ll.lat])
      if (coords.length > 0) coords.push(coords[0])
      const area = calculateArea(latLngs)
      emit('polygon-drawn', {
        coordinates: coords,
        area,
        pointCount: latLngs.length
      })
    })
  })

  map.on(L.Draw.Event.DELETED, () => {
    hasPolygon.value = false
    emit('polygon-cleared')
  })
})

function clearPolygon() {
  if (drawnItems) drawnItems.clearLayers()
  hasPolygon.value = false
  emit('polygon-cleared')
}

onUnmounted(() => {
  if (map) map.remove()
})
</script>

<style scoped>
.map-wrap {
  position: relative;
}

#map {
  height: 520px;
  width: 100%;
  background: #e8f4f0;
}

.map-controls {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 1000;
}

.clear-btn {
  font-size: 0.85rem;
  padding: 8px 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
</style>
