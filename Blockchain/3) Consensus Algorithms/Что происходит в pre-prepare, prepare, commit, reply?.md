---
tags: [блокчейн, консенсус, pbft, византийская-отказоустойчивость, алгоритмы-консенсуса]
aliases: [фазы PBFT, этапы PBFT, шаги PBFT]
---
## Короткий ответ:

PBFT состоит из четырех фаз: pre-prepare (предварительная подготовка), prepare (подготовка), commit (фиксация) и reply (ответ). Эти фазы обеспечивают согласованность и отказоустойчивость при обработке транзакций в распределенной системе.


## Подробный разбор:

**1. Pre-Prepare (Предварительная подготовка):**

* **Действие:** Лидер (primary node) получает запрос и рассылает сообщение **pre-prepare** всем остальным узлам.
* **Содержание:** `{view, sequence number, request digest}`, где:
    * `view`: номер текущего представления системы.
    * `sequence number`: уникальный номер запроса.
    * `request digest`: криптографический хэш запроса.
* **Цель:** Инициировать процесс консенсуса.


**2. Prepare (Подготовка):**

* **Действие:** Узлы проверяют сообщение **pre-prepare** и, если оно корректно, рассылают сообщение **prepare**.
* **Содержание:** `{view, sequence number, request digest, node ID}`.
* **Цель:** Убедиться, что все узлы получили одинаковое предложение от лидера. Требуется кворум 2f+1.


**3. Commit (Фиксация):**

* **Действие:** При получении 2f+1 сообщений **prepare**, узлы рассылают сообщение **commit**.
* **Содержание:** `{view, sequence number, request digest, node ID}`.
* **Цель:** Зафиксировать выполнение операции, гарантируя согласованность.


**4. Reply (Ответ):**

* **Действие:** После 2f+1 сообщений **commit**, узел выполняет запрос и отправляет **reply** клиенту.
* **Содержание:** `{view, sequence number, result, node ID}`. `result` - результат операции.
* **Цель:** Подтвердить клиенту выполнение запроса.


## Связанные темы:

* [[Расскажите о механизме работы консенсуса PBFT. Какие есть фазы?]]
* [[Что такое BFT(как метрика)?]]
* [[Почему нельзя достигнуть консенсуса PBFT, когда злонамеренных нод больше трети]]
* [Вернуться к списку вопросов](3.%20Список%20вопросов)


## Источники:

* [Practical Byzantine Fault Tolerance](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/p398-castro-bft-tocs.pdf)