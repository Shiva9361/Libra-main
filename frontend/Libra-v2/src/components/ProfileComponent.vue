<script>
import axios from "axios";
export default {
  data() {
    return {
      user_details: {},
      edit: Boolean,
      books: [],
    };
  },
  methods: {
    editFun() {
      this.edit = !this.edit;
      localStorage.setItem("editProfile", this.edit);
      this.$router.push("/user");
    },
    updateProfile() {
      if (isNaN(document.getElementById("cno").value)) {
        alert("Phone number must be a number");
        return;
      }
      if (document.getElementById("cno").value.length != 10) {
        alert("Enter 10 digit number");
        return;
      }
      let data = {
        pname: document.getElementById("pname").value,
        fname: document.getElementById("fname").value,
        lname: document.getElementById("lname").value,
        cno: document.getElementById("cno").value,
        about: document.getElementById("about").value,
      };
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      axios
        .post("http://127.0.0.1:5000/user/profile/edit", data, {
          headers: headers,
        })
        .catch((err) => {
          console.log(err);
          alert("Some error occured");
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
        })
        .then(() => {
          this.edit = !this.edit;
          localStorage.setItem("editProfile", this.edit);
          localStorage.setItem("nick_name", data.pname);
          window.dispatchEvent(
            new CustomEvent("nick_name_changed", {
              detail: {
                storage: localStorage.getItem("nick_name"),
              },
            })
          );
          // update again in frontend
          axios
            .get("http://127.0.0.1:5000/user/profile", {
              headers: headers,
            })
            .then((data) => {
              this.user_details = data.data.user;
              this.read_books = data.data.books;
            })
            .catch((err) => {
              console.log(err);
              if (err.response.data.invalid) {
                this.$router.push("/user/login");
                return;
              }
            });
        });
    },
  },
  mounted() {
    let headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt")}`,
    };
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
      return;
    }
    if (!localStorage.getItem("editProfile")) {
      localStorage.setItem("editProfile", false);
    }
    this.edit = localStorage.getItem("editProfile") == "false" ? false : true;
    axios
      .get("http://127.0.0.1:5000/user/profile", {
        headers: headers,
      })
      .then((data) => {
        this.user_details = data.data.user;
        this.books = data.data.books;
        for (let index in this.books) {
          let data = this.books[index].on;
          data = data.split(" ");
          this.books[index].on = data.slice(1, 4).join(" ");
        }
      })
      .catch((err) => {
        console.log(err);
        if (err.response.data.invalid) {
          this.$router.push("/user/login");
          return;
        }
      });
  },
};
</script>
<template>
  <div v-if="edit === false">
    <h3>Profile</h3>

    <div class="profile">
      <div class="items">
        <h3>Profile Name : {{ user_details.nick_name }}</h3>
      </div>
      <div class="items">
        <h5 v-if="user_details.last_name">
          Full Name : {{ user_details.first_name }} {{ user_details.last_name }}
        </h5>
        <h5 v-if="!user_details.last_name">
          Full Name : {{ user_details.first_name }}
        </h5>
      </div>
      <div class="items">
        <h5>Email : {{ user_details.email }}</h5>
      </div>
      <div class="items">
        <h5>Contact No : {{ user_details.phone_number }}</h5>
      </div>
      <div class="about items" v-if="user_details.about">
        <h5>About :<br />{{ user_details.about }}</h5>
      </div>

      <div class="read-books">
        <h3>Books Read : {{ books.length }}</h3>
        <div class="book col-2" v-for="book in books">
          Name: {{ book.name }} <br />
          Author: {{ book.authors }} <br />
          On: {{ book.on }}<br />
        </div>
      </div>
    </div>
    <div class="edit-button">
      <label class="btn btn-primary" role="button" @click="editFun">Edit</label>
    </div>
  </div>
  <div v-if="edit === true">
    <h3 class="h3h">Edit Profile</h3>
    <form @submit.prevent="updateProfile">
      <div class="form">
        <div>
          <label class="form-label"
            >Email :
            <input
              class="form-control"
              type="text"
              id="email"
              v-model="user_details.email"
              readonly
            />
          </label>
        </div>
        <div>
          <label class="form-label"
            >Profile Name :
            <input
              class="form-control"
              type="text"
              id="pname"
              v-model="user_details.nick_name"
              required
            />
          </label>
        </div>
        <div>
          <label class="form-label"
            >First Name :
            <input
              class="form-control"
              type="text"
              id="fname"
              v-model="user_details.first_name"
              required
            />
          </label>
        </div>
        <div>
          <label class="form-label"
            >Last Name :
            <input
              class="form-control"
              type="text"
              id="lname"
              v-model="user_details.last_name"
            />
          </label>
        </div>
        <div>
          <label class="form-label"
            >Phone Number :
            <input
              class="form-control"
              type="text"
              id="cno"
              v-model="user_details.phone_number"
              required
            />
          </label>
        </div>
        <div>
          <label class="form-label"
            >About :
            <textarea
              class="form-control"
              id="about"
              required
              rows="5"
              cols="100"
              >{{ user_details.about }}</textarea
            >
          </label>
        </div>
        <div>
          <input class="btn btn-primary" type="submit" value="Submit" />
        </div>
      </div>
    </form>
  </div>
</template>
