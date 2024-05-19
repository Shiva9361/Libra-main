<template>
  <div class="col-3">
    <form action="/user/home/search/books" method="post">
      <span class="inline">
        <input
          class="form-label"
          type="search"
          placeholder="search"
          name="key"
        />
        <select class="form-label" required name="index">
          <option value="1">Name</option>
          <option value="2">Author</option>
        </select>
        <input class="btn btn-primary" type="submit" value="🔍" />
      </span>
    </form>
  </div>
</template>
