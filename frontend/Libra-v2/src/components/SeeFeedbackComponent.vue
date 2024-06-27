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
  <div class="feedbacks">
    <h3>Feedback for {{ book_name }}:</h3>
    <div v-if="feedbacks">
      <div v-for="feedback in feedbacks">
        <div class="feedback">
          <h4>By: {{ feedback.user_name }}</h4>
          <h5>
            Rating: {{ feedback.rating }} <br />
            Feedback: {{ feedback.feedback }}
          </h5>
        </div>
      </div>
    </div>
    <h4 v-else>No feedback Available</h4>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      feedbacks: {},
    };
  },
  props: {
    id: String,
    nick_name: String,
    book_name: String,
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
      .get(`http://127.0.0.1:5000/user/checkfeedback/${this.id}`, {
        headers: headers,
      })
      .then((data) => {
        this.feedbacks = data.data;
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
