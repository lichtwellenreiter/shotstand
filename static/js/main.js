/**
 * Set the Date in the search Input for today, but not greater than today
 */

let datebox = document.getElementById("date");
let today = new Date();
let dd = String(today.getDate()).padStart(2, '0');
let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
let yyyy = today.getFullYear();
today = yyyy + '-' + mm + '-' + dd;


datebox.setAttribute('max', today);
datebox.setAttribute('value', today);