---
tags: [блокчейн, ethereum, консенсус, proof-of-stake, pos, стейкинг, casper, финализация]
aliases: [ethereum pos, стейкинг в ethereum, консенсус ethereum]
---
## Короткий ответ:

Proof-of-Stake (PoS) в Ethereum - это механизм консенсуса, где валидаторы подтверждают блоки, используя свои застейканные (заблокированные) ETH, а не вычислительную мощность.  Выбор валидатора для создания блока происходит случайным образом, с учетом размера стейка. Финализация блоков осуществляется с помощью протокола Casper FFG.

## Подробный разбор

**Как работает PoS в Ethereum:**

1. **Стейкинг:** Чтобы стать валидатором, участник должен заблокировать 32 ETH в качестве стейка.
2. **Выбор Block Proposer:**  Алгоритм случайным образом выбирает валидатора из общего пула для создания и предложения нового блока. Вероятность выбора пропорциональна размеру стейка валидатора.  Подробнее о выборе валидатора: [[Как консенсус POS определяет активного валидатора  или block proposer?]].
3. **Подтверждение блока (Attestation):** Остальные валидаторы проверяют предложенный блок и голосуют за его включение в цепочку, создавая аттестации (attestations).
4. **Финализация (Casper FFG):** Протокол Casper FFG  отслеживает аттестации валидаторов и финализирует блоки,  которые получили достаточную поддержку (2/3 валидаторов). Финализированные блоки считаются необратимыми.  Подробнее о Casper: [[Как работает механизм финализации Сasper?(основная суть)]].

**Преимущества PoS в Ethereum:**

* **Энергоэффективность:** PoS потребляет значительно меньше энергии, чем Proof-of-Work (PoW).
* **Безопасность:**  Экономические стимулы (вознаграждения за стейкинг и штрафы за некорректное поведение - slashing)  обеспечивают безопасность сети.
* **Масштабируемость:** PoS  позволяет увеличить пропускную способность сети и снизить комиссии за транзакции.

**Недостатки PoS в Ethereum:**

* **Риск централизации:**  Валидаторы с большим стейком имеют большее влияние, что потенциально может привести к централизации.
* **Сложность:** Алгоритм PoS  более сложен в реализации, чем PoW.

## Связанные темы:

* [[Что такое stake? Для чего он блокируется?]]
* [[Как консенсус POS определяет активного валидатора / block proposer?]]
* [[Как работает механизм финализации Сasper?(основная суть)]]
* [[Преимущества и недостатки PoS]]  
* [Вернуться к списку вопросов](3.%20Список%20вопросов)


## Источники:

* [Ethereum Foundation Blog: Proof-of-Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
* [Vitalik Buterin's Blog: Casper FFG](https://vitalik.ca/general/2023/05/25/attestation.html)
* [ConsenSys: Proof of Stake](https://consensys.net/knowledge-base/ethereum-2/proof-of-stake/)