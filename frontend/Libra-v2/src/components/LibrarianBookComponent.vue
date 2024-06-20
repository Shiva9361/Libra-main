<template>
  <div class="book">
    Name: {{ book.name }} <br />
    Author: {{ book.authors }} <br />
    Book Id: {{ book.id }} <br />
    <div v-if="book.email">
      With: {{ book.email }} <br />
      Return Date:{{ book.return_date }}
    </div>
    <br />
    <label @click="remove(book.id)" class="btn btn-primary" role="button"
      >Remove</label
    >
    <label @click="modify(book.id)" class="btn btn-primary" role="button"
      >Modify</label
    >
    <div v-if="book.email">
      <label @click="revoke(book.id)" class="btn btn-primary" role="button"
        >Revoke</label
      >
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  props: {
    book: Object,
  },
  methods: {
    remove(book_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/librarian/remove/book/${book_id}`, {
          headers: headers,
        })
        .then(() => {
          window.location.reload();
          return;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
    modify(book_id) {
      this.$router.push(`/librarian/modify/book/${book_id}`);
      return;
    },
    revoke(book_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/librarian/revoke/book/${book_id}`, {
          headers: headers,
        })
        .then(() => {
          window.location.reload();
          return;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
  },
  mounted() {
    if (this.book.return_date != null) {
      this.book.return_date = this.book.return_date
        .split(" ")
        .slice(1, 4)
        .join(" ");
    }
  },
};
</script>
