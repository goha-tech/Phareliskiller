import os
import sys
import time

def print_banner():
    print("\033[1;32m" + "=" * 40)
    print(" " * 10 + "🌟 PharelisKiller 🌟")
    print("=" * 40 + "\033[0m\n")
    time.sleep(0.5)

def main_menu():
    print("\033[1;34m" + "Меню:")
    print("1. 🔥 Ботнет Сносер")
    print("2. 💥 Сносер Сессий")
    print("3. ❌ Выход" + "\033[0m")
    print("\n" + "=" * 40)

def run_script(script_name):
    try:
        if os.path.exists(script_name):
            print(f"\nЗапуск {script_name}...")
            os.system(f"python {script_name}")
        else:
            print(f"\033[1;31m\n[Ошибка] Файл {script_name} не найден.\033[0m")
    except Exception as e:
        print(f"\033[1;31mОшибка при запуске {script_name}: {e}\033[0m")

def main():
    print_banner()
    while True:
        main_menu()
        choice = input("\033[1;33m\nВыберите действие: \033[0m")
        
        if choice == "1":
            run_script("Phareliskiller.py")
        elif choice == "2":
            run_script("sessionkiller.py")
        elif choice == "3":
            print("\n\033[1;35mВыход из программы...\033[0m")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print("\033[1;31m\nНеверный выбор, попробуйте снова.\033[0m")

if __name__ == "__main__":
    main()
