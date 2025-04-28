import { createApp } from 'vue'; // Import only createApp
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';

// Flatpickr
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';

// Dayjs
import dayjs from 'dayjs';
import dayjsUtc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import advancedFormat from 'dayjs/plugin/advancedFormat';
import isBetween from 'dayjs/plugin/isBetween';
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';

// Extend dayjs with required plugins
dayjs.extend(dayjsUtc);
dayjs.extend(timezone);
dayjs.extend(advancedFormat);
dayjs.extend(isBetween);
dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);

// Create app instance and configure plugins
const app = createApp(App);

app.use(flatPickr); // Use the flatPickr plugin

import vSelect from 'vue-select';
app.component('vSelect', vSelect);
app.config.globalProperties.$dayjs = dayjs; // Set dayjs globally

app.mount('#app'); // Mount the app to the DOM
