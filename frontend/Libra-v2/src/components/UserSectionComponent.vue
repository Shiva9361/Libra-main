<template>
  <div class="all_sections_users">
    <div v-for="section in sections">
      <div v-if="section.id != 0">
        <div class="section_user">
          <h5>
            Section Name : {{ section.name }}<br />
            Description : {{ section.description }}
          </h5>
          <div class="book col-2" v-for="book in section.books">
            <BookComponent :book="book" :email="email"></BookComponent>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BookComponent from "./UserBookComponent.vue";

export default {
  props: {
    sections: Object,
    email: String,
  },
  components: {
    BookComponent,
  },
};
</script>
