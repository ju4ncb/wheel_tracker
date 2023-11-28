const li_contacto = document.getElementById('li_contacto');
const passwordInput = document.getElementById("cont");

if (li_contacto != null){
    li_contacto.addEventListener('click', scrollToBottom)
}

function passwordView() {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
    } else {
      passwordInput.type = "password";
    }
}

function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}
