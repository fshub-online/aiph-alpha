<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <v-btn color="primary" @click="openCreateDialog">Create Key Result</v-btn>
      </v-col>
    </v-row>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      item-key="id"
      :items="keyResults"
      :loading="loading"
      :search="search"
    >
      <template #top>
        <v-text-field v-model="search" class="mx-4" clearable label="Search" />
      </template>
      <template #item.actions="{ item }">
        <v-btn color="primary" icon size="small" @click="openEditDialog(item)"><v-icon>mdi-pencil</v-icon></v-btn>
        <v-btn color="error" icon size="small" @click="openDeleteDialog(item)"><v-icon>mdi-delete</v-icon></v-btn>
      </template>
    </v-data-table>

    <KeyResultEditDialog
      v-model="showDialog"
      :key-result-id="dialogKeyResultId"
      @cancel="() => { showDialog = false }"
      @save="handleSaveKeyResult"
    />

    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Delete Key Result</v-card-title>
        <v-card-text>Are you sure you want to delete this key result?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteKeyResult">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>

    <v-row class="mt-8">
      <v-col cols="12">
        <router-link class="back-icon-link" to="/aiph">
          <v-icon size="48">mdi-arrow-left-circle-outline</v-icon>
          <span>Back to Hub</span>
        </router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import KeyResultEditDialog from '@/components/KeyResultEditDialog.vue'
  import api from '@/api'

  const keyResults = ref([])
  const loading = ref(false)
  const showDialog = ref(false)
  const search = ref('')
  const dialogKeyResultId = ref(null)
  const showDeleteDialog = ref(false)
  const deleteKeyResultId = ref(null)

  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  const headers = [
    { title: 'ID', value: 'id' },
    { title: 'Title', value: 'title' },
    { title: 'Start', value: 'start_value' },
    { title: 'Current', value: 'current_value' },
    { title: 'Target', value: 'target_value' },
    { title: 'Unit', value: 'unit' },
    { title: 'Status', value: 'status' },
    { title: 'Due Date', value: 'due_date' },
    { title: 'Actions', value: 'actions', sortable: false },
  ]

  async function fetchKeyResults () {
    loading.value = true
    try {
      const res = await api.get('/key-results/')
      keyResults.value = res.data
    } catch (e) {
      snackbarText.value = 'Failed to load key results: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }

  function openCreateDialog () {
    dialogKeyResultId.value = null
    showDialog.value = true
  }

  function openEditDialog (item) {
    dialogKeyResultId.value = item.id
    showDialog.value = true
  }

  function openDeleteDialog (item) {
    deleteKeyResultId.value = item.id
    showDeleteDialog.value = true
  }

  async function handleSaveKeyResult (kr, formRef) {
    if (formRef && formRef.validate && !formRef.validate()) return;
    try {
      if (dialogKeyResultId.value) {
        await api.put(`/key-results/${dialogKeyResultId.value}`, kr)
        snackbarText.value = 'Key Result updated successfully.'
      } else {
        await api.post('/key-results/', kr)
        snackbarText.value = 'Key Result created successfully.'
      }
      snackbarColor.value = 'success'
      snackbar.value = true
      showDialog.value = false
      await fetchKeyResults()
    } catch (e) {
      snackbarText.value = 'Failed to save key result: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  async function deleteKeyResult () {
    try {
      await api.delete(`/key-results/${deleteKeyResultId.value}`)
      showDeleteDialog.value = false
      await fetchKeyResults()
      snackbarText.value = 'Key Result deleted.'
      snackbarColor.value = 'success'
      snackbar.value = true
    } catch (e) {
      snackbarText.value = 'Failed to delete key result: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  onMounted(fetchKeyResults)
</script>

<style scoped>
.centered-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
.back-icon-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: inherit;
  text-decoration: none;
  transition: color 0.2s;
}
.back-icon-link:hover {
  color: #1976d2;
}
</style>
