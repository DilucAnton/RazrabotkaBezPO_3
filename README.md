# RazrabotkaBezPO_3

Практика 3: Разработка безопасного программного обеспечения

Описание задания

Цель лабораторной работы – разработка переборщика паролей для формы аутентификации на уязвимом сайте DVWA (Damn Vulnerable Web Application). Также необходимо проанализировать исходный PHP-код и предложить решение для защиты от перебора паролей.

Задачи

Разработка переборщика паролей для формы в задании Brute Force на dvwa.local.
Анализ уязвимого PHP-кода:
Выявление слабых мест с использованием метрик CWE.
Реализация защищённой системы авторизации, которая исключает возможность подбора паролей.

Реализация

1. Переборщик паролей на Python
Описание: Программа использует GET-запросы с параметрами для перебора логинов и паролей. Для успешной работы необходимо указать действительные cookies, полученные из браузера.

Код в файле razbezpo3.py.
<img width="308" alt="Снимок экрана 2024-12-17 в 17 08 32" src="https://github.com/user-attachments/assets/19768ec1-8ab2-488c-9ea9-0ee0cc6980ee" />


2. Анализ уязвимого PHP-кода
Исходный код:

<?php

if( isset( $_GET\[ 'Login' \] ) ) {
	// Get username
	$user = $_GET\[ 'username' \];
	// Get password
	$pass = $_GET\[ 'password' \];
	$pass = md5( $pass );
	// Check the database
	$query  = "SELECT \* FROM \`users\` WHERE user = '$user' AND password = '$pass';";
	$result = mysqli_query($GLOBALS\["___mysqli_ston"\],  $query ) or die( '<pre>' . ((is_object($GLOBALS\["___mysqli_ston"\])) ? mysqli_error($GLOBALS\["___mysqli_ston"\]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
	if( $result && mysqli_num_rows( $result ) == 1 ) {
		// Get users details
		$row    = mysqli_fetch_assoc( $result );
		$avatar = $row\["avatar"\];
		// Login successful
		$html .= "<p>Welcome to the password protected area {$user}</p>";
		$html .= "<img src=\\"{$avatar}\\" />";
	}
	else {
		// Login failed
		$html .= "<pre><br />Username and/or password incorrect.</pre>";
	}
	((is_null($___mysqli_res = mysqli_close($GLOBALS\["___mysqli_ston"\]))) ? false : $___mysqli_res);
}
?>


Выявленные уязвимости и CWE:

SQL-инъекция (CWE-89):
Ввод пользователя напрямую используется в SQL-запросе.
Решение: Использовать подготовленные запросы (prepared statements).
Слабый хэш пароля (CWE-327):
Используется устаревший MD5, который легко взломать.
Решение: Использовать bcrypt или password_hash().
Отсутствие защиты от перебора паролей (CWE-307):
Не ограничено количество попыток входа.
Решение:
Ввести блокировку после нескольких неудачных попыток.
Использовать задержки между попытками.
Внедрить CAPTCHA.


3. Исправленный PHP-код с защитой

<?php
session_start();
require_once 'db.php'; // Подключение к БД

if (isset($_GET['Login'])) {
    $username = $_GET['username'];
    $password = $_GET['password'];

    // Лимит попыток
    if (!isset($_SESSION['attempts'])) $_SESSION['attempts'] = 0;
    if ($_SESSION['attempts'] >= 5) die("Too many attempts. Try again later.");

    // Подготовленный запрос
    $stmt = $mysqli->prepare("SELECT * FROM users WHERE user = ? AND password = ?");
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);
    $stmt->bind_param("ss", $username, $hashed_password);
    $stmt->execute();

    $result = $stmt->get_result();
    if ($result->num_rows === 1) {
        $_SESSION['attempts'] = 0;
        echo "Welcome, {$username}!";
    } else {
        $_SESSION['attempts']++;
        echo "Username and/or password incorrect.";
    }
}
?>


Вывод

Перебор паролей успешно реализован.
Проведён анализ уязвимого PHP-кода и указаны слабые места с CWE-метриками.
Разработана безопасная версия авторизации с защитой от SQL-инъекций и перебора паролей.
