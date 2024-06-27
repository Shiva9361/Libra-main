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
      // lazy-loaded when the route is visited.
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
    {
      path: "/user/feedbacks/:id/:book_name",
      name: "feedbacks",
      component: () => import("../views/FeedbackView.vue"),
      props: true,
    },
    {
      path: "/user/register",
      name: "register",
      component: () => import("../views/RegisterUserView.vue"),
    },
    {
      path: "/librarian/login",
      name: "librarianlogin",
      component: () => import("../views/LibrarianLogin.vue"),
    },
    {
      path: "/librarian",
      name: "librarian",
      component: () => import("../views/LibrarianView.vue"),
    },
    {
      path: "/librarian/modify/book/:id",
      name: "modifyBook",
      component: () => import("../views/LibrarianModifyView.vue"),
      props: true,
    },
    {
      path: "/librarian/modify/section/:id",
      name: "modifySection",
      component: () => import("../views/LibrarianModifyView.vue"),
      props: true,
    },
    {
      path: "/librarian/process",
      name: "processRequest",
      component: () => import("../views/LibrarianProcessView.vue"),
    },
    {
      path: "/librarian/add",
      name: "addBookSection",
      component: () => import("../views/LibrarianAddView.vue"),
    },
    {
      path: "/librarian/users",
      name: "showOnlineUsers",
      component: () => import("../views/LibrarianUsersView.vue"),
    },
    {
      path: "/user/pay/:id/:book_name",
      name: "paymentPortal",
      component: () => import("../views/PaymentView.vue"),
      props: true,
    },
  ],
});

export default router;
