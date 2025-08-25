<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../axios";

const username = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

async function login() {
  error.value = "";
  try {
    // ✅ 반드시 URLSearchParams 로 폼-인코딩
    const form = new URLSearchParams();
    form.append("username", username.value);
    form.append("password", password.value);

    const res = await api.post("/token", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const accessToken = res.data?.access_token;
    if (!accessToken) throw new Error("No access_token in response");

    localStorage.setItem("token", accessToken);

    // 로그인 성공 후 페이지 이동
    router.push("/players");
  } catch (e) {
    // 서버가 주는 메시지 노출(가능하면)
    const msg = e?.response?.data?.detail || e.message || "Login failed";
    error.value = msg;
  }
}
</script>
