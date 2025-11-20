import importlib.util
import sys

def check_library(lib_name, pip_name=None):
    if pip_name is None:
        pip_name = lib_name
    
    if importlib.util.find_spec(lib_name) is not None:
        print(f"✅ {lib_name} установлена")
        return True
    else:
        print(f"❌ {lib_name} отсутствует")
        print(f"   Установите: pip install {pip_name}")
        return False

print("Проверка зависимостей NeuroChat...")
print("-" * 40)

# Проверяем основные библиотеки
libraries = [
    ("cryptography", "cryptography"),
]

all_ok = True
for lib_name, pip_name in libraries:
    if not check_library(lib_name, pip_name):
        all_ok = False

print("-" * 40)
if all_ok:
    print("✅ Все зависимости установлены! Можете запускать NeuroChat.")
else:
    print("❌ Некоторые зависимости отсутствуют. Установите их перед запуском.")

input("Нажмите Enter для выхода...")