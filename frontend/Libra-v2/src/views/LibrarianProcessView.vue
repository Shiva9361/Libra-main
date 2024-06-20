<script>
import ProcessRequestComponent from "../components/ProcessRequestComponent.vue";

export default {
  data() {
    return {
      nick_name: "",
      email: "",
      headers: Object,
    };
  },
  components: {
    ProcessRequestComponent,
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
  <ProcessRequestComponent></ProcessRequestComponent>
</template>
