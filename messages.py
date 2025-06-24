# Messages for the Telegram bot
UNKNOWN_COMMAND_TEXT = "❓ Я пока что не выучил такой команды. Напиши /start, чтобы вызвать главное меню"

MAIN_MENU_TEXT = """
Привет 👋
Распечатаю твои файлы в комнате <b>1708А</b> (2-я секция)
Пока что делаю только односторонню печать в ЧБ

{printer_status}

💵 ЧБ-печать: <b>20 коп/страница</b>

❓ Вопросы и предложения - @danila_okv
"""

# File processing messages
FILE_REQUEST_TEXT = "📂 Жду твой файл для печати. Просто отправь его мне"

FILE_REQUEST_TIMEOUT_TEXT = "⏳ Время вышло. Пришли файл ещё раз, если все еще хочешь напечатать"

FILE_PROCESSING_TEXT = "🔄 Файл <b>{file_name}</b> получил. Считаю страницы..."

FILE_PROCESSING_SUCCESS_TEXT = """
✅ Файл <b>{file_name}</b> обработан

📄 Страниц: <b>{page_count}</b>
💰 К оплате: <b>{price:.2f} BYN</b>

 ‼️ Напомню: печать одностронняя в ЧБ

Если все верно, <b>выбери способ оплаты:</b>
"""

FILE_PROCESSING_FAILURE_TEXT = "❌ Что-то пошло не так с файлом <b>{file_name}</b>. Попробуй ещё раз или пришли другой"

FILE_TYPE_ERROR_TEXT = "⚠️ Ух, пока что работаю только с .pdf и .docx"

# Payment messages
PAYMENT_CASH_TEXT = "💵 Плати наличкой в комнате 1708.\n\nПодтверждая печать, ты соглашаешься оплатить всю сумму"

PAYMENT_CARD_TEXT = """
💳 Переводи на карту через ЕРИП без комиссии

1. В приложении Банка выбери Система расчета (ЕРИП)
2. Банковские, финансовые и услуги
3. Альфа-Банк
4. Пополнение счета
5. Введи номер телефона: <code>375257270703</code> (нажми, чтобы скопировать)
"""

PAYMENT_TIMEOUT_TEXT = "⏳ Время на оплату вышло. Попробуй начать заново"

PAYMENT_SUCCESS_TEXT = "✅ Платёж получен. Запускаю печать..."

PAYMENT_FAILURE_TEXT = "❌ Платёж не найден. Проверь перевод и попробуй снова"

# Print messages
PRINT_START_TEXT = "🖨️ Печатаю <b>{file_name}</b>..."

PRINT_QUEUE_TEXT = "📑 Файл <b>{file_name}</b> поставлен в очередь. Жди - скоро распечатаю..."

PRINT_DONE_TEXT = """✅ Готово!\n Можешь забрать свой файл в комнате <b>1708А</b> (2-я секция)
Заходи без стука
"""

PRINT_CANCELLED_TEXT = "❌ Печать отменена. Если что-то не так, пиши в поддержку"

BUTTON_PRINT_FILE = "🖨️ Напечатать файл"

BUTTON_SUPPORT = "📞 По вопросам"

BUTTON_CONFIRM_PAYMENT = "✅ Я оплатил"

BUTTON_SETTINGS = "⚙️ Настройки"

BUTTON_CANCEL = "❌ Отмена"

BUTTON_METHOD_CASH = "💵 Наличные"

BUTTON_METHOD_CARD = "💳 Перевод"

BUTTON_PRINT_CONFIRM = "🖨️ Подтвердить"

BUTTON_MENU = "🏠 Главное меню"