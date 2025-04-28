<template>
  <div>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

// Register the required Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: 'SalesStackedBarChart',
  components: {
    Bar,
  },
  props: {
    salesData: {
      type: Object,
      required: true,
    },
    companyName: {
      type: String,
      required: true,
    },
    denomination: {
      type: String,
      default: '$',
    },
  },
  data() {
    return {
      // Initial state for chartData
      chartData: {
        labels: [],
        datasets: [],
      },
    };
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: this.companyName, // Title text at the top of the chart
            font: {
              size: 20, // You can adjust the font size here
              weight: 'bold', // Bold text
            },
            padding: {
              top: 10, // Space between the title and the chart
              bottom: 20, // Space between the title and the chart
            },
          },
          tooltip: {
            callbacks: {
              // Custom tooltip callback to display additional details
              label: (tooltipItem) => {
                const index = tooltipItem.dataIndex;
                const month = this.chartData.labels[index];
                const label = tooltipItem.dataset.label;
                const amount = tooltipItem.raw;

                // Format the amount with commas and add $ sign
                const formattedAmount = `${this.denomination}${new Intl.NumberFormat().format(
                  amount.toFixed(2)
                )}`;

                // Find the sale details matching the amount
                const details = this.salesData[month]?.[label]?.find(
                  (item) => item.Amount === amount
                );

                // Check if details is valid and return the tooltip text
                if (details) {
                  return `${label}: ${formattedAmount} ${details.Currency} - ${details.Customer}, ${details.Location}`;
                } else {
                  return `${label}: ${formattedAmount}`;
                }
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              // Format the y-axis labels with the $ sign and commas
              callback: (value) => {
                return `${this.denomination}${new Intl.NumberFormat().format(value.toFixed(2))}`; // Format with commas and $
              },
            },
          },
          x: {
            stacked: false,
          },
        },
      };
    },
  },
  watch: {
    salesData: {
      deep: true,
      handler(newData) {
        this.updateChartData(newData);
      },
    },
  },
  methods: {
    updateChartData(data) {
      // Prepare the chart data using the salesData prop
      const months = Object.keys(data);
      const hatSales = months.map((month) =>
        (data[month]['Hat Sales'] || []).reduce(
          (acc, sale) => acc + sale.Amount,
          0
        )
      );
      const tShirtSales = months.map((month) =>
        (data[month]['T-Shirt Sales'] || []).reduce(
          (acc, sale) => acc + sale.Amount,
          0
        )
      );

      this.chartData = {
        labels: months, // The x-axis labels (Months)
        datasets: [
          {
            label: 'Hat Sales',
            data: hatSales, // Data for Hat Sales
            backgroundColor: 'rgba(255, 99, 132, 0.6)', // Color for Hat Sales
            barPercentage: 0.4, // Set the bar width to 40% of the space
            categoryPercentage: 0.5, // Center the bars within their categories
          },
          {
            label: 'T-Shirt Sales',
            data: tShirtSales, // Data for T-Shirt Sales
            backgroundColor: 'rgba(54, 162, 235, 0.6)', // Color for T-Shirt Sales
            barPercentage: 0.4, // Set the bar width to 40% of the space
            categoryPercentage: 0.5, // Center the bars within their categories
          },
        ],
      };
    },
  },
  created() {
    // Initial chart data setup when component is created
    this.updateChartData(this.salesData);
  },
};
</script>

<style scoped>
/* Optionally add some styles for your chart */
</style>
