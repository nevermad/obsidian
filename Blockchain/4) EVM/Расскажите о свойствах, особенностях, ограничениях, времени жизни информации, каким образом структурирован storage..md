---
title: Свойства и особенности Storage в EVM
tags: [EVM, Ethereum, Storage, Постоянное хранилище, Слоты, Ключи, Gas, Ограничения]
---
## Короткий ответ

Storage в EVM - это **постоянное хранилище ключ-значение** для смарт-контрактов.  Он хранит 256-битные значения в 256-битных слотах, адресуемых 256-битными ключами. Запись в storage - самая дорогая операция в EVM.

![[Pasted image 20241213175520.png]]
## Подробный разбор

**Структура и организация:**

* **Ключ-значение:** Storage организован как key-value store, где как keys, так и values являются 256-битными числами (uint256).
* **256-битные слоты:**  Storage можно представить как massive array из 2<sup>256</sup>  **слотов**, каждый из которых может хранить 256-битное значение.
* **Постоянное хранилище:** Данные в storage  хранятся **постоянно** в состоянии блокчейна и доступны между вызовами транзакций и даже после самоуничтожения контракта. Они сохраняются, пока существует контракт.

**Свойства и особенности:**

* **Дорогостоящая запись:**  **Запись** данных в storage -  **самая дорогая операция** в EVM с точки зрения потребления газа. Это связано с тем, что изменение требует обновления дерева состояний блокчейна, что является вычислительно сложной операцией.
* **Дешевое чтение:** Чтение данных из storage значительно **дешевле**, чем запись.
* **Default value:**  По умолчанию, все слоты в storage инициализируются нулем.
* **Доступ через опкоды:** Доступ к данным в storage осуществляется с помощью specific opcodes (специальных опкодов), таких как `SLOAD` (чтение из storage), `SSTORE` (запись в storage).

**Ограничения:**

* **Высокая стоимость газа:**  Из-за высокой стоимости записи в storage, разработчики должны тщательно управлять использованием хранилища и минимизировать количество записей.
* **256-битные ключи и значения:** Storage может хранить только 256-битные значения. Для работы с данными другого размера требуется преобразование или декомпозиция. Сложные структуры данных  такие как динамически изменяемые массивы,  хранят свои данные в storage, используя схемы хеширования и индексации  для доступа к элементам.

**Примеры использования:**

* **Хранение балансов токенов:**  В ERC-20 токенах, балансы держателей токенов хранятся в storage, используя mapping  от address к balance.
* **Хранение состояния контракта:**  Любые постоянные данные, необходимые для работы контракта, такие как  параметры конфигурации или результаты вычислений, хранятся в storage.
## Связанные темы

* [Вернуться к списку вопросов](4.%20Список%20вопросов.md)
* [[Расскажите об основных компонентах EVM? Какие сущности существуют постоянно, какие временно? Расскажите о их жизненном цикле.]]
* [[Какие ограничения есть у memory, stack, storage, code storage?]]
* [[Расскажите о свойствах, особенностях, ограничениях, времени жизни информации, каким образом структурирован stack.]]
* [[Расскажите о свойствах, особенностях, ограничениях, времени жизни информации, каким образом структурирован memory.]]
* [[EVM Opcodes]]

## Источники

* [Ethereum Yellow Paper - EVM](https://ethereum.github.io/yellowpaper/paper.pdf#page=15) 
* [Solidity Documentation - Data Location](https://docs.soliditylang.org/en/v0.8.20/internals/layout_in_memory.html) 

---