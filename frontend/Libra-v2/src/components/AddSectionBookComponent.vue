<template>
  <div>
    <div class="row header">
      <div class="col-lg">
        <h1>Libra</h1>
        <h3>Welcome, {{ nick_name }}</h3>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="goHome">Home</label>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="logout">Logout</label>
      </div>
    </div>
  </div>
  <div class="add_books">
    <h3>Add Book</h3>
    <form
      class="mt5"
      @submit.prevent="addBook"
      id="librarian_add_book"
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
            value=""
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
            value=""
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
              v-model="defaultSectionid"
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
            id="content1"
            rows="5"
            cols="100"
          ></textarea>
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

  <div class="add_section">
    <h3>Add Section</h3>
    <form
      class="mt5"
      @submit.prevent="addSection"
      id="librarian_add_section"
      ref="sectionform"
    >
      <div>
        <label class="form-label"
          >Section Name
          <input
            class="form-control"
            type="text"
            id="sectionname"
            value=""
            required
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Description
          <input
            class="form-control"
            type="text"
            id="description"
            value=""
            required
          />
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
      nick_name: "",
      defaultSectionid: 0,
      sections: {},
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/librarian/login");
    },
    goHome() {
      this.$router.push("/librarian");
    },
    addSection() {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let data = {
        name: document.getElementById("sectionname").value,
        description: document.getElementById("description").value,
      };
      axios
        .post("http://127.0.0.1:5000/librarian/add/section", data, {
          headers: headers,
        })
        .then((data) => {
          this.$refs.sectionform.reset();
          alert("Section Added");
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
    addBook() {
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
      };
      const formdata = new FormData();
      formdata.append("name", data.name);
      formdata.append("authors", data.authors);
      formdata.append("section_id", data.section_id);
      formdata.append("content1", data.content1);
      if (this.$refs.bookfile.files[0] != undefined) {
        formdata.append("content", this.$refs.bookfile.files[0]);
      } else {
        if (data.content1 == "") {
          alert("Both pdf and content can't be empty");
          return;
        }
      }

      axios
        .post("http://127.0.0.1:5000/librarian/add/book", formdata, {
          headers: headers,
        })
        .then((data) => {
          alert("Book Added");
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
    this.nick_name = localStorage.getItem("nick_name");
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
