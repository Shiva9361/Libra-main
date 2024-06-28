<script>
import axios from "axios";
export default {
  props: {
    nick_name: String,
  },
  data() {
    return {
      users: {},
      stats: {},
    };
  },
  methods: {
    logout() {
      localStorage.clear();
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
    axios
      .get("http://127.0.0.1:5000/librarian/getactiveusers", {
        headers: headers,
      })
      .then((data) => {
        this.users = data.data;
      })
      .catch((err) => {
        if (err.response.data.invalid) {
          this.$router.push("/librarian/login");
          return;
        }
      });
    axios
      .get("http://127.0.0.1:5000/librarian/getstats", {
        headers: headers,
      })
      .then((data) => {
        this.stats = data.data;
      })
      .catch((err) => {
        if (err.response.data.invalid) {
          this.$router.push("/librarian/login");
          return;
        }
      });
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
  <h3>Number of Requests: {{ stats.requests }}</h3>
  <h3>Number of Accepted Requests: {{ stats.arequests }}</h3>
  <h3>Number of Rejected Requests: {{ stats.rrequests }}</h3>
  <h3>Number of Books:{{ stats.books }}</h3>
  <h3>Number of Sections:{{ stats.sections }}</h3>
  <h3>Online users: {{ users.length }}</h3>
  <div class="all_users">
    <div v-for="user in users">
      <div class="user">
        Nick_Name: {{ user.nick_name }}<br />
        Email: {{ user.email }}
      </div>
    </div>
  </div>
</template>
