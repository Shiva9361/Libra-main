<template>
  <div v-for="section in sections">
    <div v-if="section.id != 0">
      <div class="section">
        <h5>
          <div class="rmbuttons">
            <label
              @click="remove(section.id)"
              class="btn btn-primary"
              role="button"
              >Remove</label
            >
            <label
              @click="modify(section.id)"
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
import axios from "axios";
import BookComponent from "./LibrarianBookComponent.vue";
export default {
  props: {
    sections: Object,
  },
  components: {
    BookComponent,
  },
  methods: {
    modify(section_id) {
      this.$router.push(`/librarian/modify/section/${section_id}`);
    },
    remove(section_id) {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/librarian/remove/section/${section_id}`, {
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
.rmbuttons {
  margin: 10px;
  padding-left: 10px;
  float: inline-end;
}
</style>
