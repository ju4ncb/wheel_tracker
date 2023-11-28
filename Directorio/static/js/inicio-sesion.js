const passwordInput = document.getElementById("cont");

function passwordView() {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
    } else {
      passwordInput.type = "password";
    }
}