<template>
  <div class="row header">
    <div class="col-15">
      <h1 class="hh">Libra - Library For All</h1>
    </div>
  </div>

  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="submit">
      <div>
        <label class="form-label"
          >User Name
          <input class="form-control" type="text" id="uname" required />
        </label>
      </div>
      <div v-if="udne">
        <label class="form-label">User Name not Found</label>
      </div>
      <div>
        <label class="form-label"
          >Password
          <input class="form-control" type="password" id="upass" required />
        </label>
        <div v-if="wrong_pass">
          <div class="signup">Wrong Password!!</div>
        </div>
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

<style>
.hh {
  margin: 10px;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.signup {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-top: 40px;
  text-align: center;
}
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 200px;
  margin-left: 720px;
  border-style: solid;
  width: 20%;
  padding: 50px;
  padding-top: 10px;
  background-color: #f8f8eb;
}
.header {
  border-style: solid;
  background-color: black;
  border-color: black;
  color: white;
  display: flex;
  text-align: center;
}
</style>
