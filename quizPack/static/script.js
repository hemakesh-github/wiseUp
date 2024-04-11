// questions = {}
// keys = []
// let getQuestions = () => {
//     let topic = document.getElementById('topic').value;
//     const formData = new FormData();
//     const questions = document.querySelector('.t-container');
//     const choose = document.querySelector('.topic-container');
//     const str = window.location.href;
//     const lastSlashIndex = str.lastIndexOf('/');
//     const next = str.slice(0,lastSlashIndex + 1) + 'q';

//     formData.append('topic', topic)
//     console.log(formData)
//     fetch("/topicChoose", {
//         method: 'POST',
//         body: formData
//     }).then(response => {
//         return response.json()
//     }).then(questions => {
//         const keys = Object.keys(questions)
//         localStorage.setItem('myJsonData', JSON.stringify(questions));
//         // showQuestions(questions, keys)
//         window.location.href = next;
//     }).catch(error => {
//         console.log(error)
//     })
// }

// let showQuestions = () => {
//     q = document.querySelector('.quiz-question');
//     const qs = localStorage.getItem('myJsonData');
//     q.innerHTML = questions['question1'].question;
//     console.log(questions);
// }

// const t_btn = document.getElementById('topic-btn');
// t_btn.addEventListener('click', 
// (evt)=>{
//     evt.preventDefault()
//     console.log('clicked')
//     getQuestions()
//     // form.submit();
// })
// showQuestions(questions, keys);
