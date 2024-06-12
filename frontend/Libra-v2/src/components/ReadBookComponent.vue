<template>
  <div class="row header">
    <div class="col-10">
      <h1>Libra</h1>
      <h3>Welcome, {{ nick_name }}</h3>
    </div>
    <div class="col-1">
      <br />
      <label class="btn btn-info" role="button" @click="goHome">Home</label>
    </div>
    <div class="col-1">
      <br />
      <label class="btn btn-info" role="button" @click="logout">Logout</label>
    </div>
  </div>

  <div class="read_book">
    <h3>{{ book.name }}</h3>
    <div v-if="url != ''">
      <embed
        :src="'http://127.0.0.1:5000' + url"
        type="application/pdf"
        height="800px"
        width="1300px"
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
      localStorage.clear();
      this.$router.push("/user/login");
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
<style scoped>
embed {
  display: flex;
  margin-left: 280px;
}
.content {
  display: flex;
  width: 100%;
  margin: 10px;
  flex-direction: column;
  background-color: floralwhite;
}
</style>
