<script>
import SectionModifyComponent from "../components/SectionModifyComponent.vue";
import BookModifyComponent from "../components/BookModifyComponent.vue";
import axios from "axios";
export default {
  props: {
    id: String,
  },
  data() {
    return {
      nick_name: "",
      book: {},
      section: {},
      show_book: true,
    };
  },
  components: {
    BookModifyComponent,
    SectionModifyComponent,
  },
  methods: {
    logout() {
      localStorage.clear();
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios.get(`http://127.0.0.1:5000/logout`, {
        headers: headers,
      });
      this.$router.push("/librarian/login");
    },
    goHome() {
      this.$router.push("/librarian");
    },
  },
  mounted() {
    let headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/librarian/login");
      return;
    }
    if (this.$route.name === "modifyBook") {
      axios
        .get(`http://127.0.0.1:5000/librarian/book/${this.id}`, {
          headers: headers,
        })
        .then((data) => {
          this.book = data.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    } else {
      this.show_book = false;
      axios
        .get(`http://127.0.0.1:5000/librarian/section/${this.id}`, {
          headers: headers,
        })
        .then((data) => {
          this.section = data.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    }
    this.nick_name = localStorage.getItem("nick_name");
  },
};
</script>
<template>
  <div>
    <div class="row header">
      <div class="col-lg">
        <h1>Libra</h1>
        <h3>Welcome, {{ nick_name }}</h3>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="goHome">Home</label>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="logout">Logout</label>
      </div>
    </div>
  </div>
  <div v-if="show_book">
    <BookModifyComponent :book="book"></BookModifyComponent>
  </div>
  <div v-else>
    <SectionModifyComponent :section="section"></SectionModifyComponent>
  </div>
</template>
