<template>
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

  <div class="read_book">
    <h3>{{ book.name }}</h3>
    <br />
    <div v-if="url != ''" class="bookembed">
      <iframe
        class="book_embed"
        :src="'http://127.0.0.1:5000' + url + '#toolbar=0'"
        type="application/pdf"
        height="100%"
        width="100%"
      />
    </div>
    <div v-else>{{ book.content }}</div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      book: {},
      url: "",
    };
  },
  props: {
    id: String,
    nick_name: String,
  },
  methods: {
    logout() {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/user/logout`, {
          headers: headers,
        })
        .then(() => {
          localStorage.clear();
          this.$router.push("/user/login");
        })
        .catch((err) => {
          localStorage.clear();
        });
    },
    goHome() {
      this.$router.push("/user");
    },
  },
  mounted() {
    let headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
      return;
    }
    axios
      .get(`http://127.0.0.1:5000/user/readbook/${this.id}`, {
        headers: headers,
      })
      .then((data) => {
        this.book = data.data.book;
        this.url = data.data.url;
      })
      .catch((err) => {
        if (err.response.data.invalid) {
          this.$router.push("/user/login");
          return;
        }
        if (err.response.status === 403) {
          if (window.confirm("You Don't Have Permisson to read ")) {
            this.$router.push("/user");
            return;
          }
        } else if (err.response.status === 404) {
          if (window.confirm("Book does not exist")) {
            this.$router.push("/user");
            return;
          }
        }
        console.log(err);
      });
  },
};
</script>
