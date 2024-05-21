<script>
import axios from "axios";
export default {
  props: {
    book: Object,
    email: String,
  },
  methods: {
    feedback(book_id, book_name) {
      this.$router.push(`/user/feedback/${book_id}/${book_name}`);
    },
    markBook(book_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/bookread/${book_id}`, {
          headers: headers,
        })
        .then((data) => {
          if (data.data.message == "done") {
            alert("Marked as Read");
          }
        })
        .catch((err) => {
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
          alert("Already Marked as Read");
          console.log(err);
        });
      // Reload
    },
    requestBook(book_id) {
      this.headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/requestbook/${book_id}`, {
          headers: this.headers,
        })
        .then((data) => {
          if (data.data.message === "Already Requested") {
            alert("You have already Requested this Book");
          } else if (data.data.message === "Requested") {
            alert("Your request will be processed soon");
          }
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
        });
    },
    returnBook(book_id) {
      this.headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/returnbook/${book_id}`, {
          headers: this.headers,
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
        })
        .then(() => {
          window.location.reload();
        });
    },
    readBook(book_id) {
      this.$router.push(`/user/read/${book_id}`);
    },
  },
};
</script>
<template>
  Name: {{ book.name }} <br />
  Author: {{ book.authors }} <br />
  Rating: {{ book.rating }}<br />
  <label
    class="btn btn-primary"
    role="button"
    @click="requestBook(book.id)"
    v-show="email != book.email"
    >Request
  </label>
  <label
    class="btn btn-primary"
    role="button"
    @click="readBook(book.id)"
    v-show="email === book.email"
    >Read</label
  >
  <label
    class="btn btn-primary"
    role="button"
    @click="returnBook(book.id)"
    v-show="email === book.email"
    >Return</label
  ><br />
  <label
    class="btn btn-primary"
    role="button"
    v-show="email === book.email"
    @click="feedback(book.id, book.name)"
    >Feedback</label
  >
  <label
    class="btn btn-primary"
    role="button"
    @click="BuyBook(book.id)"
    v-show="email === book.email"
    >Buy</label
  >
  <label
    class="btn btn-primary"
    role="button"
    @click="markBook(book.id)"
    v-show="email === book.email"
    >Mark as Read</label
  >
</template>
