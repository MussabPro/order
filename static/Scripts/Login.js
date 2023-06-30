function handleEnter(event, nextField) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById(nextField).focus();

    if (nextField === "submit") {
      document.getElementById("loginForm").submit();
    }
  }
}
function handlePasswordKeyDown(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("submitButton").click();
  }
}
