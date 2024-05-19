<script>
import axios from "axios";
export default {
  name: "BookComponent",
  props: {
    books: Object,
    email: String,
  },
  methods: {
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
        .catch((err) => {
          console.log(err);
        });
      // Reload
      this.$router.push("/user");
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
        });
    },
  },
};
</script>

<template>
  <div class="books">
    <div class="book" v-for="book in books">
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
      <label class="btn btn-primary" role="button" v-show="email === book.email"
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
    </div>
  </div>
</template>
<style scoped>
.btn-primary {
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>
