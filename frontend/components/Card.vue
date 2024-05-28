<template>
  <div class="sm:w-80 md:w-80 lg:w-100 rounded overflow-hidden shadow-lg p-2 m-1 ">
    <div class="px-6 py-4">
      <div class="font-bold text-gray-700 text-3xl ">{{ item.product_name }}</div>
      <div>
        <p class="font-bold text-blue-700 text-base pb-8">{{ item.product_company }}</p>
      </div>
      <div class="flex flex-wrap justify-between font-bold text-xl mb-2">

      </div>
      <div class="flex flex-wrap flex-col mb-4 ">
        <div class=" mb-2">
          <p class="text-gray-700 text-base">Цена: {{ item.product_price }}</p>
        </div>
        <div class="">
          <p class="text-gray-700 text-base">{{ item.product_desc }}</p>
        </div>
      </div>
      <!-- Остальное содержимое карточки -->
    </div>
    <div class="px-6 pt-4 pb-2">
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-xl font-semibold text-gray-700 mr-2 mb-2">ОКПД 2:{{ item.okpd2 }}</span>
      <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-xl font-semibold text-gray-700 mr-2 mb-2">ОГРН: {{ item.ogrn }}</span>
      <span class99="inline-block bg-gray-200 rounded-full px-3 py-1 text-xl font-semibold text-gray-700 mr-2 mb-2">ИНН: {{ item.inn }}</span>

      <div v-if="item.ссылка_на_товар">
        <a :href="item.ссылка_на_товар" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Ссылка
          <svg class="w-3.5 h-3.5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "Card",
  props: {
    item: Object // Определите тип пропса в соответствии с вашими данными
  }
}
</script>

<style scoped>

</style>