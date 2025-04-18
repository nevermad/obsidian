---
title: Почему Nonce увеличивается после каждой транзакции?
tags: [EVM, Ethereum, Аккаунты, Nonce, Транзакции, Безопасность]
---

## Короткий ответ

Nonce увеличивается после каждой транзакции для предотвращения повторного использования транзакций (replay-атак) и обеспечения порядка выполнения транзакций от одного отправителя.


## Подробный разбор


Как было описано в заметке [[Что такое Nonce в состоянии аккаунта?]], nonce - это счетчик транзакций, связанный с каждым аккаунтом. Увеличение nonce после каждой транзакции выполняет две важные функции:

**1. Предотвращение Replay-атак:**

Если nonce не увеличивался бы, злоумышленник мог бы перехватить валидную транзакцию и повторно отправить ее в сеть.  Поскольку все параметры транзакции (кроме nonce) остаются неизменными,  она была бы выполнена повторно, что привело бы к нежелательным последствиям, например, двойному списанию средств.

Увеличение nonce делает каждую транзакцию уникальной.  Повторная отправка транзакции с уже использованным nonce будет отклонена сетью как невалидная.

**2. Гарантия порядка транзакций:**

Nonce обеспечивает правильный порядок обработки транзакций от одного отправителя.  Если пользователь отправляет несколько транзакций одновременно,  сеть может получить их в разном порядке. Nonce позволяет определить корректную последовательность выполнения,  гарантируя, что транзакции будут выполнены в том порядке, в котором они были созданы отправителем.

Сеть Ethereum отслеживает использованные nonce через **состояние аккаунта (account state)**.  Каждый аккаунт в Ethereum (как EOA - Externally Owned Account, так и контракт) имеет связанное с ним состояние, которое хранится в базе данных состояния Ethereum.  Это состояние включает в себя различную информацию, включая:

* **Nonce:** Текущий nonce аккаунта.
* **Balance:** Баланс ETH аккаунта.
* **CodeHash:** (только для контрактов) Хеш кода контракта.
* **StorageRoot:** (только для контрактов) Хеш корня дерева Merkle, представляющего состояние хранилища контракта.


**Процесс проверки nonce:**

1. **Получение транзакции:** Когда узел Ethereum получает новую транзакцию, он сначала проверяет ее подпись, чтобы убедиться, что она была отправлена владельцем соответствующего аккаунта.

2. **Загрузка состояния аккаунта:**  Затем узел загружает состояние аккаунта отправителя из базы данных состояния.  Это включает в себя текущий nonce аккаунта.

3. **Сравнение nonce:** Узел сравнивает nonce, указанный в транзакции, с текущим nonce аккаунта, хранящимся в состоянии.

    * **Если nonce в транзакции равен текущему nonce аккаунта:** Транзакция считается валидной и добавляется в mempool (пул ожидающих транзакций).  После включения транзакции в блок,  nonce аккаунта в состоянии **увеличивается на 1**.

    * **Если nonce в транзакции меньше текущего nonce аккаунта:** Транзакция считается невалидной и отклоняется, так как она уже была выполнена или заменена другой транзакцией с более высоким gas price.  Это предотвращает replay-атаки.

    * **Если nonce в транзакции больше текущего nonce аккаунта:** Транзакция также считается валидной, но она будет помещена в очередь в mempool до тех пор, пока не будут выполнены все транзакции с меньшими nonce от того же отправителя.  Это обеспечивает правильный порядок выполнения транзакций.


**Важно отметить:**

* **Каждый узел независимо проверяет nonce:** Все узлы в сети Ethereum выполняют эту проверку nonce независимо друг от друга,  гарантируя консенсус о валидности транзакций.
* **Nonce хранится в состоянии, а не в транзакции:**  Сам nonce  не хранится в транзакции.  Транзакция содержит только заявленный nonce, который затем проверяется по состоянию аккаунта.
* **Изменение состояния после выполнения блока:** Состояние аккаунта, включая nonce, обновляется только после того, как транзакция включена в блок и добавлена в блокчейн.


Таким образом,  сеть Ethereum отслеживает использованные nonce через состояние аккаунта, хранящееся в распределенной базе данных.  Это обеспечивает защиту от повторного использования транзакций и гарантирует правильный порядок их выполнения,  что является критически важным для безопасности и надежности сети.

## Пример

Представьте, что вы отправляете два перевода с вашего банковского счета: 100 ETH и 50 ETH.  Если бы nonce не увеличивался, банк мог бы случайно обработать эти транзакции в обратном порядке, списав сначала 50 ETH, а затем 100 ETH.  Nonce гарантирует, что транзакции будут выполнены в правильной последовательности.

## Связанные темы

* [Вернуться к списку вопросов](4.%20Список%20вопросов.md)
* [[Что такое Nonce в состоянии аккаунта?]]
* [[Что такое replay-attack? Как защититься?]]
* [[Как транзакция выполняется на уровне EVM? Может ли измениться code storage аккаунта? Что происходит со storage аккаунта?]]


---