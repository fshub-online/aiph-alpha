<template>
  <div>
    <v-table v-if="keyResults.length">
      <thead>
        <tr>
          <th>Due Date</th>
          <th>Title</th>
          <th>Start / Current / Target</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="kr in keyResults" :key="kr.id">
          <td>
            {{ kr.due_date }}
          </td>
          <td>{{ kr.title }}</td>
          <td>{{ kr.start_value ?? "-" }} / {{ kr.current_value ?? "-" }} / {{ kr.target_value ?? "-" }}</td>
          <td>
            <v-btn
              icon
              size="small"
              @click="$emit('edit', kr)"
            ><v-icon size="18">mdi-pencil</v-icon></v-btn>
            <v-btn
              color="error"
              icon
              size="small"
              @click="$emit('delete', kr)"
            ><v-icon size="18">mdi-delete</v-icon></v-btn>
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
  });

  defineEmits(['edit', 'delete']);
</script>
