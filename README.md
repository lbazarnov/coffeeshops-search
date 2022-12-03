# Coffeeshops Search

## Установка и запуск скрипта

Для запуска скрипта необходимо установить poetry и python версии не ниже 3.8, а также [получить](https://yandex.ru/dev/maps/jsapi/doc/2.1/quick-start/index.html#get-api-key) ключ API Яндекс.Карт.

После этого необходимо:

1. Склонировать репозиторий к себе на компьютер

    ```bash
    $ git clone https://github.com/lbazarnov/coffeeshops-search.git
    ```

2. Создать файл для переменных окружения `.env`, поместив туда ваш ключ API Яндекс.Карт

    ```bash
    $ сd coffeeshops-search
    $ touch .env
    $ echo 'APIKEY=вставьте_ваш_ключ_сюда' > .env
    ```

3. Последовательно запустить несколько команд

    ```bash
    $ make install # Для установки зависимостей проекта
    $ make build # Для сборки проекта
    $ make package-install # Для установки скрипта на компьютер
    ```

4. Запустить скрипт командой

    ```bash
    $ coffeeshops-search
    ```
