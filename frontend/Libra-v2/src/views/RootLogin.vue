<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <main>
    <div class="row header-center">
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
