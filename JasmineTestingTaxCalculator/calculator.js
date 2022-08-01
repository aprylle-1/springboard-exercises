window.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("calc-form");
  if (form) {
    setupIntialValues();
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      update();
    });
  }
});

function getCurrentUIValues() {
  return {
    amount: +(document.getElementById("loan-amount").value),
    years: +(document.getElementById("loan-years").value),
    rate: +(document.getElementById("loan-rate").value),
  }
}

// Get the inputs from the DOM.
// Put some default values in the inputs
// Call a function to calculate the current monthly payment
function setupIntialValues() {
  return getCurrentUIValues();
}

// Get the current values from the UI
// Update the monthly payment
function update() {
  let initialValues = setupIntialValues();
  let monthly = calculateMonthlyPayment(initialValues);
  updateMonthly(monthly);
}

// Given an object of values (a value has amount, years and rate ),
// calculate the monthly payment.  The output should be a string
// that always has 2 decimal places.
function calculateMonthlyPayment(values) {
    let P = values['amount'];
    let rate = values["rate"];
    let years = values["years"]
    if (P < 0 || years < 0 || rate < 0){
      throw new Error('Negative Input')
    }
    else if (!Number.isFinite(P) || !Number.isFinite(rate) || !Number.isFinite(years)){
      throw new Error ('Bad Input')
    }
    else{
      let i = (values['rate']/100)/12;
      let n = values["years"] * 12
      let monthly = ((P * i)/(1 - ((1 + i) ** -n))).toFixed(2);
      return monthly;
    }
}

// Given a string representing the monthly payment value,
// update the UI to show the value.
function updateMonthly(monthly) {
  let monthly_payment = document.getElementById("monthly-payment");
  monthly_payment.innerText = `$${monthly}`;
}

