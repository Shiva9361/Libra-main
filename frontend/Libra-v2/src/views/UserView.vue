<script>
import UserHome from "../components/UserHome.vue";

export default {
  data() {
    return {
      nick_name: "",
      email: "",
      headers: Object,
    };
  },
  components: {
    UserHome,
  },
  methods: {
    logout(event) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }

      fetch(`http://127.0.0.1:5000/user/logout`, {
        method: "GET",
        headers: headers,
      });
      localStorage.clear();
    },
  },
  mounted() {
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
    }
    this.nick_name = localStorage.getItem("nick_name");
    this.email = localStorage.getItem("email");
    // To update nick_name after changes in profile

    window.addEventListener("nick_name_changed", (event) => {
      this.nick_name = event.detail.storage;
    });
  },
};
</script>

<template>
  <UserHome :email="email" :nick_name="nick_name"></UserHome>
</template>
