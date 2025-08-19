// static/js/modal.js
function openModal(postId) {
    var modal = document.getElementById("myModal-" + postId);
    modal.style.display = "block";
}

function closeModal(postId) {
    var modal = document.getElementById("myModal-" + postId);
    modal.style.display = "none";
}

// Закрываем модальное окно при клике вне окна
window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
}