<template>
  <Header></Header>
  <div class="flex flex-row">
    <div>
  <FilterBar/>
    </div>
    <div>
    <Suppliers/>
    </div>
  </div>
</template>

<script>
import Header from '../components/Header.vue'
import Card from '../components/Card.vue'
import FilterBar from '../components/FilterBar.vue'
import Suppliers from '../components/Suppliers.vue'
import SearchBar from '../components/SearchBar.vue'

export default {
  name: "index.vue",
  components: {SearchBar, Card, Header},
  data() {
    return {
      items: new Array(10).fill(null),

    };
  }
}
</script>

<style scoped>

</style>