<template>
  <div id="app">
    <!-- 간단한 네비게이션 -->
    <nav>
      <router-link to="/">Login</router-link> |
      <router-link to="/players">Players</router-link>
    </nav>

    <!-- 여기서 라우터가 현재 경로에 맞는 컴포넌트를 보여줍니다 -->
    <router-view />
  </div>
</template>

<script setup>
// Vue 3 <script setup> 문법, 특별히 로직 필요 없음
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 20px;
}

nav {
  margin-bottom: 20px;
}
</style>
