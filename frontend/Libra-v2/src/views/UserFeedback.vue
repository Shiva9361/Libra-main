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
