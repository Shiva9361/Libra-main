<script>
import LibrarainHome from "../components/LibrarianHome.vue";

export default {
  data() {
    return {
      nick_name: "",
      email: "",
      socket: "",
      headers: Object,
    };
  },
  components: {
    LibrarainHome,
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/librarian/login");
    },
  },
  mounted() {
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/librarian/login");
    }
    this.nick_name = localStorage.getItem("nick_name");
  },
};
</script>

<template>
  <LibrarainHome :nick_name="nick_name"></LibrarainHome>
</template>
