import re
import os
import json
import asyncio
import logging
from telethon import TelegramClient, functions, types
from telethon.errors import SessionPasswordNeededError
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

logging.basicConfig(level=logging.ERROR) 
logger = logging.getLogger('telethon')
logger.setLevel(logging.ERROR)  

session_dir = 'sessions'
config_file = 'config.json'  

def create_config_file(file_path=config_file, default_data=None):
    if not os.path.exists(file_path):
        if default_data is None:
            default_data = {}
        with open(file_path, 'w') as json_file:
            json.dump(default_data, json_file, indent=4)
            os.chmod(file_path, 0o777)
        print(f"Файл '{file_path}' был создан.")
    else:
        print(f"Файл '{file_path}' уже существует.")

create_config_file()

def load_config():
    if not os.path.exists(config_file):
        console.print("[yellow]Файл конфигурации не найден, делаем новый.[/yellow]")
        return {}
    with open(config_file, 'r') as f:
        return json.load(f)

def save_config(api_id, api_hash):
    config = {
        'api_id': api_id,
        'api_hash': api_hash
    }
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4) 
    console.print("[blue]Конфиг успешно сохранен.[/blue]")

config = load_config()
api_id = config.get('api_id')
api_hash = config.get('api_hash')

report_reasons = {
    '1': types.InputReportReasonSpam(),
    '2': types.InputReportReasonViolence(),
    '3': types.InputReportReasonPornography(),
    '4': types.InputReportReasonCopyright()
}

console = Console()

def create_sessions_dir():
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)  
        os.chmod(session_dir, 0o777)  
        print(f"Папка '{session_dir}' была успешно создана с правами 777.")
    else:
        print(f"Папка '{session_dir}' уже существует.")

def load_sessions():
    sessions = {}
    for filename in os.listdir(session_dir):
        if filename.endswith(".session"):
            sessions[filename[:-8]] = os.path.join(session_dir, filename)
    return sessions

def display_banner():
    banner = """
⠄⠄⠄⠄⠄⠄⠄⠄⣀⣠⣤⣤⣤⣄⡀⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⣠⣿⣿⣿⡿⣿⡿⣗⢌⢳⡀⠄⠄⠄
⠄⠄⠄⠄⠄⣼⣿⡇⣿⠹⡸⡹⣷⡹⡎⣧⢳⠄⠄⠄
⠄⠄⠄⠄⠄⣿⣿⠱⡙⠰⣢⡱⢹⡇⡷⢸⢸⠄⠄⠄
⠄⠄⠄⠄⠄⢿⢸⡈⣉⣤⠠⣴⡄⡇⠁⠄⢸⠄⠄⠄
⠄⠄⠄⠄⠄⠸⡆⡃⡙⢍⣹⡿⢓⠄⠤⣐⡟⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠙⠾⠾⠮⢵⢸⡔⢷⣍⠉⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢀⣴⣾⣿⣷⡶⡋⢞⣎⣚⣭⣴⣶⣶⣤⡀
⠄⠄⠄⠄⢘⣛⣩⣾⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷
⠄⠄⣀⠺⣿⣿⣿⠟⣡⣾⠿⢿⣿⣿⡎⢋⠻⣿⣿⣿
⠄⠄⣉⣠⣿⣿⡏⣼⣿⠁⠶⠄⣿⣿⡇⡼⠄⠈⠛⢿
⠄⠄⣈⠻⠿⠟⢁⠘⢿⣷⣶⣾⣿⠟⡰⠃⠄⠄⠄⠄
⠄⣴⣿⣧⢻⣿⣿⣷⣦⣬⣉⣩⣴⠞⠁⠄⠄⠄⠄⠄
⠄⠘⠿⠿⢸⣿⢸⣿⣿⣿⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄
⠄⢤⡝⣧⠘⣿⢸⣿⡿⢻⣿⡿⠄⠄⠄⠄⠄⠄⠄⠄
⣜⢧⠻⣰⢇⣸⢠⣿⡅⣿⠏⣴⣧⡀⠄⠄⠄⠄⠄⠄
⠹⠢⢾⣿⣸⣿⣿⣿⢡⡏⣸⣿⣿⣷⠄⠄⠄⠄⠄⠄
⠄⣷⣦⡉⠛⠻⠿⠿⠾⠿⠿⠿⠿⠛⠋⠄⠄⠄⠄⠄
⢸⣿⣿⣿⣦⡀⠄⠄⠄⢀⣤⣶⣾⣿⣿⡆⠄⠄⠄⠄
⢸⣿⣿⣿⣿⣿⣄⠄⣾⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄
⠸⣿⣿⣿⣿⣿⣿⠄⢿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄
⠄⣿⣿⣿⣿⣿⣿⠄⠈⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄
⠄⢹⣿⣿⣿⣿⡟⠄⠄⠹⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄
    """
    console.print(banner)
    console.print("[bold green]Script made by tg @fckPharelis. Before use, enter the API ID and API HASH[/bold green]")

def input_api_credentials():
    api_id = Prompt.ask("[yellow]Введите API ID:[/yellow]")
    api_hash = Prompt.ask("[yellow]Введите API HASH:[/yellow]")
    save_config(api_id, api_hash)

async def add_session(phone):
    sessions = load_sessions()
    
    if phone in sessions:
        console.print(f"[yellow]Сессия для {phone} уже существует.[/yellow]")
        return
    
    client = TelegramClient(os.path.join(session_dir, phone), api_id, api_hash)
    
    console.print("[cyan]Подключение к Telegram...[/cyan]")
    await client.start()

    try:
        if not await client.is_user_authorized():
            console.print(f"[cyan]Отправка кода на {phone}...[/cyan]")
            await client.send_code_request(phone)
            code = Prompt.ask(f"Введите код для {phone}")

            await client.sign_in(phone=phone, code=code)

            if await client.is_user_authorized():
                console.print(f"[green]Успешно авторизован: {phone}[/green]")
            else:
                console.print(f"[red]Не удалось авторизоваться для {phone}[/red]")
    
    except SessionPasswordNeededError:
        password = Prompt.ask("Введите двухфакторный пароль")
        await client.sign_in(password=password)
       
        if await client.is_user_authorized():
            console.print(f"[green]Успешно авторизован: {phone}[/green]")

    await client.disconnect()

async def send_complaint(client, chat_id, message_id, reason):
    try:
        result = await client(functions.messages.ReportRequest(
            peer=chat_id,
            id=[message_id],
            reason=reason,
            message='Отправка жалобы через скрипт'
        ))
        console.print(f"[green]Жалоба отправлена на сообщение {message_id} в чате {chat_id}[/green]")
    except Exception as e:
        console.print(f"[red]Ошибка при отправке жалобы: {e}[/red]")

async def attack(message_url):
    sessions = load_sessions()
    
    if not sessions:
        console.print("[red]Нет активных сессий.[/red]")
        return

    match = re.match(r'https://t\.me/(\w+)/(\d+)', message_url)
    if not match:
        console.print("[red]Некорректная ссылка на сообщение.[/red]")
        return
    
    chat_id, message_id = match.groups()
    
    console.print("[cyan]Выберите причину для жалобы:[/cyan]")
    console.print("1: Спам\n2: Насилие\n3: Порнография\n4: Нарушение авторских прав")
    reason_choice = Prompt.ask("[yellow]Введите номер причины:[/yellow]")
    reason = report_reasons.get(reason_choice)
    
    if not reason:
        console.print("[red]Неверный выбор причины.[/red]")
        return

    with Progress() as progress:
        task = progress.add_task("[green]Отправка жалоб...", total=len(sessions))
        
        for phone, session_path in sessions.items():
            client = TelegramClient(session_path, api_id, api_hash)
            await client.start()

            console.print(f"[blue]Отправка жалобы через {phone}...[/blue]")
            await send_complaint(client, chat_id, int(message_id), reason)
            await client.disconnect()
            
            progress.update(task, advance=1)

def view_active_sessions():
    sessions = load_sessions()
    if not sessions:
        console.print("[red]Нет активных сессий.[/red]")
    else:
        console.print("[cyan]Активные сессии:[/cyan]")
        for phone in sessions.keys():
            console.print(f"[blue]{phone}[/blue]")

async def main():
    display_banner()
    
    global api_id, api_hash
    config = load_config()  
    api_id = config.get('api_id')
    api_hash = config.get('api_hash')

    if not api_id or not api_hash:
        console.print("[red]API ID или API HASH не найдены. Пожалуйста, введите их. что это ? https://teletype.in/@sakurahost/GetApi[/red]")
        input_api_credentials()  
        config = load_config()  
        api_id = config.get('api_id')
        api_hash = config.get('api_hash')

    while True:
        console.print("\n[bold cyan]Выберите действие:[/bold cyan]")
        console.print("0: Изменить API ID и API HASH")
        console.print("1: Добавить сессию")
        console.print("2: Атака (сносим нахуй)")
        console.print("3: Просмотреть активные сессии")
        console.print("4: Выход")
        
        choice = Prompt.ask("[yellow]Введите номер действия:[/yellow]")
        
        if choice == '0': 
            input_api_credentials()
        elif choice == '1':  
            phone = Prompt.ask("[yellow]Введите номер телефона (в формате +12345678901):[/yellow]")
            await add_session(phone)
        elif choice == '2':
            message_url = Prompt.ask("[yellow]Введите ссылку на сообщение (https://t.me/username/message_id):[/yellow]")
            await attack(message_url)
        elif choice == '3':
            view_active_sessions()
        elif choice == '4':
            console.print("[green]Завершение программы.[/green]")
            break
        else:
            console.print("[red]Неверный выбор. Попробуйте снова.[/red]")

if __name__ == '__main__':
    create_sessions_dir()
    asyncio.run(main())