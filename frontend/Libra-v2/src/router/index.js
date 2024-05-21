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
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/UserLogin.vue"),
    },
    {
      path: "/user",
      name: "user",
      component: () => import("../views/UserView.vue"),
    },
    {
      path: "/user/read/:id",
      name: "userRead",
      component: () => import("../views/UserRead.vue"),
      props: true,
    },
    {
      path: "/user/feedback/:id/:book_name",
      name: "userFeedback",
      component: () => import("../views/UserFeedback.vue"),
      props: true,
    },
  ],
});

export default router;
