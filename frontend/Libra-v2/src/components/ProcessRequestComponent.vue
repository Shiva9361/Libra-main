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
  <div class="requests">
    <div v-if="requests">
      <h3>Book Requests</h3>
      <div v-for="request in requests" class="request">
        User ID: {{ request.user_id }} <br />
        Book ID: {{ request.book_id }} <br />
        <label @click="accept(request.id)" class="btn btn-primary" role="button"
          >Accept</label
        >
        <label @click="reject(request.id)" class="btn btn-primary" role="button"
          >Reject</label
        >
      </div>
    </div>
    <div v-else><h3>No Pending Requests</h3></div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      requests: Object,
      nick_name: String,
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
    accept(request_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/librarian/processrequest/${request_id}/0`, {
          headers: headers,
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        })
        .then(() => window.location.reload());
    },
    reject(request_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/librarian/processrequest/${request_id}/1`, {
          headers: headers,
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        })
        .then(() => window.location.reload());
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
      .get("http://127.0.0.1:5000/librarian/requests", {
        headers: headers,
      })
      .then((data) => {
        this.requests = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.invalid) {
          this.$router.push("/librarian/login");
          return;
        }
      });
    this.nick_name = localStorage.getItem("nick_name");
  },
};
</script>
