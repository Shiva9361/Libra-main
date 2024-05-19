<template>
  <div class="row">
    <div class="col-9">
      <h3>
        Available Books sorted by Section
        <a href="/user/home/0" class="btn btn-primary" role="button">Toggle</a>
      </h3>
    </div>
    <div class="col-2">
      <form action="/user/home/search/sections" method="post">
        <span class="inline">
          <input
            class="form-label"
            type="search"
            placeholder="search"
            name="key"
          />
          <input class="btn btn-primary" type="submit" value="🔍" />
        </span>
      </form>
    </div>
  </div>
  <div class="all_sections">
    {% for section in sections %} {% if section.section_id!=0%}
    <div class="section">
      <h5>
        Section Name : {{ section.name }}<br />
        Description : {{ section.description }}
      </h5>
      {% for book in section.books %}
      <div class="book col-2">
        Name: {{ book.name }} <br />
        Author: {{ book.authors }} <br />
        {% if book.user_email == mail%}
        <a
          href="/user/readbook/{{book.book_id}}"
          class="btn btn-primary"
          role="button"
          >Read</a
        >
        {% else %}
        <a
          href="/user/requestbook/{{book.book_id}}"
          class="btn btn-primary"
          role="button"
          >Request</a
        >
        <a
          href="/user/checkfeedback/{{book.book_id}}"
          class="btn btn-primary"
          role="button"
          >Check Feedback</a
        >
        {% endif %}
      </div>
      {% endfor %}
    </div>
    {% endif %} {% endfor %}
  </div>
</template>
