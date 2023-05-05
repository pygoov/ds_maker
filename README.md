# ds_maker

Проект DatasetMaker для создания датасетов на базе интеграции с OpenAI

Телеграм бот, позваляющий перефразировать ваши предложения чтобы они подходили под определённые фразы.

## Запуск

1. устанoвите зависимости

> pip install -r requirements.txt

2. запустите скрипт

> python3 main.py --tg_token "<TELEGRAM_BOT_TOKEN>" --open_ai_token "<OPEN_AI_TOKEN>"

или

> python3 main.py -t "<TELEGRAM_BOT_TOKEN>" -o "<OPEN_AI_TOKEN>"  

где:

`TELEGRAM_BOT_TOKEN` - токен полученый из телеграм - создайте бота в телеграм и получите его токен в [BotFather](https://t.me/BotFather)

`OPEN_AI_TOKEN` - токен доступа к OpenAI


