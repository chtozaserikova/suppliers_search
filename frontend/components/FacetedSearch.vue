<template>
  <div class="search-bar">
    <div class="flex flex-wrap m-4">

<!--      <input v-model="searchQuery"  type="text" class="block p-2.5 w-full z-20 text-xl text-gray-900 bg-gray-50 rounded-[16px] border-l-gray-50 border-l-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-l-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500" placeholder="Искать товары, категории..." required>-->
      <div class="flex flex-col mb-4 px-4 w-1/4"> <!-- w-1/4 задаст каждому блоку ширину в 25% от родительского элемента -->
        <label for="price" class="mb-2 text-gray-700">Цена</label>
        <input id="price" v-model="price" type="text" class="border p-2 rounded-md" placeholder="Цена" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="supplier" class="mb-2 text-gray-700">Поставщик</label>
        <input id="supplier" v-model="supplier" type="text" class="border p-2 rounded-md" placeholder="Поставщик" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="volume" class="mb-2 text-gray-700">Объем</label>
        <input id="volume" v-model="volume" type="text" class="border p-2 rounded-md" placeholder="Объем" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="okpd" class="mb-2 text-gray-700">ОКПД2</label>
        <input id="okpd" v-model="okpd" type="text" @input="onSearch" class="border p-2 rounded-md" placeholder="ОКПД2" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="name" class="mb-2 text-gray-700">Название</label>
        <input id="name" v-model="name" type="text" class="border p-2 rounded-md" placeholder="Название" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="inn" class="mb-2 text-gray-700">ИНН</label>
        <input id="inn" v-model="inn" type="text" class="border p-2 rounded-md" placeholder="ИНН" required>
      </div>

      <div class="flex flex-col mb-4 px-4 w-1/4">
        <label for="ogrn" class="mb-2 text-gray-700">ОГРН</label>
        <input id="ogrn" v-model="ogrn" type="text" class="border p-2 rounded-md" placeholder="ОГРН" required>
      </div>
      <div class="flex flex-col px-4 w-1/4 pt-8">
      <button
          class=" pt-2  w-20 h-10 p-2.5 text-sm font-medium  text-white bg-blue-700 rounded-r-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          @click="executeSearch">
        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
        </svg>
        <span class="sr-only">Искать</span>
      </button>
      </div>
    </div>
    <ul v-if="results.length">
      <li v-for="result in results" :key="result">{{ result }}</li>
    </ul>
  </div>

  <div class="flex flex-wrap">
    <div v-for="item in data" :key="item.index" class="flex flex-row p-2" v-if="data && data.length">
      <Card :item="item"/>
    </div>
  </div>
  <nav aria-label="Paginate me">
    <ul class="flex flex-wrap justify-center space-x-2">
      <nuxt-link v-if="previous != null" class="px-4 py-2 border rounded" :to="previous" tabindex="-1">Предыдущая</nuxt-link>
      <li v-else class="px-4 py-2 border rounded bg-gray-200 text-gray-400 cursor-not-allowed">
        <a href="#" tabindex="-1">Предыдущая</a>
      </li>
      <template v-for="i in total">
        <li v-if="current_page === i || ($route.query.page === '/' && i === 1)" class="px-4 py-2 border rounded bg-blue-500 text-white">
          <nuxt-link :to="`?page=${i}`">{{i}}</nuxt-link>
        </li>
        <li v-else class="px-4 py-2 border rounded hover:bg-gray-200">
          <nuxt-link :to="`?page=${i}`">{{i}}</nuxt-link>
        </li>
      </template>
      <nuxt-link v-if="next != null" class="px-4 py-2 border rounded" :to="next">Следующая</nuxt-link>
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
  name: "FacetedSearch",
  components: {
    Card
  },
  data() {
    return {
      searchQuery: '',
      results: [],
      price: '',
      supplier: '',
      volume: '',
      okpd: '',
      name: '',
      inn: '',
      ogrn: ''
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

    const price = ref('');      // Добавьте эту строку
    const supplier = ref('');   // Добавьте эту строку
    const volume = ref('');     // Добавьте эту строку
    const okpd = ref('');       // Добавьте эту строку
    const name = ref('');       // Добавьте эту строку
    const inn = ref('');        // Добавьте эту строку
    const ogrn = ref('');       // Добавьте эту строку
// Function to load data
    const loadData = async () => {
      try {
        const page = router.currentRoute.value.query.page || 1;
        const query = router.currentRoute.value.query.q || '';
        searchQuery.value = query;

        let queryParams = [];
        queryParams.push(`okpd=${encodeURIComponent(okpd.value)}`);
        queryParams.push(`price=${encodeURIComponent(price.value)}`);  // Измените эту строку
        queryParams.push(`supplier=${encodeURIComponent(supplier.value)}`); // Измените эту строку
        queryParams.push(`volume=${encodeURIComponent(volume.value)}`); // Измените эту строку
        queryParams.push(`name=${encodeURIComponent(name.value)}`);     // Измените эту строку
        queryParams.push(`inn=${encodeURIComponent(inn.value)}`);       // Измените эту строку
        queryParams.push(`ogrn=${encodeURIComponent(ogrn.value)}`);     // Измените эту строку
        const queryString = queryParams.join('&');

        console.log(`Запрос к: http://127.0.0.1:8000/api/suppliers2/?${queryString}&page=${page}`);

        const response = await fetch(`http://127.0.0.1:8000/api/suppliers2/?${queryString}&page=${page}`);
        const responseData = await response.json();
        data.value = responseData.results;
        total.value = Math.ceil(responseData.count / 500);
        next.value = responseData.next ? new URL(responseData.next).searchParams.get("page") : null;
        previous.value = responseData.previous ? new URL(responseData.previous).searchParams.get("page") : null;
        current_page.value = Number(page);
      } catch (error) {
        console.error('Произошла ошибка при загрузке данных:', error);
      }
    }

    const executeSearch = () => {
      console.log("Функция executeSearch вызвана");
      const queryParams = { page: 1 };

      if (searchQuery.value) queryParams.q = searchQuery.value;
      if (price.value) queryParams.price = price.value;
      if (supplier.value) queryParams.supplier = supplier.value;
      if (volume.value) queryParams.volume = volume.value;
      if (okpd.value) queryParams.okpd = okpd.value;
      if (name.value) queryParams.name = name.value;
      if (inn.value) queryParams.inn = inn.value;
      if (ogrn.value) queryParams.ogrn = ogrn.value;

      router.push({ path: `${router.currentRoute.value.path}`, query: queryParams });
      loadData();
    }

    // Watch for changes in route query 'page' and 'q' and load data
    watch(() => ({page: router.currentRoute.value.query.page, q: router.currentRoute.value.query.q}), loadData, { immediate: true });

    return { data, total, next, previous, current_page, searchQuery, price, supplier, volume, okpd, name, inn, ogrn, executeSearch };  // Добавьте новые свойства здесь
  }
}
</script>

<style scoped>

</style>