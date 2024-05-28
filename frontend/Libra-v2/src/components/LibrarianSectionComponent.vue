<template>
  <div v-for="section in sections">
    <div v-if="section.id != 0">
      <div class="section">
        <h5>
          <div class="rmbuttons">
            <label
              @click="remove(section.section_id)"
              class="btn btn-primary"
              role="button"
              >Remove</label
            >
            <label
              @click="modify(section.section_id)"
              class="btn btn-primary"
              role="button"
              >Modify</label
            >
          </div>
          Section Name : {{ section.name }}<br />
          Description : {{ section.description }}
        </h5>
        <div class="col-2" v-for="book in section.books">
          <BookComponent :book="book"></BookComponent>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import BookComponent from "./LibrarianBookComponent.vue";
export default {
  props: {
    sections: Object,
  },
  components: {
    BookComponent,
  },
};
</script>
<style scoped>
.section {
  overflow-y: hidden;
  border-style: solid;
  border-radius: 25px;
  padding: 10px;
  margin: 10px;
}
</style>
