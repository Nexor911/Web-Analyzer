import requests
import random

proxy = {
    "http": "http://96.70.186.221:80",
    "https": "https://194.186.248.97:80"
}

user_agent = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.1; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; JAT-LX1 Build/HONORJAT-LX1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36 GoNativeAndroid/1.0 gonative",
    "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36"
]

headers = {
    "User-Agent": random.choice(user_agent)
}
print(f"Используетя User-Agent: {headers['User-Agent']}")

target = input("Введи url веб сайта: ")

try:
    response = requests.get(target, allow_redirects=True, headers=headers, proxies=proxy)
    if response.history:
        print("\n[!] Обнаружены редиректы:")
        for idx, resp in enumerate(response.history):
            loc = resp.headers.get("Location", "<не указан>")
            print(f"  {idx + 1}) {resp.status_code} → {loc}")
        print(f"[+] Финальный URL: {response.url}")
    else:
        print("[+] Редиректов не было. Финальный URL:", response.url)
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
