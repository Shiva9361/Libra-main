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
export default {
  props: {
    book: Object,
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
