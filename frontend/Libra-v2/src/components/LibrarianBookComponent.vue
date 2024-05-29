<template>
  <div class="book">
    Name: {{ book.name }} <br />
    Author: {{ book.authors }} <br />
    Book Id: {{ book.id }} <br />
    <div v-if="book.user_email">
      With: {{ book.user_email }} <br />Return Date:{{ book.return_date }}
    </div>
    <br />
    <label @click="remove(book.id)" class="btn btn-primary" role="button"
      >Remove</label
    >
    <label @click="modify(book.id)" class="btn btn-primary" role="button"
      >Modify</label
    >
    <div v-if="book.user_email">
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
          if (err.response.data.authenticated === false) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
    modify(book_id) {
      this.$router.push(`/librarian/modify/book/${book_id}`);
      return;
    },
  },
};
</script>
<style>
.book {
  float: left;
  margin-right: 30px;
  margin: 10px;
  padding: 10px;
  border-style: solid;
  border-color: dimgrey;
  border-radius: 25px;
  background-color: #f4f5de;
}
</style>
