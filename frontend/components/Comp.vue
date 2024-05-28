<template>
  <form class="pt-8 pb-8 ml-64 w-1/2" @submit.prevent="submitSearch">
    <div class="relative w-full">
      <input type="search" v-model="query" @input="onSearch" id="search-dropdown" class="block p-2.5 w-full z-20 text-xl text-gray-900 bg-gray-50 rounded-[16px] border-l-gray-50 border-l-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-l-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500" placeholder="Искать товары, категории..." required>
      <button
          type="submit"
          class="absolute top-0 right-0 p-2.5 text-sm font-medium h-full text-white bg-blue-700 rounded-r-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
        </svg>
        <span class="sr-only">Искать</span>
      </button>
    </div>
    <ul v-if="results.length">
      <li v-for="result in results" :key="result">{{ result }}</li>
    </ul>
    <!-- Список сохраненных поисковых запросов -->
    <ul v-if="searchStore.searchHistory.length" class="mt-4 pr-2 flex flex-wrap">
      <li v-for="(query, index) in searchStore.searchHistory" :key="index">
        <button @click="selectQuery(query, $event)" class="p-2.5 mr-1 text-sm font-medium h-full text-gray-900 bg-gray-200 rounded-lg border border-gray-300 hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-blue-300">{{ query }}</button>
        <button @click="deleteQuery(index)" class="text-red-500 mr-6"><svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M6 6L14 14M14 6L6 14"/>
        </svg>
        </button>
      </li>
    </ul>

    <!-- Кнопка для очистки всей истории -->
    <div v-if="searchStore.searchHistory.length" class="mt-4">
      <button
          @click="clearHistory"
          class="p-2.5 text-sm font-medium h-full text-gray-900 bg-gray-200 rounded-lg border border-gray-300 hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-blue-300"
      >
        Очистить всю историю
      </button>
    </div>
  </form>
  <div v-if="results && results.length" class="flex flex-wrap">
    <div v-for="result in results" :key="result.row_number" class="flex flex-row p-2">
      <Card :item="result"/>
    </div>
  </div>
</template>

<script>
import { useSearchStore } from '../store/searchStore';
import { useRouter } from 'vue-router';

import { ref } from 'vue';

export default {
  name: "Comp.vue",
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
        } else {
          console.error("Ошибка сервера:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Ошибка поиска:", error);
      }
    }
  },
  setup() {
    const router = useRouter(); // <-- Add this line
    const data = ref([]);

    const searchStore = useSearchStore();
    const query = ref('');  // Используем ref для управления значением input

    const submitSearch = async () => {
      const searchInput = document.getElementById("search-dropdown");
      searchStore.setQuery(searchInput.value);
      if (query.value.trim()) {
        searchStore.setQuery(query.value);
        router.push({ name: 'index', query: { q: query.value.trim() } });
        try {
          const response = await fetch('http://127.0.0.1:8000/api/suppliers2/?search=' + encodeURIComponent(query.value.trim()));
          if (response.ok) {
            const data = await response.json();
            this.results = data.results;
            console.log(data.results);
          } else {
            console.error("Ошибка сервера:", response.status, response.statusText);
          }
        } catch (error) {
          console.error("Ошибка поиска:", error);
        }
        query.value = '';
      }
      searchInput.value = '';  // Очищаем поле ввода после отправки
    };

    const selectQuery = (selectedQuery, event) => {
      event.preventDefault();
      const search = document.getElementById("search-dropdown");
        search.value = `${selectedQuery}`;
    };

    const deleteQuery = (index) => {
      searchStore.deleteQuery(index);
    };

    const clearHistory = () => {
      searchStore.clearHistory();
    };

    return { searchStore, query, submitSearch, selectQuery, deleteQuery, clearHistory };
  }
}
</script>

<style scoped>

</style>
