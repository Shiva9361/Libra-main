<template>
  <div>
    <div class="row header">
      <div class="col-10">
        <h1>Libra</h1>
        <h3>Welcome, {{ nick_name }}</h3>
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

  <div class="book_header">
    <h3 class="col-6">Available Books</h3>
    <div class="col-2">
      <form @submit.prevent="searchBooks">
        <span class="inline">
          <input
            class="form-label"
            type="search"
            placeholder="search"
            id="keyforbooksearch"
          />
          <select class="form-label" required id="indexforbooksearch">
            <option value="1">Name</option>
            <option value="2">Author</option>
            <option value="3">With</option>
          </select>
          <input class="btn btn-primary" type="submit" value="🔍" />
        </span>
      </form>
    </div>
  </div>
  <div class="tophalf">
    <div class="all_books">
      <div v-for="book in books">
        <LibrarianBookComponent :book="book"></LibrarianBookComponent>
      </div>
    </div>
    <div class="chart">
      <img
        src="http://127.0.0.1:5000/static/chart.png"
        width="500"
        height="370"
        alt="Pie chart"
      />
    </div>
  </div>
  <div class="row sec">
    <div class="col-9">
      <h3>All Sections</h3>
    </div>
    <div class="col-2">
      <form @submit.prevent="searchSections">
        <span class="inline">
          <input
            class="form-label"
            type="search"
            placeholder="search"
            id="keyforsearchsection"
          />
          <input class="btn btn-primary" type="submit" value="🔍" />
        </span>
      </form>
    </div>
  </div>

  <div class="all_sections">
    <LibrarianSectionComponent :sections="sections"></LibrarianSectionComponent>
  </div>
</template>

<script>
import axios from "axios";
import LibrarianSectionComponent from "./LibrarianSectionComponent.vue";
import LibrarianBookComponent from "./LibrarianBookComponent.vue";
export default {
  data() {
    return {
      books: {},
      sections: {},
    };
  },
  props: {
    nick_name: String,
  },
  components: {
    LibrarianSectionComponent,
    LibrarianBookComponent,
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/librarian/login");
    },
    searchBooks() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      let data = {
        key: document.getElementById("keyforbooksearch").value,
        index: document.getElementById("indexforbooksearch").value,
      };
      axios
        .post("http://127.0.0.1:5000/librarian/search/books", data, {
          headers: headers,
        })
        .then((data) => {
          this.books = data.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.authenticated === false) {
            this.$router.push("/librarian/login");
            return;
          }
        });
    },
    searchSections() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      let data = {
        key: document.getElementById("keyforsearchsection").value,
      };
      axios
        .post("http://127.0.0.1:5000/librarian/search/sections", data, {
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
      .get("http://127.0.0.1:5000/librarian/books", {
        headers: headers,
      })
      .then((data) => {
        this.books = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.authenticated === false) {
          this.$router.push("/librarian/login");
          return;
        }
      });
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
    axios
      .get("http://127.0.0.1:5000/librarian/graph/books", {
        headers: headers,
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
.sec {
  padding-top: 10px;
}
.tophalf {
  display: flex;
}
.chart {
  float: inline-end;
  border-style: solid;
  border-radius: 25px;
  margin-left: 10px;
}
.all_books {
  overflow-y: auto;
  height: 370px;
  width: 70%;
  padding-left: 10px;
  padding-right: 10px;
  border-style: solid;
  border-radius: 25px;
  background-color: #f8f8eb;
}

.section {
  overflow-y: hidden;
  border-style: solid;
  border-radius: 25px;
  padding: 10px;
  margin: 10px;
}

.all_sections {
  border-style: solid;
  border-radius: 25px;
  overflow-y: auto;
  height: 350px;
  background-color: #f8f8eb;
}
.book_header {
  display: flex;
  flex-direction: row;
  padding-top: 10px;
}
.inline {
  display: inline-flex;
  gap: 10px;
}
</style>
