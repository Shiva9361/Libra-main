<script>
import OnlineUserComponent from "../components/OnlineUserComponent.vue";

export default {
  data() {
    return {
      nick_name: "",
      email: "",
      headers: Object,
    };
  },
  components: {
    OnlineUserComponent,
  },
  methods: {},
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
  <OnlineUserComponent :nick_name="nick_name"></OnlineUserComponent>
</template>
