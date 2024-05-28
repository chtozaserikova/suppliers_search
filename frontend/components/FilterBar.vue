<template>
    <div  class="p-3 m-3 z-10 w-56  bg-white rounded-lg shadow dark:bg-gray-700">
      <button
          id="dropdownDefault"
          data-dropdown-toggle="dropdown"
          class="mb-3 text-xl font-medium text-gray-900 dark:text-white"
          type="button"
          @click="toggleDropdown"
      >
        <span class="flex items-center">
        Категория
        <svg
            class="w-4 h-4 ml-2"
            aria-hidden="true"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
        >        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
        </span>
      </button>
      <ul id="dropdown-filter" class="hidden space-y-2 text-sm" aria-labelledby="dropdownDefault">
        <li class="flex items-center">
          <input id="c1" type="checkbox" value=""
                 class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

          <label for="c1" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
            Инструменты (9275)
          </label>
        </li>
        <li class="flex items-center">
          <input id="c2" type="checkbox" value=""
                 class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

          <label for="c2" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
            Изделия из металла и пластика (10180)
          </label>
        </li>
        <li class="flex items-center">
          <input id="c2" type="checkbox" value=""
                 class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

          <label for="c2" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
            Промышленное оборудование и станки (3482)
          </label>
        </li>
        <li class="flex items-center">
          <input id="c2" type="checkbox" value=""
                 class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

          <label for="c2" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
            Другое (13482)
          </label>
        </li>
      </ul>
  </div>
  <div  class="p-3 m-3 z-10 w-56  bg-white rounded-lg shadow dark:bg-gray-700">
    <button
        id="dropdownDefaultPrice"
        data-dropdown-toggle="dropdown"
        class="mb-3 text-xl font-medium text-gray-900 dark:text-white"
        type="button"
        @click="toggleDropdownPrice"
    >
        <span class="flex items-center">
        Цена
        <svg
            class="w-4 h-4 ml-2"
            aria-hidden="true"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
        >        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
        </span>
    </button>
    <ul id="dropdown-price" class="hidden space-y-2 text-sm" aria-labelledby="dropdownDefault">
      <li class="flex items-center">
        <input id="p1" type="checkbox" value=""
               class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

        <label for="p1" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
          0 - 5.000
        </label>
      </li>

      <li class="flex items-center">
        <input id="p2" type="checkbox" value=""
               class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

        <label for="p2" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
          5.000 - 100.000
        </label>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "FilterBar",
  methods: {
    toggleDropdown() {
      const dropdown = document.getElementById("dropdown-filter");
      dropdown.classList.toggle("hidden");
    },
    toggleDropdownPrice() {
      const dropdownPrice = document.getElementById("dropdown-price");
      dropdownPrice.classList.toggle("hidden");
    },
  },
}



</script>

<style scoped>

</style>