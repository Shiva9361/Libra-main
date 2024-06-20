<script>
import BookComponent from "./UserBookComponent.vue";
export default {
  props: {
    books: Object,
    email: String,
  },
  methods: {},
  components: {
    BookComponent,
  },
};
</script>

<template>
  <div class="books">
    <div class="book col-2" v-for="book in books">
      <BookComponent :book="book" :email="email"> </BookComponent>
    </div>
  </div>
</template>
