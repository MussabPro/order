function changeText() {
  var textarea = document.getElementById("info");
  if (textarea.value == "") textarea.value = "Title :\nDescription :";
}

function updateCostAndServices() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  let totalCost = 0;
  const selectedServices = [];

  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      const service = checkbox.value;
      selectedServices.push(service);
      const rate = parseFloat(service.match(/\d+(\.\d+)?/)[0]);
      if (!isNaN(rate)) {
        totalCost += rate;
      }
    }
  });

  const costElement = document.getElementById("cost");

  costElement.textContent = "Cost : " + totalCost.toFixed(2) + "$/hr";
  document.getElementById("costInput").value = totalCost.toFixed(2);
  document.getElementById("selectedServicesInput").value =
    selectedServices.join(", ");
}

const checkboxes = document.querySelectorAll('input[type="checkbox"]');
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", updateCostAndServices);
});

// Set initial cost to zero
updateCostAndServices();

function validateServices(event) {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  let atLeastOneChecked = false;

  const form = document.querySelector("form");

  // Reset the 'is-invalid' class and 'required' message for all form elements
  const formElements = form.querySelectorAll("input, textarea");
  formElements.forEach((element) => {
    element.classList.remove("is-invalid");
  });
  const invalidFeedbacks = form.querySelectorAll(".invalid-feedback");
  invalidFeedbacks.forEach((feedback) => {
    feedback.style.display = "none";
  });

  // Add the 'is-invalid' class and show the 'required' message for required form elements without a value
  const requiredFields = form.querySelectorAll(
    "input:required, textarea:required"
  );
  requiredFields.forEach((field) => {
    if (!field.value) {
      field.classList.add("is-invalid");
    }
  });

  // Show the 'required' message for required form elements without a value
  requiredFields.forEach((field) => {
    if (!field.value) {
      const invalidFeedback = field.nextElementSibling;
      if (
        invalidFeedback &&
        invalidFeedback.classList.contains("invalid-feedback")
      ) {
        invalidFeedback.style.display = "block";
      }
    }
  });
  form.classList.add("was-validated");

  if (!form.checkValidity()) {
    event.preventDefault(); // Prevent form submission
    event.stopPropagation();
  }
  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      atLeastOneChecked = true;
      return;
    }
  });

  if (!atLeastOneChecked) {
    document.getElementById("serviceError").style.display = "block";
    event.preventDefault(); // Prevent form submission
    return false;
  }
}

const form = document.querySelector("form");
form.addEventListener("submit", validateServices);
const currentDate = new Date().toISOString().slice(0, 16);
document.getElementById("datec").min = currentDate;
