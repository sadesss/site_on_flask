document.addEventListener('DOMContentLoaded', function () {
    // Ваша логика получения имени пользователя

    // Отобразить всплывающее окно после загрузки страницы
    showPopup(username);

    // Скрыть всплывающее окно через несколько секунд
    setTimeout(function () {
        closePopup();
    }, 5000); // 5000 миллисекунд (5 секунд)
});

document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll(".response-btn");
  
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var meroText = button.getAttribute("data-mero");
        document.getElementById("mero-text").value = meroText;
      });
    });
  });
  

function showPopup(username) {
    var popup = document.getElementById("welcome-popup");
    var usernameSpan = document.getElementById("username");

    if (popup && usernameSpan) {
        usernameSpan.innerText = username;
        popup.style.display = "block";
    }
}

function closePopup() {
    var popup = document.getElementById("welcome-popup");
    if (popup) {
        popup.style.display = "none";
    }
}
