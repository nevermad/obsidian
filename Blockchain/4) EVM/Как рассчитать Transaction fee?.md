---
title: Как рассчитать Transaction fee?
tags: [EVM, Ethereum, Транзакции, Gas, Fee, Gas Price, Gas Limit]
---
## Короткий ответ

Transaction fee рассчитывается как произведение **gas used** (использованного газа) и **gas price**:

`Transaction Fee = Gas Used * Gas Price`

## Подробный разбор

Transaction fee (комиссия за транзакцию) в Ethereum рассчитывается как произведение **gas used** (использованного газа) и **gas price**:

`Transaction Fee = Gas Used * Gas Price`

Однако, с введением EIP-1559,  механизм определения `Gas Price` изменился. Давайте разберем оба варианта.

**До EIP-1559 (устарело, но важно для понимания):**

* **Gas Price (цена газа):** Пользователь устанавливал Gas Price - ставку в **Wei** за единицу gas. (см. [[Размерность wei, gwei, ether?]]) Более высокая цена газа увеличивала вероятность быстрого включения транзакции в блок.  **Этот механизм  уже  не  используется.**

**После EIP-1559 (текущий механизм):**

* **Base Fee (базовая комиссия):**  Базовая комиссия за газ, которая **динамически изменяется** в зависимости от загруженности сети.  Она **сжигается**,  то есть  уничтожается  и  не  достается  валидаторам.
* **Priority Fee (tip, чаевые):**  Дополнительная комиссия, которую пользователь платит **непосредственно валидатору** за включение транзакции в блок.  Она  влияет  на  приоритет  транзакции  в  блоке.  **Пользователь  теперь  указывает  Max Priority Fee  и  Max Fee Per Gas.**
* **Max Fee Per Gas:** Максимальная сумма, которую пользователь готов заплатить за единицу газа, включая Base Fee и Priority Fee.
* **Max Priority Fee:** Максимальная сумма чаевых, которую валидатор получит.

**Gas Used (использованный газ):**

* **Фактические затраты:** Gas Used - это количество gas, фактически затраченное на выполнение транзакции. Это значение определяется после выполнения транзакции.
* **Зависит от сложности:** Gas Used зависит от сложности транзакции: простой перевод Ether потребляет меньше gas, чем вызов сложной функции смарт-контракта.


**Gas Limit (лимит газа):**

* **Максимальные затраты:** Gas Limit - это максимальное количество gas, которое пользователь готов потратить на транзакцию. (см. [[В чем различие Gas Price и Gas Limit?]])
* **Возврат неиспользованного газа (частичный):** Если транзакция использует меньше gas, чем указано в Gas Limit,  **только  часть** оставшегося газа (газ,  превышающий  Base Fee) возвращается пользователю.  `Base Fee`  всегда  сжигается.


**Пример расчета (после EIP-1559):**

* **Gas Used:** 21,000
* **Base Fee:** 15 Gwei
* **Priority Fee (Tip):** 2 Gwei

`Transaction Fee = 21,000 * (15 + 2) Gwei = 357,000 Gwei = 0.000357 ETH`

## Связанные темы

* [Вернуться к списку вопросов](4.%20Список%20вопросов.md)
* [[Что такое газ?]]
* [[В чем различие Gas Price и Gas Limit?]]
* [[Размерность wei, gwei, ether?]]
## Источники

* [Ethereum Documentation - Gas and Fees](https://ethereum.org/en/developers/docs/gas/)

---