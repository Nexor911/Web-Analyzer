import requests


target = input("Введит url веб сайта: ")

try:
    response = requests.get(target)
    if response.status_code == 200:
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        else:
            print(f"{response.status_code}: {response.text}")
except Exception as e:
    exit()

security_headers_to_check = {
    "Strict-Transport-Security": "HSTS (HTTP Strict Transport Security) - Защищает от downgrade атак и cookie hijacking. Отсутствие - потенциальный риск.",
    "X-Content-Type-Options": "X-Content-Type-Options - Предотвращает MIME-sniffing. Должен быть 'nosniff'. Отсутствие - риск.",
    "X-Frame-Options": "X-Frame-Options - Защищает от Clickjacking. Должен быть 'DENY' или 'SAMEORIGIN'. Отсутствие - риск.",
    "Content-Security-Policy": "CSP (Content Security Policy) - Снижает риски XSS и других инъекций. Отсутствие/слабая политика - риск.",
    "Referrer-Policy": "Referrer-Policy - Контролирует отправку Referer заголовка. Отсутствие - потенциальная утечка информации.",
    "Permissions-Policy": "Permissions-Policy (ранее Feature-Policy) - Контролирует доступ к возможностям браузера. Отсутствие - потенциальный риск.",
}

found_security_headers = []
missing_security_headers = []

for expected_header, description in security_headers_to_check.items():
    if expected_header in response.headers:
        print(f"[+] Найден {expected_header}: {response.headers[expected_header]} - {description.split(' - ')[0]}")
        found_security_headers.append(expected_header)
    else:
        missing_security_headers.append((expected_header, description))

if not missing_security_headers:
    print("Все основные заголовки безопасности присутствуют.")
else:
    print("\n[-] Внимание: Отсутствуют или не настроены следующие заголовки безопасности:")
    for header, description in missing_security_headers:
        print(f"    - {header}: {description}")
