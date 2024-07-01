<template>
  <div class="container mx-auto">
    <h1 class="text-3xl font-semibold text-center mt-8 mb-4">На этой странице можно получить рейтинг выбранной компании.</h1>
    <div class="relative mt-4">
      <input v-model="inn" type="text" class="border rounded-md p-2 w-full" placeholder="Введите ИНН компании" @keyup="handleInput">
      <ul v-if="filteredSuggestions.length" class="absolute bg-white shadow-md w-full max-h-32 overflow-auto border border-gray-300 rounded-b-md z-10">
        <li v-for="suggestion in filteredSuggestions" :key="suggestion" class="py-1 px-3 cursor-pointer hover:bg-gray-100" @click="selectSuggestion(suggestion)">{{ suggestion }}</li>
      </ul>
      <button @click="searchInns" class="absolute right-0 top-0 bottom-0 bg-blue-500 text-white px-4 py-2 rounded-r-md">&#10003;</button>
    </div>
    <div class="mt-8">
      <p class="text-lg font-semibold">Выберите тип деловых отношений:</p>
      <div class="flex items-center mt-2">
        <input type="radio" id="agent" name="relationship" value='агент' v-model="relationship" class="mr-2">
        <label for="agent" class="mr-4">Агент</label>
        <input type="radio" id="counterparty" name="relationship" value='контрагент' v-model="relationship" class="mr-2">
        <label for="counterparty">Контрагент</label>
      </div>
    </div>
    <div class="flex justify-center mt-4">
      <button @click="getRecommendation" class="bg-blue-500 text-white px-4 py-2 rounded-md">Получить рекомендацию</button>
    </div>
    <div v-if="recommendation" class="mt-4">
      <p class="text-lg font-semibold">Рекомендация:</p>
      <p v-html="recommendation"></p>
    </div>
    <div v-if="category" class="mt-4">
      <p class="text-lg font-semibold">Категория поставщика:</p>
      <p>{{ category }}</p>
    </div>
    <div class="mt-4 flex justify-center relative">
      <canvas id="ratingChart" width="400" height="400"></canvas>
      <div class="text-center absolute inset-0 flex justify-center items-center text-4xl font-bold text-gray-700 rating-number" v-if="rating !== null">{{ rating }}</div>
    </div>
  </div>
</template>

<script>
import innList from '@/components/inn_list.json';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      inn: '',
      results: [],
      relationship: 'agent',
      recommendation: '',
      suggestions: [],
      rating: null, 
      category: '',
    };
  },
  computed: {
    filteredSuggestions() {
      if (this.inn === '') return [];
      return this.suggestions.filter(suggestion => suggestion.startsWith(this.inn)).slice(0, 5);
    }
  },
  methods: {
    async searchInns() {
      try {
        const response = await fetch('/search_inns/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ start_text: this.inn })
        });
        if (response.ok) {
          const data = await response.json();
          this.results = data.inns;
        } else {
          console.error('Ошибка при выполнении запроса');
        }
      } catch (error) {
        console.error('Произошла ошибка:', error);
      }
    },
    selectSuggestion(suggestion) {
      this.inn = suggestion;
      this.suggestions = []; // Скрыть выпадающий список
    },
    async getRecommendation() {
      try {
        const url = `http://127.0.0.1:8000/api/get_recommendation/?inn=${encodeURIComponent(this.inn)}&agent=${encodeURIComponent(this.relationship)}`;
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          this.recommendation = data.recommendations;
          this.rating = data.rating;
          this.category = data.category;
          this.drawRatingChart(data.rating);
        } else {
          console.error("Ошибка сервера:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Произошла ошибка:", error);
      }
    },
    drawRatingChart(rating) {
      const ctx = document.getElementById('ratingChart').getContext('2d');
      const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Рейтинг', 'Остаток'],
          datasets: [{
            data: [rating, 100 - rating],
            backgroundColor: ['#007BFF', '#E2E2E2'],
            borderWidth: 0,
          }]
        },
        options: {
          cutout: '40%',
          plugins: { legend: { display: false } },
          aspectRatio: 1, // Соотношение сторон 1:1 (можете изменить по вашему усмотрению)
          responsive: false // Отключаем респонсивность для фиксированного размера
        }
      });
    },
    handleInput() {
      this.suggestions = innList.filter(suggestion => suggestion.startsWith(this.inn));
    },
  },
}
</script>

<style scoped>
#ratingChart {
  width: 200px; /* Или любое другое значение по вашему усмотрению */
  height: 200px; /* Или любое другое значение по вашему усмотрению */
}
.rating-number {
  font-size: 2em; /* Или любое другое значение по вашему усмотрению */
}
/* Добавляем анимацию для появления рекомендации */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active в версии 2.1.8+ */ {
  opacity: 0;
}
</style>