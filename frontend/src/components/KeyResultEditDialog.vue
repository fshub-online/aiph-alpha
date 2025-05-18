<template>
  <v-dialog v-model="dialogVisible" max-width="600px">
    <v-card>
      <v-card-title class="py-2 px-3">
        <span class="text-h6">{{ isEdit ? 'Edit' : 'Create' }} Key Result</span>
      </v-card-title>
      <v-card-text class="py-2 px-3">
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.description"
                density="compact"
                hide-details
                label="Description"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.target_value"
                density="compact"
                hide-details
                label="Target Value"
                required
                :rules="[rules.required]"
                type="number"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.current_value"
                density="compact"
                hide-details
                label="Current Value"
                required
                :rules="[rules.required]"
                type="number"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.start_value"
                density="compact"
                hide-details
                label="Start Value"
                type="number"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.unit"
                density="compact"
                hide-details
                label="Unit"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localKeyResult.status"
                density="compact"
                :disabled="!enumOptionsLoaded"
                :items="enumOptions.status"
                label="Status"
                :loading="!enumOptionsLoaded"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localKeyResult.complexity_level"
                density="compact"
                :disabled="!enumOptionsLoaded"
                :items="enumOptions.complexity_level"
                label="Complexity Level"
                :loading="!enumOptionsLoaded"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localKeyResult.due_date"
                density="compact"
                hide-details
                label="Due Date"
                type="date"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localKeyResult.objective_id"
                density="compact"
                :disabled="!objectivesLoaded"
                item-title="title"
                item-value="id"
                :items="objectives"
                label="Objective"
                :loading="!objectivesLoaded"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localKeyResult.team_member_id"
                clearable
                density="compact"
                :disabled="!teamMembersLoaded"
                item-title="name"
                item-value="id"
                :items="teamMembers"
                label="Team Member"
                :loading="!teamMembersLoaded"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="py-2 px-3">
        <v-spacer />
        <v-btn text @click="onCancel">Cancel</v-btn>
        <v-btn color="primary" @click="onSave">Save</v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
  </v-dialog>
</template>
<script setup>
  import { computed, ref, watch } from 'vue'
  import api from '@/api'

  const props = defineProps({
    modelValue: Boolean,
    keyResultId: {
      type: Number,
      required: false,
      default: null,
    },
  })
  const emit = defineEmits(['update:modelValue', 'save', 'cancel'])
  const formRef = ref(null)
  const dialogVisible = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  const localKeyResult = ref(null)
  const enumOptions = ref({ status: [], complexity_level: [] })
  const enumOptionsLoaded = ref(false)
  const objectives = ref([])
  const objectivesLoaded = ref(false)
  const teamMembers = ref([])
  const teamMembersLoaded = ref(false)
  const loading = ref(false)
  const rules = { required: v => !!v || 'Required' }
  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  async function fetchAllData () {
    loading.value = true
    try {
      if (props.keyResultId) {
        const [krRes, enumsRes, objRes, membersRes] = await Promise.all([
          api.get(`/key-results/${props.keyResultId}`),
          api.get('/key-results/enums'),
          api.get('/objectives/'),
          api.get('/team-members/'),
        ])
        localKeyResult.value = krRes.data
        enumOptions.value = enumsRes.data
        enumOptionsLoaded.value = true
        objectives.value = objRes.data
        objectivesLoaded.value = true
        teamMembers.value = membersRes.data.map(tm => ({
          id: tm.id,
          name: tm.first_name + ' ' + tm.last_name + (tm.position ? ` (${tm.position})` : ''),
        }))
        teamMembersLoaded.value = true
      } else {
        const [enumsRes, objRes, membersRes] = await Promise.all([
          api.get('/key-results/enums'),
          api.get('/objectives/'),
          api.get('/team-members/'),
        ])
        localKeyResult.value = {
          description: '',
          target_value: '',
          current_value: '',
          start_value: '',
          unit: '',
          status: '',
          complexity_level: '',
          due_date: '',
          objective_id: null,
          team_member_id: null,
        }
        enumOptions.value = enumsRes.data
        enumOptionsLoaded.value = true
        objectives.value = objRes.data
        objectivesLoaded.value = true
        teamMembers.value = membersRes.data.map(tm => ({
          id: tm.id,
          name: tm.first_name + ' ' + tm.last_name + (tm.position ? ` (${tm.position})` : ''),
        }))
        teamMembersLoaded.value = true
      }
    } catch (e) {
      console.error('Failed to load key result data', e)
      snackbarText.value = 'Failed to load key result data: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }

  watch(() => props.keyResultId, fetchAllData, { immediate: true })

  function onSave () {
    emit('save', localKeyResult.value, formRef.value)
  }
  function onCancel () {
    emit('cancel')
    emit('update:modelValue', false)
  }
</script>
