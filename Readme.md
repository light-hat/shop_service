# Сервис магазинов

## API

![Swagger](assets/swagger.png)

API задокументирован при помощи Swagger `drf-spectacular`.

Тестирование API: `http://127.0.0.1/swagger/`

Документация: `http://127.0.0.1/redoc`

JSON: `http://127.0.0.1/.../`

## База данных

![ERD](assets/database.png)

Связи между сущностями:

- Улица к городу: `многие к одному`;

- Магазин к улице: `многие к одному`;

- Магазин к городу: `многие к одному`.

СУБД: `PostgreSQL 15 версии`.

ORM: `Django ORM`.

## Админка Django

Админка Django доступна по адресу `http://127.0.0.1/admin`

## Конфигурирование



## Деплой

Для начала клонируйте репозиторий:

```bash
git clone https://github.com/light-hat/shop_service
cd shop_service
```

Далее предлагается два варианта на выбор:

### 1. Docker

> [!IMPORTANT]  
> В системе должен быть установлен Docker и Docker Compose.

```bash
docker-compose up -d --build
```

### 2. Vagrant

> [!IMPORTANT]  
> Должен быть установлен Vagrant и VirtualBox.

> [!TIP]
> Базовый box можно скачать [отсюда](https://portal.cloud.hashicorp.com/vagrant/discover/ubuntu/focal64).

```bash
vagrant up
```

> [!NOTE]  
> Сервис в обоих случаях будет доступен на `127.0.0.1:80`.

## Управление проектом через Make

Для автоматизации работы с docker-compose предлагается использование утилиты Make.

- Сборка и запуск стека приложений:

```bash
make build
```

- Запуск ранее собранного стека приложений:

```bash
make up
```

- Остановка стека приложений:

```bash
make down
```

- Перестроить стек приложений с удалением всех контейнеров и томов:

```bash
make rebuild
```

- Очистить все контейнеры, сети и тома:

```bash
make clean
```

- Вывести логи:

```bash
make logs
```
