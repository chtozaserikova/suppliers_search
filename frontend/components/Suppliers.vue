<template>
  <div class="search-bar">
    <div class="relative w-1/2 m-4">

    <input v-model="searchQuery" @input="onSearch" type="text" class="block p-2.5 w-full z-20 text-xl text-gray-900 bg-gray-50 rounded-[16px] border-l-gray-50 border-l-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-l-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500" placeholder="Искать товары, категории..." required>
    <button
        class="absolute top-0 right-0 p-2.5 text-sm font-medium h-full text-white bg-blue-700 rounded-r-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        @click="executeSearch">
      <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
      </svg>
      <span class="sr-only">Искать</span>
    </button>

    </div>
    <ul v-if="results.length">
      <li v-for="result in results" :key="result">{{ result }}</li>
    </ul>
  </div>

  <div class="flex flex-wrap">
    <div v-for="(item, index) in data.slice((current_page - 1) * 15, (current_page - 1) * 15 + 15)" :key="index" class="flex flex-row p-2" v-if="data && data.length">
      <Card :item="item"/>
    </div>
  </div>
  <nav aria-label="Paginate me">
    <ul class="flex flex-wrap justify-center space-x-2">
      <nuxt-link v-if="previous != null" class="px-4 py-2 border rounded" :to="`?page=${current_page - 1}`" tabindex="-1">Предыдущая</nuxt-link>
      <li v-else class="px-4 py-2 border rounded bg-gray-200 text-gray-400 cursor-not-allowed">
        <a href="#" tabindex="-1">Предыдущая</a>
      </li>
      <template v-for="i in total">
      <template v-if="i <= 10 || (i > current_page - 2 && i < current_page + 2)">
        <li v-if="current_page === i || ($route.query.page === '/' && i === 1)" class="px-4 py-2 border rounded bg-blue-500 text-white">
          <nuxt-link :to="`?page=${i}`">{{i}}</nuxt-link>
        </li>
        <li v-else class="px-4 py-2 border rounded hover:bg-gray-200">
          <nuxt-link :to="`?page=${i}`">{{i}}</nuxt-link>
        </li>
      </template>
      <template v-else-if="i === 11 && total.value > 10">
        <li class="px-4 py-2 border rounded hover:bg-gray-200">...</li>
      </template>
      <template v-else-if="i === total.value">
        <li class="px-4 py-2 border rounded hover:bg-gray-200">{{total.value}}</li>
      </template>
    </template>

      <nuxt-link v-if="next != null" class="px-4 py-2 border rounded" :to="`?page=${current_page + 1}`">Следующая</nuxt-link>
      <li v-else class="px-4 py-2 border rounded bg-gray-200 text-gray-400 cursor-not-allowed">
        <a href="#">Следующая</a>
      </li>
    </ul>
  </nav>

</template>

<script>
import Card from './Card.vue'
import { useRouter } from 'vue-router';
import { ref, watch } from 'vue';

export default {
  name: "Suppliers",
  components: {
    Card
  },
  data() {
    return {
      searchQuery: '',
      results: []
    };
  },
  methods: {
    async onSearch() {
      if (!this.searchQuery) {
        this.results = [];
        return;
      }
      try {
        const response = await fetch('http://127.0.0.1:8000/api/search/?q=' + encodeURIComponent(this.searchQuery));
        if (response.ok) {
          const data = await response.json();
          this.results = data.results;
        } else {
          console.error("Ошибка сервера:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Ошибка поиска:", error);
      }
    }
  },
  setup() {
    const data = ref([]);
    const total = ref(0);
    const next = ref(null);
    const previous = ref(null);
    const current_page = ref(1);
    const router = useRouter();
    const searchQuery = ref('');

// Function to load data
    const loadData = async () => {
      try {
        const page = router.currentRoute.value.query.page || 1;
        const query = router.currentRoute.value.query.q || '';
        searchQuery.value = query;
        const response = await fetch(`http://127.0.0.1:8000/api/suppliers2/?search=${encodeURIComponent(query)}&page=${page}`);
        const responseData = await response.json();
        data.value = responseData.results;
        total.value = Math.ceil(responseData.count / 15);
        next.value = responseData.next ? new URL(responseData.next).searchParams.get("page") : null;
        previous.value = responseData.previous ? new URL(responseData.previous).searchParams.get("page") : null;
        current_page.value = Number(page);
      } catch (error) {
        console.error('Произошла ошибка при загрузке данных:', error);
      }
    }
    const executeSearch = () => {
      router.push({ path: router.currentRoute.value.path, query: { q: searchQuery.value, page: 1 } });
      loadData();
    }

    // Watch for changes in route query 'page' and 'q' and load data
    watch(() => ({page: router.currentRoute.value.query.page, q: router.currentRoute.value.query.q}), loadData, { immediate: true });

    return { data, total, next, previous, current_page, searchQuery, executeSearch };
  }
}
</script>

<style scoped>

</style>