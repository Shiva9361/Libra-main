<template>
  <div class="all_sections">
    <div v-for="section in sections">
      <div v-if="section.id != 0">
        <div class="section">
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
import BookComponent from "./BookComponent.vue";

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
<style>
.section {
  overflow-y: hidden;
  border-radius: 20px;
  border-style: solid;
  padding-left: 10px;
  padding-right: 10px;
  vertical-align: top;
  margin-top: 5px;
}
.all_sections {
  overflow-y: auto;
  height: 370px;
  background-color: #f8f8eb;
  border-style: solid;
  border-radius: 25px;
  padding: 5px;
}
</style>
