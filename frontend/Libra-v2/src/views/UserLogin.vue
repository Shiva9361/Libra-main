<script>
import { RouterLink } from "vue-router";
import axios from "axios";
export default {
  name: "UserLogin",
  data() {
    return {
      invalidCredentials: false,
    };
  },
  methods: {
    doLogin() {
      const data = {
        email: document.getElementById("uemail").value,
        password: document.getElementById("upass").value,
      };
      axios
        .post("http://127.0.0.1:5000/login/user", data, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((res) => res.data)
        .then((data) => {
          localStorage.setItem("jwt", data.token);
          localStorage.setItem("nick_name", data.user_details.nick_name);
          localStorage.setItem("email", data.user_details.email);
          console.log(localStorage.getItem("user"));
          this.invalidCredentials = false;
          this.$router.push("/user");
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.error == "Invalid Credentials") {
            this.invalidCredentials = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<template>
  <main>
    <div class="row header-center">
      <div class="col-15">
        <h1 class="hh">Libra - Library For All</h1>
      </div>
    </div>
    <div class="login">
      <h1>Login</h1>
      <div v-if="invalidCredentials">Check Credentials</div>
      <div>
        <label class="form-label"
          >Email
          <input
            class="form-control"
            type="email"
            id="uemail"
            value=""
            required
          />
        </label>
      </div>
      <div>
        <label class="form-label"
          >Password
          <input class="form-control" type="password" id="upass" required />
        </label>
      </div>

      <div>
        <input
          class="btn btn-primary"
          type="submit"
          value="Login"
          @click="doLogin"
        />
      </div>
      <label class="form-label">
        New User? <RouterLink to="/user/register">Register</RouterLink>
      </label>
    </div>
  </main>
</template>
