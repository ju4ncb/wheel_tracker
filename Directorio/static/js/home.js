const li_contacto = document.getElementById('li_contacto');
if (li_contacto != null){
    li_contacto.addEventListener('click', scrollToBottom)
}

function scrollToBottom() {
    console.log('waos')
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

(function(){
    const titleQuestions = [...document.querySelectorAll('.questions__title')];
    console.log(titleQuestions)

    titleQuestions.forEach(question =>{
        question.addEventListener('click', ()=>{
            let height = 0;
            let answer = question.nextElementSibling;
            let addPadding = question.parentElement.parentElement;

            addPadding.classList.toggle('questions__padding--add');
            question.children[0].classList.toggle('questions__arrow--rotate');

            if(answer.clientHeight === 0){
                height = answer.scrollHeight;
            }

            answer.style.height = `${height}px`;
        });
    });
})();