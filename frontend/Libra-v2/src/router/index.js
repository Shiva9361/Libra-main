import { createRouter, createWebHistory } from "vue-router";
import RootLogin from "../views/RootLogin.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "rootLogin",
      component: RootLogin,
    },
    {
      path: "/user/login",
      name: "userLogin",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/UserLogin.vue"),
    },
  ],
});

export default router;
