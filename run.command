# Переход в директорию скрипта (где лежит и venv, и main.py)
cd "$(dirname "$0")"

# Активируем виртуальное окружение
source ./venv/bin/activate

# Запускаем бота
python main.py