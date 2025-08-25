<template>
  <div>
    <h2>Players</h2>
    <button @click="fetchPlayers">Load Players</button>
    <ul>
      <li v-for="p in players" :key="p.id">{{ p.name }} ({{ p.email }})</li>
    </ul>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../axios";

const players = ref([]);
const error = ref("");

async function fetchPlayers() {
  error.value = "";
  try {
    const res = await api.get("/players/?skip=0&limit=20");
    players.value = res.data;
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message;
  }
}
</script>
