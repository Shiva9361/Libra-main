<template>
  <div class="row header-center">
    <div class="col-15">
      <h1 class="hh">Libra - Library For All</h1>
    </div>
  </div>

  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="submit" class="librarian-login-form">
      <div>
        <label class="form-label"
          >User Name
          <input class="form-control" type="text" id="uname" required />
        </label>
      </div>
      <div v-if="udne">
        <label class="form-label">User Name not Found</label>
      </div>
      <div v-if="wrong_pass">
        <div class="form-label">Wrong Password!!</div>
      </div>
      <div>
        <label class="form-label"
          >Password
          <input class="form-control" type="password" id="upass" required />
        </label>
      </div>

      <div>
        <input class="btn btn-primary" type="submit" value="Login" />
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      wrong_pass: false,
      udne: false,
    };
  },
  methods: {
    submit() {
      let data = {
        uname: document.getElementById("uname").value,
        upass: document.getElementById("upass").value,
      };
      axios
        .post("http://127.0.0.1:5000/login/librarian", data, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((res) => res.data)
        .then((data) => {
          localStorage.setItem("jwt", data.token);
          localStorage.setItem("nick_name", data.librarian_details.user_name);
          this.$router.push("/librarian");
        })
        .catch((err) => {
          console.log(err);
          if (err.response.status === 404) {
            this.udne = true;
            this.wrong_pass = false;
          }
          if (err.response.status === 403) {
            this.wrong_pass = true;
            this.udne = false;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
