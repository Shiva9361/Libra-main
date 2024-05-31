<template>
  <div>
    <div class="row header">
      <div class="col-9">
        <h1>Libra</h1>
        <h3>Welcome, {{ nick_name }}</h3>
      </div>
      <div class="col-1">
        <br />
        <label class="btn btn-info" role="button" @click="addBookSection"
          >Add B/S</label
        >
      </div>
      <div class="col-1">
        <br />
        <label class="btn btn-info" role="button" @click="goHome">Home</label>
      </div>
      <div class="col-1">
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
          >Content
          <input class="form-control" type="text" id="content1" required />
        </label>
      </div>
      <div>
        <label class="form-label"
          >File
          <input class="form-control" type="file" id="content" />
        </label>
      </div>
      <div>
        <input class="btn btn-primary" type="submit" value="Submit" />
      </div>
    </form>
  </div>

  <div class="add_section">
    <h3>Add Section</h3>
    <form class="mt5" @submit.prevent="addSection" id="librarian_add_section">
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
        if (err.response.data.authenticated === false) {
          this.$router.push("/librarian/login");
          return;
        }
      });
  },
};
</script>
<style scoped>
.add_books {
  overflow-y: auto;
  height: 450px;
  background-color: #f8f8eb;
  border-style: solid;
  border-radius: 25px;
  padding: 10px;
  margin-bottom: 10px;
}
.add_section {
  overflow-y: auto;
  height: 300px;
  background-color: #f8f8eb;
  border-style: solid;
  border-radius: 25px;
  padding: 10px;
}
</style>
