$(document).ready(function() {
  analyzeFrequencyChoicebox();
  $("#id_payment_frequency").change(analyzeFrequencyChoicebox);
});


function analyzeFrequencyChoicebox() {
  let combo = document.getElementById("id_payment_frequency");
  let saturdayCheckbox = document.getElementById("id_include_saturday");
  let sundayCheckbox = document.getElementById("id_include_sunday");
  if (combo.value == 4) {
    saturdayCheckbox.disabled = false;
    sundayCheckbox.disabled = false;
  } else {
    saturdayCheckbox.disabled = true;
    sundayCheckbox.disabled = true;
  }
};