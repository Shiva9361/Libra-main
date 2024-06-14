<script>
import axios from "axios";
export default {
  props: {
    nick_name: String,
  },
  data() {
    return {
      users: {},
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
        console.log(this.users);
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
  </div>
  <h1>Online users: {{ users.length }}</h1>
  <div class="all_users">
    <div v-for="user in users">
      <div class="user">
        Nick_Name: {{ user.nick_name }}<br />
        Email: {{ user.email }}
      </div>
    </div>
  </div>
</template>

<style>
.all_users {
  overflow-y: auto;
  height: 80vh;
  padding-left: 10px;
  border-style: solid;
  border-radius: 25px;
  background-color: #f8f8eb;
}
.user {
  float: left;
  margin: 10px;
  margin-right: 40px;
  padding: 10px;
  border-style: solid;
  border-color: dimgrey;
  border-radius: 25px;
  background-color: #f4f5de;
}
</style>
