<script>
import LibrarainHome from "../components/LibrarianHome.vue";
import io from "socket.io-client";

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

    this.socket = io("http://127.0.0.1:5000");
    this.socket.on("connect", () => {
      console.log("con");
    });
    this.socket.on("csv_generated", () => {
      alert("csv file generated");
    });
  },
};
</script>

<template>
  <LibrarainHome :nick_name="nick_name"></LibrarainHome>
</template>
