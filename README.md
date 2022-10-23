# Transacion API

## Модель базы данных

- Пользователь – репрезентация пользователей в приложении. Есть обычные и админ пользователи (админ назначается руками в базе или создаётся на старте приложения).

- Товар – Состоит из заголовка, описания и цены.

- Счёт – Имеет идентификатор счёта и баланс. Привязан к пользователю. У пользователя может быть несколько счетов.

- Транзакция – история зачисления на счёт, хранит сумму зачисления и идентификатор счёта.

## Функциональные критерии

Весь описываемый ниже функционал осуществлён в формате REST API. Работа с шаблонами, HTML или фронтендом в любой форме не предусматривается.

Пользователю доступны следующие действия:

1. Регистрация по паролю и логину (возврат ссылки активации не реализован).
2. Логин.
3. Просмотр списка товаров.
4. Покупка товара, с баланса списывается стоимость товара, при условии наличия на балансе счёта достаточного количества средств.
5. Просмотр баланса всех принадлежащих пользователю счетов и истории его транзакций.
6. Зачисление средств на счёт, выполняется с помощью эндпоинта ```POST /payment/webhook```, симулирует начисление со стороннего сервиса.

Пример тела вебхука, с транзакцией (формат json):

```
{
    "signature": "f4eae5b2881d8b6a1455f62502d08b2258d80084",
    "transaction_id": 1234567,
    "user_id": 123456,
    "bill_id": 123456,
    "amount": 100
}
```

Сигнатура формируются по правилу:

```
from Crypto.Hash import SHA1

hasher = SHA1.new()
hasher.update(f'{private_key}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode(encoding='utf-8'))
hexdigest = hasher.hexdigest()
```

Где:
- private_key – приватный ключ, задаётся в свойствах приложения;
- transaction_id – уникальный идентификатор транзакции:
- user_id – пользователь на чеё счёт произойдёт зачисление;
- bill_id – идентификатор счёта (по умолчанию принимается, что соответствующий счет существует и принадлежит пользователю с переданным user_id);
- amount – сумма транзакции.
 
### Возможности админа (реализовано через Django Admin Site):

1. Видеть все товары.
2. Видеть всех пользователей и их счета.
3. Включать/отключать пользователей.
4. Создавать/редактировать/удалять товары.
 
### Не функциональные критерии

1. Логины пользователей уникальны.
2. После регистрации пользователь создаётся в не активном состоянии. Становится активным, переходя по ссылке, полученной после регистрации (не реализовано).
3. Авторизация должна быть сделана через JWT. Защищённые эндпоинты должны получать токен в заголовке Authorization в Bearer формате.
