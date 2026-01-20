const today = new Date();
const currentYear = today.getFullYear();
const currentMonth = String(today.getMonth() + 1).padStart(2, '0');
console.log(currentMonth)
console.log(today.getFullYear())
