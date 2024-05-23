<script>
import axios from "axios";
export default {
  props: {
    id: String,
  },
  data() {
    return {
      email_exists: false,
    };
  },
  methods: {
    submit() {
      let data = {
        email: document.getElementById("email").value,
        fname: document.getElementById("fname").value,
        lname: document.getElementById("lname").value,
        pnum: document.getElementById("pnum").value,
        nick_name: document.getElementById("nick_name").value,
        password: document.getElementById("password").value,
      };
      if (document.getElementById("password2").value !== data.password) {
        console.log(password);
        console.log(document.getElementById("password2"));
        alert("Confirm password does not match");
        return;
      }
      if (isNaN(data.pnum)) {
        alert("Enter valid number");
        return;
      } else if (data.pnum.length != 10) {
        alert("Enter 10 digit phone number");
        return;
      }
      axios
        .post(`http://127.0.0.1:5000/signup/user`, data)
        .catch((err) => {
          if (err.response.status === 401) {
            window.confirm("Email Already registered").then(() => {
              this.$router.push("/user/login");
            });

            return;
          }
          console.log(err);
        })
        .then((res) => {
          console.log(res);
          if (res.status == 201) {
            window.confirm("Created");
          }
        })
        .then(() => {
          this.$router.push("/user/login");
        });
    },
  },
};
</script>
<template>
  <div class="row header">
    <div class="col-15">
      <h1 class="hh">Libra - Library For All</h1>
    </div>
  </div>
  <div class="signup">
    <h1>Sign Up</h1>
    <div v-if="email_exists">
      <label class="form-label">Email is already registered</label>
    </div>
    <form @submit.prevent="submit">
      <div>
        <label class="form-label">First Name</label>
        <input class="form-control" type="text" id="fname" required />
      </div>
      <div>
        <label class="form-label">Last Name</label>
        <input class="form-control" type="text" id="lname" />
      </div>
      <div>
        <label class="form-label">Phone Number</label>
        <input class="form-control" type="text" id="pnum" required />
      </div>
      <div>
        <label class="form-label">Email Address</label>
        <input class="form-control" type="email" id="email" required />
      </div>
      <div>
        <label class="form-label">Nick Name</label>
        <input class="form-control" type="text" id="nick_name" required />
      </div>
      <div>
        <label class="form-label">Password</label>
        <input
          class="form-control"
          pattern=".{8,}"
          type="password"
          id="password"
          required
          title="Atleast 8 characters"
        />
      </div>
      <br />
      <div>
        <label class="form-label">Confirm Password</label>
        <input
          class="form-control"
          pattern=".{8,}"
          type="password"
          id="password2"
          required
          title="Atleast 8 characters"
        />
      </div>
      <br />
      <div>
        <input class="btn btn-primary" type="submit" value="Submit" />
      </div>
    </form>
  </div>
</template>

<style scoped>
h1 {
  margin-top: 40px;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  align-items: normal;
}
.signup {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 100px;
  margin-left: 650px;
  border-style: solid;
  width: 30%;
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
.hh {
  margin: 10px;
}
</style>
