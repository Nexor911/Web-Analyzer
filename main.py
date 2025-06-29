import requests

target = input("Введи url веб сайта: ")

try:
    response = requests.get(target)
    if response.status_code != 200:
        print(f"[!] Сервер вернул статус: {response.status_code}")
    else:
        for k, v in response.headers.items():
            print(f"{k}: {v}")
except Exception as e:
    print(f"{e}")
    exit()

security_headers_to_check = {
    "Strict-Transport-Security": "HSTS (HTTP Strict Transport Security) - Защищает от downgrade атак и cookie hijacking. Отсутствие - потенциальный риск.\n",
    "X-Content-Type-Options": "X-Content-Type-Options - Предотвращает MIME-sniffing. Должен быть 'nosniff'. Отсутствие - риск.\n",
    "X-Frame-Options": "X-Frame-Options - Защищает от Clickjacking. Должен быть 'DENY' или 'SAMEORIGIN'. Отсутствие - риск.\n",
    "Content-Security-Policy": "CSP (Content Security Policy) - Снижает риски XSS и других инъекций. Отсутствие/слабая политика - риск.\n",
    "Referrer-Policy": "Referrer-Policy - Контролирует отправку Referer заголовка. Отсутствие - потенциальная утечка информации.\n",
    "Permissions-Policy": "Permissions-Policy (ранее Feature-Policy) - Контролирует доступ к возможностям браузера. Отсутствие - потенциальный риск.\n",
}

found_security_headers = []
missing_security_headers = []

for expected_header, description in security_headers_to_check.items():
    if expected_header in response.headers:
        value = response.headers[expected_header]
        print(f"[+] Найден {expected_header}: {value}")
        found_security_headers.append((expected_header, value))
    else:
        print(f"[-] Отсутствует {expected_header}")
        missing_security_headers.append((expected_header, description))

fail = input("Сохранить итог в файл? (y/n): ").strip().lower()
if fail == 'y':
    menu = input("Введите имя файла: ")
    failname = f"{menu}.txt"
    with open(failname, "w", encoding="utf-8") as f:
        f.write(f"URL: {target}\n")
        f.write("Найденные заголовки безопасности:\n")
        for header, value in found_security_headers:
            f.write(f'    [+] {header}: {value}\n')
        f.write("\nОтсутствующие или слабые заголовки:\n")
        for header, description in missing_security_headers:
            f.write(f"    [-] {header}: {description}\n")
        print(f"Результаты сохранены в файл {failname}")
elif fail == 'n':
    print("\nНайденные заголовки безопасности\n")
    for header, value in found_security_headers:
        print(f'    [+] {header}: {value}')
    print("\nОтсутствующие или слабые заголовки:\n")
    for header, value in missing_security_headers:
        print(f'    [-] {header}: {value}')
else:
    print("Error")
