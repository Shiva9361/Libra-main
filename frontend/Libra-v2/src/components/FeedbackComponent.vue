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
  <h3>Feedback Form</h3>
  <form @submit.prevent="submitFeedback">
    <div class="feedback_form">
      <div>
        <label class="form-label"
          >Book Name
          <input
            class="form-control"
            type="text"
            id="bookname"
            :value="book_name"
            readonly
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Rating(1-10)
          <input
            class="form-control"
            type="range"
            id="rating"
            min="1"
            max="10"
            required
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Feedback
          <textarea
            class="form-control"
            id="feedback"
            required
            rows="5"
            cols="100"
          ></textarea>
        </label>
      </div>
      <div>
        <input class="btn btn-primary" type="submit" value="Submit" />
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  props: {
    nick_name: String,
    id: String,
    book_name: String,
  },
  methods: {
    goHome() {
      this.$router.push("/user");
    },
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
    submitFeedback() {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      let data = {
        rating: document.getElementById("rating").value,
        feedback: document.getElementById("feedback").value,
      };
      axios
        .post(`http://127.0.0.1:5000/user/feedback/${this.id}`, data, {
          headers: headers,
        })
        .catch((err) => {
          if (err.response.status === 401) {
            window.confirm("Already gave feedback");
            this.$router.push("/user");
            return;
          }
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
          console.log(err);
        })
        .then((res) => {
          console.log(res);
          if (res.status == 201) {
            window.confirm("Feedback Given");
          }
        })
        .then(() => {
          this.$router.push("/user");
        });
    },
  },
  mounted() {
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
      return;
    }
  },
};
</script>
