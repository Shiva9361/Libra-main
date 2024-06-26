<script>
import FeedbackComponent from "../components/FeedbackComponent.vue";
export default {
  props: {
    id: String,
    book_name: String,
  },
  data() {
    return {
      nick_name: "s",
    };
  },
  components: {
    FeedbackComponent,
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
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
    }
    this.nick_name = localStorage.getItem("nick_name");
  },
};
</script>
<template>
  <FeedbackComponent :id="id" :nick_name="nick_name" :book_name="book_name">
  </FeedbackComponent>
</template>
