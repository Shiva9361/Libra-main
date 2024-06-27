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
    buyBook(book_id, book_name) {
      this.$router.push(`/user/pay/${book_id}/${book_name}`);
    },
    downloadBook(book_id, book_name) {
      let headers = {
        "Content-Type": "application/pdf",

        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/download/${book_id}`, {
          headers: headers,
          responseType: "blob",
        })
        .then((data) => {
          console.log(data);
          const blob = data.data;
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", `${book_name}.pdf`);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
          if (err.response.status === 404) {
            alert("Book does not exist");
          } else if (err.response.status === 403) {
            alert("Access Denied");
          }
        });
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
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
          alert("Already Marked as Read");
          console.log(err);
        });
      // Reload
    },
    requestBook(book_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/requestbook/${book_id}`, {
          headers: headers,
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
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
        });
    },
    returnBook(book_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/returnbook/${book_id}`, {
          headers: headers,
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
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
    seeFeedback(book_id, book_name) {
      this.$router.push(`/user/feedbacks/${book_id}/${book_name}`);
    },
  },
};
</script>
<template>
  Name: {{ book.name }} <br />
  Author: {{ book.authors }} <br />
  Rating: {{ book.rating }}<br />
  <label
    class="btn btn-primary btn-book"
    role="button"
    @click="requestBook(book.id)"
    v-show="email != book.email"
    >Request
  </label>
  <label
    class="btn btn-primary btn-book"
    role="button"
    @click="readBook(book.id)"
    v-show="email === book.email"
    >Read</label
  >
  <label
    class="btn btn-primary btn-book"
    role="button"
    @click="returnBook(book.id)"
    v-show="email === book.email"
    >Return</label
  >
  <label
    class="btn btn-primary btn-book"
    role="button"
    @click="downloadBook(book.id, book.name)"
    v-show="book.owner"
    >Download</label
  >
  <br />
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
    @click="seeFeedback(book.id, book.name)"
    v-show="email != book.email"
    >Feedbacks
  </label>
  <label
    class="btn btn-primary"
    role="button"
    @click="buyBook(book.id, book.name)"
    v-show="!book.owner"
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
