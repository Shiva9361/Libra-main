<script>
import axios from "axios";
import BooksComponent from "./BooksComponent.vue";
import ProfileComponent from "./ProfileComponent.vue";
import SectionComponent from "./SectionComponent.vue";
export default {
  data() {
    return {
      headers: {},
      all_books: {},
      ur_books: {},
      all_sections: {},
      display_section: false,
      user_home: true,
    };
  },
  props: {
    email: String,
    nick_name: String,
  },
  components: {
    BooksComponent,
    ProfileComponent,
    SectionComponent,
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/user/login");
    },
    toggleHomeProfile() {
      this.user_home = !this.user_home;
      this.$router.push("/user");
    },
    toggleBookSection() {
      this.display_section = !this.display_section;
      this.$router.push("/user");
    },
    searchAllBooks() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      let data = {
        key: document.getElementById("keyforallsearch").value,
        index: document.getElementById("indexforallsearch").value,
      };
      axios
        .post("http://127.0.0.1:5000/user/search/books", data, {
          headers: this.headers,
        })
        .then((data) => {
          this.all_books = data.data;
        })
        .catch((err) => {
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
          console.log(err);
        });
    },
    searchUserBooks() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      let data = {
        key: document.getElementById("keyforusersearch").value,
        index: document.getElementById("indexforusersearch").value,
      };
      axios
        .post("http://127.0.0.1:5000/user/search/accessible/books", data, {
          headers: this.headers,
        })
        .then((data) => {
          this.ur_books = data.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
        });
    },
    searchAllSections() {
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      let data = {
        key: document.getElementById("keyforsection").value,
      };
      axios
        .post("http://127.0.0.1:5000/user/search/sections", data, {
          headers: this.headers,
        })
        .then((data) => {
          this.all_sections = data.data;
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.authenticated === false) {
            this.$router.push("/user/login");
            return;
          }
        });
    },
  },
  mounted() {
    this.headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
      return;
    }
    axios
      .get("http://127.0.0.1:5000/user/books", {
        headers: this.headers,
      })
      .then((data) => {
        this.all_books = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.authenticated === false) {
          this.$router.push("/user/login");
          return;
        }
      });
    axios
      .get("http://127.0.0.1:5000/user/sections", {
        headers: this.headers,
      })
      .then((data) => {
        this.all_sections = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.authenticated === false) {
          this.$router.push("/user/login");
          return;
        }
      });
    axios
      .get("http://127.0.0.1:5000/user/accessible/books", {
        headers: this.headers,
      })
      .then((data) => {
        this.ur_books = data.data;
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.authenticated === false) {
          this.$router.push("/user/login");
          return;
        }
      });
    localStorage.setItem("edit", false);
  },
};
</script>

<template>
  <div class="row header">
    <div class="col-10">
      <h1>Libra</h1>
      <h3>Welcome, {{ nick_name }}</h3>
    </div>
    <div class="col-1" v-if="user_home === true">
      <br />
      <label class="btn btn-info" role="button" @click="toggleHomeProfile"
        >Profile</label
      >
    </div>
    <div class="col-1" v-if="user_home === false">
      <br />
      <label class="btn btn-info" role="button" @click="toggleHomeProfile"
        >Home</label
      >
    </div>
    <div class="col-1">
      <br />
      <label class="btn btn-info" role="button" @click="logout">Logout</label>
    </div>
  </div>

  <div v-if="user_home === true">
    <div class="col-10">
      <h3>Your Books</h3>
    </div>
    <div class="col-3">
      <span class="inline">
        <input
          class="form-label"
          type="search"
          placeholder="search"
          id="keyforusersearch"
        />
        <select class="form-label" required id="indexforusersearch">
          <option value="1">Name</option>
          <option value="2">Author</option>
        </select>
        <input
          class="btn btn-primary"
          type="submit"
          @click="searchUserBooks"
          value="🔍"
        />
      </span>
    </div>
    <BooksComponent :books="ur_books" :email="email"></BooksComponent>
    <div v-if="display_section === false">
      <span class="inline col-10">
        <h3 class="col-1">All Books</h3>
        <div class="col-3">
          <input
            class="btn btn-primary"
            type="submit"
            @click="toggleBookSection"
            value="Toggle"
          />
        </div>
      </span>
      <div class="col-3">
        <span class="inline">
          <input
            class="form-label"
            type="search"
            placeholder="search"
            id="keyforallsearch"
          />
          <select class="form-label" required id="indexforallsearch">
            <option value="1">Name</option>
            <option value="2">Author</option>
          </select>
          <input
            class="btn btn-primary"
            type="submit"
            @click="searchAllBooks"
            value="🔍"
          />
        </span>
      </div>

      <BooksComponent :books="all_books" :email="email"> </BooksComponent>
    </div>
    <div v-if="display_section === true">
      <div class="row">
        <div class="col-9">
          <h3>
            Available Books sorted by Section
            <input
              class="btn btn-primary"
              type="submit"
              @click="toggleBookSection"
              value="Toggle"
            />
          </h3>
        </div>
        <div class="col-2">
          <span class="inline">
            <input
              class="form-label"
              type="search"
              placeholder="search"
              id="keyforsection"
            />
            <input
              class="btn btn-primary"
              type="submit"
              @click="searchAllSections"
              value="🔍"
            />
          </span>
        </div>
      </div>
      <SectionComponent
        :sections="all_sections"
        :email="email"
      ></SectionComponent>
    </div>
  </div>
  <div v-if="user_home === false">
    <ProfileComponent></ProfileComponent>
  </div>
</template>

<style>
a {
  margin: 5px;
}
.header1 {
  display: block;
}

.ur_books {
  overflow-y: auto;
  height: 350px;
  border-style: solid;
  border-radius: 25px;
  padding-left: 50px;
  background-color: #f8f8eb;
}
.books {
  overflow-y: auto;
  height: 350px;
  padding-left: 10px;
  border-style: solid;
  border-radius: 25px;
  background-color: #f8f8eb;
}
.book {
  float: left;
  margin: 10px;
  margin-right: 40px;
  padding: 10px;
  border-style: solid;
  border-color: dimgrey;
  border-radius: 25px;
  background-color: #f4f5de;
}

.inline {
  display: inline-flex;
  gap: 10px;
}
.all_books {
  overflow-y: auto;
  height: 350px;
  padding-left: 10px;
  border-style: solid;
  border-radius: 25px;
  background-color: #f8f8eb;
}
.inline {
  display: inline-flex;
  gap: 10px;
}
</style>
