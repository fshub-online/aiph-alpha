<template>
  <div>
    <h1>Backend Health Check</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import axios from 'axios'

  const result = ref(null)
  const error = ref(null)
  const loading = ref(true)

  onMounted(async () => {
    try {
      // Adjust the URL if your backend runs on a different host/port
      const res = await axios.get('http://localhost:8000/health')
      result.value = res.data
    } catch (err) {
      error.value = err.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  })
</script>
