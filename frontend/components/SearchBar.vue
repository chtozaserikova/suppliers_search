<template>
  <div class="sm:w-80 md:w-80 lg:w-100 rounded overflow-hidden shadow-lg p-2 m-1 ">
    <input type="text" v-model="query" @input="onSearch" />
    <ul v-if="results.length">
      <li v-for="result in results" :key="result">{{ result }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      results: []
    };
  },
  methods: {
    async onSearch() {
      if (!this.query) {
        this.results = [];
        return;
      }
      try {
        const response = await fetch('http://127.0.0.1:8000/api/search/?q=' + encodeURIComponent(this.query));
        if (response.ok) {
          const data = await response.json();
          this.results = data.results;
          console.log(data.results)
        } else {
          console.error("Ошибка сервера:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Ошибка поиска:", error);
      }
    }
  }
};
</script>
