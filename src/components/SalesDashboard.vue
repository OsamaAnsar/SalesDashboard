<template>
  <div>
    <h3 class="text-gray">Sales Data Dashboard</h3>
    <SalesFilters
      @update-filters="applyFilters"
      :currency-options="currencyOptions"
      :customer-options="customerOptions"
      :location-options="locationOptions"
    />
    <div class="chart-container">
      <StackedBarChart v-if="salesData" :sales-data="salesData" :company-name="companyName" :denomination="denomination"/>
    </div>
  </div>
</template>

<script>
import SalesFilters from './SalesFilters.vue';
import StackedBarChart from './StackedBarChart/StackedBarChart.vue';
// import { commaSeparatedValue } from '@/helpers/helper';

export default {
  name: 'SalesDashboard',

  components: {
    SalesFilters,
    StackedBarChart,
  },

  data() {
    return {
      // Initial sales chart configuration (you can customize this)
      salesChart: {
        chartData: {
          labels: [],
          datasets: [
            {
              label: 'Sales Data',
              data: [],
              backgroundColor: '#64B5F6',
              borderColor: '#4DD0E1',
              borderWidth: 1,
            },
          ],
        },
        chartOptions: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Sales Amount',
              },
            },
          },
          plugins: {
            title: {
              display: true,
              text: 'Sales Data Over Time',
            },
            legend: {
              position: 'bottom',
            },
          },
        },
      },
      companyName: '',
      customerOptions: [],
      currencyOptions: [],
      locationOptions: [],
      salesData: null,
      denomination: '$',
    };
  },

  methods: {
    // Fetch filtered sales data
    async fetchSalesData(params) {
      const query = new URLSearchParams(params).toString();
      const response = await fetch(
        `http://127.0.0.1:5000/api/sales-data?${query}`,
        {
          cache: 'no-store',
        }
      );
      const data = await response.json();
      return data;
    },

    // Build the chart data from the fetched sales data
    async buildChart(filters = {}) {
      const salesData = await this.fetchSalesData(filters);
      console.log('Sales Data', salesData);
      this.currencyOptions = salesData.meta.currencies || [];
      this.customerOptions = salesData.meta.customers || [];
      this.locationOptions = salesData.meta.locations || [];
      this.salesData = salesData.periods[(filters || {}).period || 'YTD F2024'] || [];
      this.companyName = salesData.company_name || '';
      this.denomination = salesData.denomination || '$';
      console.log('Sales Data', salesData.periods, filters.period);
    },

    // Handle filter updates from the SalesFilters component
    async applyFilters(filters) {
      await this.buildChart(filters);
    },
  },

  // Lifecycle hook to fetch initial data when the component is mounted
  mounted() {
    this.buildChart();
  },
};
</script>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.chart-container {
  width: 100%;
  max-width: 900px;
  margin: auto;
}

form > div {
  display: flex;
  flex-direction: column;
}

button {
  margin-top: 1rem;
}
</style>
