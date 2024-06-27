<template>
  <div class="form">
    <form
      class="mt5"
      @submit.prevent="modify"
      id="librarian_modify_book"
      enctype="multipart/form-data"
      ref="bookform"
    >
      <div>
        <label class="form-label"
          >Book Name
          <input
            class="form-control"
            type="text"
            id="bookname"
            :value="book.name"
            required
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Authors
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
          <textarea class="form-control" id="content1" rows="5" cols="100">{{
            book.content
          }}</textarea>
        </label>
      </div>
      <div>
        <label class="form-label">
          Overwrite file?
          <input type="radio" id="overwrite" value="" />
        </label>
      </div>
      <div>
        <label class="form-label"
          >File (Will overide content)
          <input class="form-control" type="file" id="content" ref="bookfile" />
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
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let data = {
        name: document.getElementById("bookname").value,
        authors: document.getElementById("authors").value,
        section_id: document.getElementById("section_id").value,
        content1: document.getElementById("content1").value,
        overwrite: document.getElementById("overwrite").checked,
      };
      const formdata = new FormData();
      formdata.append("name", data.name);
      formdata.append("authors", data.authors);
      formdata.append("section_id", data.section_id);
      formdata.append("content1", data.content1);
      formdata.append("overwrite", data.overwrite);
      if (this.$refs.bookfile.files[0] != undefined) {
        formdata.append("content", this.$refs.bookfile.files[0]);
      } else {
        if (data.content1 == "") {
          alert("Both pdf and content can't be empty");
          return;
        }
      }
      axios
        .post(
          `http://127.0.0.1:5000/librarian/modify/book/${this.book.id}`,
          formdata,
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
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.invalid) {
          this.$router.push("/librarian/login");
          return;
        }
      });
  },
};
</script>
