// Ждем, пока весь HTML-документ будет полностью загружен
document.addEventListener('DOMContentLoaded', function () {

    // Получение имени пользователя

    // Отобразить всплывающее окно после загрузки страницы
    // (замените 'username' на актуальное значение имени пользователя)
    showPopup(username);

    // Скрыть всплывающее окно через несколько секунд
    setTimeout(function () {
        closePopup();
    }, 5000); // 5 секунд

});

// Добавляем обработчик события "DOMContentLoaded" для выполнения кода после загрузки DOM
document.addEventListener("DOMContentLoaded", function () {

    // Находим все кнопки с классом "response-btn"
    var buttons = document.querySelectorAll(".response-btn");

    // Для каждой найденной кнопки добавляем обработчик события "click"
    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            // Получаем значение атрибута "data-mero" у нажатой кнопки
            var meroText = button.getAttribute("data-mero");

            // Устанавливаем значение текстового поля с id "mero-text" в значение "data-mero"
            document.getElementById("mero-text").value = meroText;
        });
    });

});

// Функция для отображения всплывающего окна с именем пользователя
function showPopup(username) {
    // Находим элементы всплывающего окна и span для имени пользователя
    var popup = document.getElementById("welcome-popup");
    var usernameSpan = document.getElementById("username");

    // Проверяем, что элементы существуют
    if (popup && usernameSpan) {
        // Устанавливаем текст в span для имени пользователя
        usernameSpan.innerText = username;
        // Показываем всплывающее окно
        popup.style.display = "block";
    }
}

// Функция для закрытия всплывающего окна
function closePopup() {
    // Находим элемент всплывающего окна
    var popup = document.getElementById("welcome-popup");

    // Проверяем, что элемент существует
    if (popup) {
        // Скрываем всплывающее окно
        popup.style.display = "none";
    }
}
