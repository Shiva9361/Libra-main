<template>
  <div class="row header">
    <div class="col-lg">
      <h1>Libra</h1>
      <h3>Welcome, {{ nick_name }}</h3>
    </div>
    <div class="col-auto">
      <br />
      <label class="btn btn-info" role="button" @click="goHome">Home</label>
    </div>
    <div class="col-auto">
      <br />
      <label class="btn btn-info" role="button" @click="logout">Logout</label>
    </div>
  </div>
  <h3>Payment Portal</h3>
  <form @submit.prevent="submitPayment(id)">
    <div class="feedback_form">
      <div>
        <label class="form-label"
          >Book Name
          <input
            class="form-control"
            type="text"
            id="bookname"
            :value="book_name"
            readonly
          />
        </label>
        <label class="form-label"
          >Card Number
          <input
            class="form-control"
            type="text"
            id="card_id"
            pattern="[0-9]{16}"
          />
        </label>
        <label class="form-label"
          >CVV
          <input class="form-control" type="text" id="cvv" pattern="[0-9]{3}" />
        </label>
      </div>
      <div>
        <input class="btn btn-primary" type="submit" value="Submit" />
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  props: {
    nick_name: String,
    id: String,
    book_name: String,
  },
  methods: {
    goHome() {
      this.$router.push("/user");
    },
    logout() {
      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/user/logout`, {
          headers: headers,
        })
        .then(() => {
          localStorage.clear();
          this.$router.push("/user/login");
        })
        .catch((err) => {
          localStorage.clear();
        });
    },
    submitPayment(book_id) {
      let check_number = (val) => {
        var sum = 0;
        for (var i = 0; i < val.length; i++) {
          var intVal = parseInt(val.substr(i, 1));
          if (i % 2 == 0) {
            intVal *= 2;
            if (intVal > 9) {
              intVal = 1 + (intVal % 10);
            }
          }
          sum += intVal;
        }
        return sum % 10 == 0;
      };
      if (!check_number(document.getElementById("card_id").value)) {
        alert("Card Number Not Valid");
        return;
      }

      let headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("jwt")}`,
      };
      if (!localStorage.getItem("jwt")) {
        this.$router.push("/user/login");
      }
      axios
        .get(`http://127.0.0.1:5000/user/buy/${book_id}`, {
          headers: headers,
        })
        .then((data) => {
          if (data.data.message == "done") {
            alert("Bought");
          } else if (data.status == 201) {
            alert("Already owned");
          }
        })
        .then(() => {
          this.$router.push("/user");
          return;
        })
        .catch((err) => {
          if (err.response.data.invalid) {
            this.$router.push("/user/login");
            return;
          }
          if (err.response.status === 404) {
            alert("Does Not Exist");
          }
          console.log(err);
        });
    },
  },
  mounted() {
    if (!localStorage.getItem("jwt")) {
      this.$router.push("/user/login");
      return;
    }
  },
};
</script>
