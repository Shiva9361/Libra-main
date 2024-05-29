<template>
  <div class="form">
    <form
      class="mt5 modify"
      @submit.prevent="modify"
      id="librariab_modify_book"
    >
      <div>
        <label class="form-label"
          >Book ID:
          <input
            class="form-control"
            type="text"
            id="id"
            :value="book.id"
            readonly
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Book Name:
          <input
            class="form-control"
            type="text"
            id="name"
            :value="book.name"
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Authors :
          <input
            class="form-control"
            type="text"
            id="authors"
            :value="book.authors"
            required
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Section Name
          <div>
            <select
              class="form-label"
              id="section_id"
              v-model="book.section_id"
            >
              <option v-for="section in sections" :value="section.id">
                {{ section.name }}
              </option>
            </select>
          </div>
        </label>
      </div>
      <div>
        <label class="form-label"
          >Content :
          <textarea
            class="form-control"
            id="content"
            required
            rows="5"
            cols="100"
            >{{ book.content }}</textarea
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
  data() {
    return {
      sections: {},
    };
  },
  props: {
    book: Object,
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
        content: document.getElementById("content").value,
        authors: document.getElementById("authors").value,
        section_id: document.getElementById("section_id").value,
      };
      axios
        .post(
          `http://127.0.0.1:5000/librarian/modify/book/${this.book.id}`,
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
          if (err.response.data.authenticated === false) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
  },
  mounted() {
    let headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/librarian/login");
      return;
    }
    axios
      .get("http://127.0.0.1:5000/librarian/sections", {
        headers: headers,
      })
      .then((data) => {
        this.sections = data.data;
        console.log(data);
        console.log(this.book.section_id);
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.authenticated === false) {
          this.$router.push("/user/login");
          return;
        }
      });
  },
};
</script>
