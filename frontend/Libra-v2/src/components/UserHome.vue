<script>
import axios from "axios";
import BookComponent from "./BookComponent.vue";
import ProfileComponent from "./ProfileComponent.vue";
export default {
  data() {
    return {
      headers: {},
      all_books: {},
      ur_books: {},
      user_home: true,
    };
  },
  props: {
    email: String,
    nick_name: String,
  },
  components: {
    BookComponent,
    ProfileComponent,
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
    <h3>Your Books</h3>
    <BookComponent :books="ur_books" :email="email"></BookComponent>
    <h3>All Books</h3>
    <BookComponent :books="all_books" :email="email"> </BookComponent>
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
  margin-bottom: 30px;
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
.section {
  overflow-y: hidden;
  border-radius: 20px;
  border-style: solid;
  padding-left: 10px;
  padding-right: 10px;
  vertical-align: top;
}
.all_sections {
  overflow-y: auto;
  height: 350px;
  background-color: #f8f8eb;
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
</style>
