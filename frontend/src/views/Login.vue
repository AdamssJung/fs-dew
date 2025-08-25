<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";

const username = ref("");
const password = ref("");
const error = ref("");

async function login() {
  try {
    const res = await axios.post("http://127.0.0.1:8000/token", {
      username: username.value,
      password: password.value,
    }, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });

    localStorage.setItem("token", res.data.access_token);
    error.value = "";
    alert("Login Success!");
  } catch (err) {
    error.value = "Login failed";
  }
}
</script>
