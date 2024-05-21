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
