import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import Login from "./views/Login.vue";
import Players from "./views/Players.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/players", component: Players },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount("#app");
