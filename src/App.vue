<template>
  <div id="app">
    <SalesDashboard />
  </div>
</template>

<script>
import SalesDashboard from './components/SalesDashboard.vue';

export default {
  name: 'App',
  components: {
    SalesDashboard
  }
}
</script>

<style>
#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
