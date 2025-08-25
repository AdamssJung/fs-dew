<template>
  <div>
    <h2>Players</h2>
    <button @click="fetchPlayers">Load Players</button>
    <ul>
      <li v-for="p in players" :key="p.id">{{ p.name }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../axios";

const players = ref([]);

async function fetchPlayers() {
  const res = await api.get("/players/");
  players.value = res.data;
}
</script>
