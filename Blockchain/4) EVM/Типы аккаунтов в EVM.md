---
title: Типы аккаунтов в EVM
tags: [EVM, Ethereum, Аккаунты]
---

## Короткий ответ

В EVM есть два типа аккаунтов: **Externally Owned Accounts (EOA)**, управляемые пользователями через приватные ключи, и **Contract Accounts**, содержащие смарт-контракты и управляемые кодом.

![[Pasted image 20241213172907.png]]

## Подробный разбор

### EOA (Externally Owned Account)

* Контролируется приватным ключом пользователя.
* Может инициировать транзакции.
* Не может хранить код.
* Nonce - счетчик транзакций.

### Contract Account (Смарт-контракт)

* Контролируется кодом контракта.
* Может инициировать транзакции.
* Хранит код.
* Nonce - счетчик созданных контрактов.

### Общие характеристики аккаунтов

* **Address:** Уникальный 20-байтовый идентификатор.
* **Balance:** Количество Ether (ETH).


## Связанные темы

* [Вернуться к списку вопросов](4.%20Список%20вопросов.md)
* [[Что такое EOA? Имеет ли он приватный ключ? Может ли хранить произвольные данные ? Может ли хранить код? Кто контролирует аккаунт?]]
* [[Что такое SmartContract? Может ли иметь приватный ключ? Может ли хранить произвольные данные ? Может ли хранить код? Кто контролирует аккаунт?]]


## Источники

* [Ethereum Documentation - Accounts](https://ethereum.org/en/developers/docs/accounts/)


---