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

  // Read backend URL from environment variable
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

  onMounted(async () => {
    try {
      const res = await axios.get(`${backendUrl}/health`)
      result.value = res.data
    } catch (err) {
      error.value = err.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  })
</script>
