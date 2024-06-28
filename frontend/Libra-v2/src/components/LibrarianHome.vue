<template>
  <div>
    <div class="row header">
      <div class="col-lg">
        <h1>Libra</h1>
        <h3>Welcome, {{ nick_name }}</h3>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="generateCSV"
          >Report</label
        >
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="showOnlineUsers"
          >Stats</label
        >
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="addBookSection"
          >Add
        </label>
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="processRequest"
          >Requests</label
        >
      </div>
      <div class="col-auto">
        <br />
        <label class="btn btn-info" role="button" @click="logout">Logout</label>
      </div>
    </div>
  </div>

  <div class="book_header">
    <div class="row">
      <div class="col-auto">
        <h3>All Books</h3>
      </div>
      <div class="col-auto">
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
            <input
              class="btn btn-primary btn-search"
              type="submit"
              value="🔍"
            />
          </span>
        </form>
      </div>
    </div>
  </div>
  <div class="tophalf">
    <div class="all_books_librarian">
      <div v-for="book in books">
        <LibrarianBookComponent :book="book"></LibrarianBookComponent>
      </div>
    </div>
    <div class="chart">
      <Pie :data="pie_chart_data" :options="pie_chart_options" />
    </div>
  </div>
  <div class="row sec">
    <div class="col-auto">
      <h3>All Sections</h3>
    </div>
    <div class="col-auto">
      <form @submit.prevent="searchSections">
        <span class="inline">
          <input
            class="form-label"
            type="search"
            placeholder="search"
            id="keyforsearchsection"
          />
          <input class="btn btn-primary btn-search" type="submit" value="🔍" />
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
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "vue-chartjs";

ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  data() {
    return {
      books: {},
      sections: {},
      pie_data: [],
    };
  },
  computed: {
    pie_chart_data() {
      return {
        labels: ["With User", "Free"],
        datasets: [
          {
            backgroundColor: ["#41B883", "#E46651"],
            data: this.pie_data,
          },
        ],
      };
    },
    pie_chart_options() {
      return {
        responsive: true,
        maintainAspectRatio: false,
      };
    },
  },
  props: {
    nick_name: String,
  },
  components: {
    LibrarianSectionComponent,
    LibrarianBookComponent,
    Pie,
  },
  methods: {
    generateCSV() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/librarian/login");
        return;
      }
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };

      axios
        .get("http://127.0.0.1:5000/librarian/generate_report", {
          headers: headers,
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.invalid) {
            this.$router.push("/librarian/login");
            return;
          }
        })
        .then(() => {
          alert("Request Sent");
        });
    },
    showOnlineUsers() {
      this.$router.push("/librarian/users");
    },
    addBookSection() {
      this.$router.push("/librarian/add");
    },
    processRequest() {
      this.$router.push("/librarian/process");
    },
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
          if (err.response.data.invalid) {
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
      .get("http://127.0.0.1:5000/librarian/books", {
        headers: headers,
      })
      .then((data) => {
        this.books = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.invalid) {
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
        if (err.response.data.invalid) {
          this.$router.push("/librarian/login");
          return;
        }
      });
    axios
      .get("http://127.0.0.1:5000/librarian/graph/books", {
        headers: headers,
      })
      .then((data) => {
        this.pie_data = data.data.chart_data;
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
