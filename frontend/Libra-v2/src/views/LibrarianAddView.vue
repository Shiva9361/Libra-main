<script>
import AddSectionBookComponent from "../components/AddSectionBookComponent.vue";

export default {
  data() {
    return {
      nick_name: "",
      email: "",
      headers: Object,
    };
  },
  components: {
    AddSectionBookComponent,
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
  <AddSectionBookComponent></AddSectionBookComponent>
</template>
