export const isValidInputValue = (value, checks = [null, undefined, '']) => {
    return !checks.includes(value);
  };
  
  export const removeNullValues = (obj) => {
    for (var prop in obj) {
      if (
        typeof obj[prop] === 'object' &&
        !Array.isArray(obj[prop]) &&
        obj[prop] !== null
      ) {
        removeNullValues(obj[prop]);
      } else if (!isValidInputValue(obj[prop])) {
        delete obj[prop];
      }
    }
  
    return obj;
  };

  export const formatAmount = (amount) => {
    if (!isValidInputValue(amount)) return null;
  
    return Number(amount).toLocaleString('en-US', {
      style: 'currency',
    });
  };

  export const commaSeparatedValue = (value) => {
    return (value || '').toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  };