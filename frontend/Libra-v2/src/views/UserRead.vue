<script>
import ReadBookComponent from "../components/ReadBookComponent.vue";
export default {
  props: {
    id: String,
  },
  data() {
    return {
      nick_name: "",
    };
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
  components: {
    ReadBookComponent,
  },
  mounted() {
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
    }
    this.nick_name = localStorage.getItem("nick_name");
  },
};
</script>
<template>
  <ReadBookComponent :id="id" :nick_name="nick_name"> </ReadBookComponent>
</template>
