function validateForm(event) {
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

  // Validate order number range
  const orderNumberInput = form.querySelector("#Order_number");
  const orderNumber = parseInt(orderNumberInput.value);
  if (orderNumber < 1000 || orderNumber > 9999 || isNaN(orderNumber)) {
    orderNumberInput.classList.add("is-invalid");
    const invalidFeedback = orderNumberInput.nextElementSibling;
    if (
      invalidFeedback &&
      invalidFeedback.classList.contains("invalid-feedback")
    ) {
      event.preventDefault();
      invalidFeedback.style.display = "block";
    }
  }

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
}

let Error = document.getElementById("ErrorTrue").innerText;
if (Error) {
  document.getElementById("Error").style.display = "block";
  document.getElementById("form").style.display = "none";
}
