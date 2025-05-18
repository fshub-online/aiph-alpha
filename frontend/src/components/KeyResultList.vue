<template>
  <div>
    <v-table v-if="keyResults.length" class="key-result-table">
      <thead>
        <tr>
          <th>Due Date</th>
          <th>Title</th>
          <th>Start</th>
          <th>Current</th>
          <th>Target</th>
          <th style="width: 80px;">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="kr in keyResults" :key="kr.id">
          <td>{{ kr.due_date ? (new Date(kr.due_date)).toLocaleDateString() : '-' }}</td>
          <td>{{ kr.title }}</td>
          <td>{{ kr.start_value ?? '-' }}</td>
          <td>{{ kr.current_value ?? '-' }}</td>
          <td>{{ kr.target_value ?? '-' }}</td>
          <td>
            <v-btn icon size="small" @click="$emit('edit', kr)"><v-icon size="18">mdi-pencil</v-icon></v-btn>
            <v-btn color="error" icon size="small" @click="$emit('delete', kr)"><v-icon size="18">mdi-delete</v-icon></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <v-alert v-else type="info">No key results for this objective.</v-alert>
  </div>
</template>

<script setup>
  defineProps({
    keyResults: {
      type: Array,
      required: true,
    },
  })

  defineEmits(['edit', 'delete'])
</script>

<style scoped>
.key-result-table {
  margin-bottom: 1.5rem;
}
.key-result-table th, .key-result-table td {
  padding: 0.5rem 0.75rem;
  font-size: 0.97em;
}
.key-result-table th {
  background: #f5f7fa;
  font-weight: 600;
  color: #1976d2;
}
.key-result-table td {
  background: #fff;
}
</style>
