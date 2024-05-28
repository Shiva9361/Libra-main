<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <main>
    <div class="row header">
      <div class="col-15">
        <h1 class="hh">Libra - Library For All</h1>
      </div>
    </div>
    <div class="login">
      <h2>Choose Login</h2>
      <RouterLink to="/user/login" class="btn btn-info" role="button"
        >User Login</RouterLink
      >
      <RouterLink to="/librarian/login" class="btn btn-info" role="button"
        >Librarain Login</RouterLink
      >
    </div>
  </main>
</template>

<style scoped>
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
h1 {
  margin-top: 40px;
  text-align: center;
  margin-bottom: 0px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
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
.btn-info {
  margin: 10px;
}
</style>
