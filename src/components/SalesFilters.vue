<template>
  <div class="filters">
    <div class="card w-100 m-5 p-3">
      <div class="card-header bg-gray">
        <h2 class="text-dark">Chart Filters</h2>
      </div>
      <div class="card-body">
        <div class="d-flex gap-4 mb-3 align-items-md-baseline">
        <h6 class="text-gray">Select Fiscal Period</h6>
        <select
          v-model="filters.period"
          id="fiscalYearSelect"
          class="form-select w-25"
        >
          <option value="" selected>YTD F2024</option>
          <option v-for="period in fiscalPeriod" :key="period" :value="period">
            {{ period }}
          </option>
        </select>
        </div>
        <form @submit.prevent="applyFilters" class="d-flex flex-wrap gap-4">
          <div class="d-flex flex-column">
            <flatPickr
              v-model="selectedDateRange"
              :config="configDateFlatPickr"
              placeholder="Date"
              class="form-control"
            />
          </div>

          <!-- Customer Select Dropdown -->
          <div class="d-flex flex-column">
            <select
              v-model="filters.customer"
              id="customerSelect"
              class="form-select"
            >
              <option value="" selected>Select Customer</option>
              <option
                v-for="customer in customerOptions"
                :key="customer"
                :value="customer"
              >
                {{ customer }}
              </option>
            </select>
          </div>

          <!-- Currency Select Dropdown -->
          <div class="d-flex flex-column">
            <select
              v-model="filters.currency"
              id="currencySelect"
              class="form-select"
            >
              <option value="" selected>Select Currency</option>
              <option
                v-for="currency in currencyOptions"
                :key="currency"
                :value="currency"
              >
                {{ currency }}
              </option>
            </select>
          </div>

          <!-- Location Select Dropdown -->
          <div class="d-flex flex-column">
            <select
              v-model="filters.location"
              id="locationSelect"
              class="form-select"
            >
              <option value="" selected>Select Location</option>
              <option
                v-for="location in locationOptions"
                :key="location"
                :value="location"
              >
                {{ location }}
              </option>
            </select>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import flatPickr from 'vue-flatpickr-component';
import { removeNullValues } from '@/helpers/helper';

export default {
  name: 'SalesFilters',
  props: {
    customerOptions: {
      type: Array,
      required: true,
    },
    currencyOptions: {
      type: Array,
      required: true,
    },
    locationOptions: {
      type: Array,
      required: true,
    },
  },
  components: {
    flatPickr,
  },
  data() {
    return {
      configDateFlatPickr: {
        enableTime: false,
        mode: 'range',
      },
      selectedDateRange: '',
      filters: {
        startDate: '',
        endDate: '',
        customer: '',
        currency: '',
        location: '',
        period: '',
      }, // Example locations
      fiscalPeriod: ['F2022', 'F2023', 'LTM Dec 2023'],
    };
  },
  watch: {
    filters: {
      deep: true,
      handler(newFilters) {
        const updatedFilters = structuredClone(newFilters);
        this.$emit('update-filters', removeNullValues(updatedFilters));
      },
    },
    selectedDateRange: {
      immediate: true,
      handler (newSelectedDateRange) {
        if(!newSelectedDateRange) {
            this.filters.startDate = ''
            this.filters.endDate = ''
            return;
        }
        const dates = newSelectedDateRange.split(' to ')

        if (dates.length <= 1) return

        this.filters = {
            ...this.filters,
            startDate: dates[0],
            endDate: dates[1],
        }
      }
    }
  }
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
