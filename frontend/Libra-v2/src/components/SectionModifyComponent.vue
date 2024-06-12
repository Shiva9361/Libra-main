<template>
  <div class="form">
    <form
      class="mt5 modify"
      @submit.prevent="modify"
      id="librariab_modify_section"
    >
      <div>
        <label class="form-label"
          >Section ID:
          <input
            class="form-control"
            type="text"
            id="id"
            :value="section.id"
            readonly
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Section Name:
          <input
            class="form-control"
            type="text"
            id="name"
            :value="section.name"
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Description :
          <textarea
            class="form-control"
            id="description"
            required
            rows="5"
            cols="100"
            >{{ section.description }}</textarea
          >
        </label>
      </div>
      <div>
        <input class="btn btn-primary" type="submit" value="Submit" />
      </div>
    </form>
  </div>
</template>
<script>
import axios from "axios";
export default {
  props: {
    section: Object,
  },
  methods: {
    modify() {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let data = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
      };
      axios
        .post(
          `http://127.0.0.1:5000/librarian/modify/section/${this.section.id}`,
          data,
          {
            headers: headers,
          }
        )
        .then(() => {
          this.$router.push("/librarian");
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
};
</script>
