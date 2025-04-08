# Введение

### Цели и задачи курса

Предоставить студентам программу, сообщество и поддержку при обучении и поиске работы.

### Цели курса:

- научить разрабатывать коммерческие блокчейн проекты
- понимание современного технического стека и как работают протоколы на блокчейне
- найти работу в блокчейн проекте

### Структура и формат курса

- Текстовые и видео учебные материалы.  
Для модулей курса, будут предоставлены основные материалы, а иногда и дополнительные.
Задача запомнить информацию(перенести в долговременную память) и научиться думать в новой парадигме и понятиях.
  - Если вы гений и быстро запоминаете на ходу, то просто изучайте материалы и будет вам счастье =)
  - Если вы человек обычный, то советую делать собственные конспекты по пройденным темам.  
  Сначала вы изучаете материал и пробуете понять его, а потом пишете свой конспект.
  Суть не в переписывании материалов, а изложении своего понимание максимально детально и глубоко.
  Это очень помогает.  
  Ну и конечно же практика и периодические интервальное повторение собственных конспектов.
  Чаще всего я учусь этим способом, и только когда хорошо начинаю понимать направление, то могу перестать делать конспекты.  
  Вы также можете делать любым удобным для вас способом, это один из работающих вариантов.
- Задания в автоматизированных системах. 
- Задания в публикацией кода в Github.  
  Будем использовать cross-review, mentor | course author review.
- Еженедельные встречи в формате вопрос-ответ, разъяснение сложных тем, сдача заданий и интервью по модулям, обсуждение обратной связи.

### Вводная по обучению

Школа предоставляет необходимую программу с детализацией по всем нужным темам.  
Мы создаем сообщество и помогаем с ответами на сложные вопросы чтобы ваше обучение проходило быстрее и эффективнее.  
От вас требуется отнестись к обучению ответственно.  
Делать все возможно(в меру ваших внутренних сил), чтобы освоить теоретический материал и выполнить практические задания.  
Учится студент, за него никто не усвоит информацию и не получит навыки.  
Процесс связан с упорной работой на протяжении всего курса.  
Скажу честно - Будет сложно.  
Задавайте вопросы, участвуйте в обсуждениях в чате и аудио конференциях(подвергайте критике решения ваших коллег и сами предлагайте идеи), так вы вырастите быстрее.  

### Важные правила

Токсичное общение, поведение недопустимо, списывание готовых заданий решений или ответов.
1 предупреждение, далее отчисляем без возможности восстановится.
Мы создаем атмосферу, где ребята настроены на работу и делятся своими знаниями с другими. 

Это первый поток курса, поэтому могут быть сложности в части процесса обучения.
Не стесняйтесь давать обратную связь, таким образом мы сможем развивать и наполнять программу курса.

Если не справляетесь с темпом курса или кол-вом информации и заданий говорите об этом.
При необходимости подкорректируем требования в программе.

# Основная часть

- Основа курс - [Введение в блокчейн 23/24, ПМИ ФКН ВШЭ](https://www.youtube.com/playlist?list=PLEwK9wdS5g0rmAlWx3dRkUaoPb1FQU3L4)  
Самостоятельно необходимо читать дополнительные ссылки из курса Berkley или помеченные must self-learn.
Другие ссылки изучать по желанию.
- [Course material github repository](https://github.com/sizovk/blockchain-hse)
- [Updraft Cyfrin](https://updraft.cyfrin.io/) - если после изучения основных материалов и ссылок из урока нашего курса,
вам не понятны часть можете попробовать найти похожие темы в этом курсе.

# Intro(в первый день курса)

[Metamask Wallet - Quick Installation and Set up](https://www.youtube.com/watch?v=kHF70SWFTYU) - установить расширение, завести тестовый кошелек, переключиться на тестовую сеть Sepolia, получить ETH в кране.

Список кранов для получения Ether в Sepolia:
- https://www.alchemy.com/faucets/ethereum-sepolia
- https://sepoliafaucet.com/
- https://faucet-sepolia.rockx.com
- https://www.infura.io/faucet/sepolia
- https://faucet.quicknode.com/ethereum/sepolia
- https://www.ethereum-ecosystem.com/faucets/ethereum-sepolia (возможность майнинга sETH).
- https://sepolia-faucet.pk910.de/ (возможность майнинга sETH).

### Lesson 1: Basic cryptography

[Введение в блокчейн 23/24 лекция 1](https://www.youtube.com/watch?v=hwUeswEeYSA&list=PLEwK9wdS5g0rmAlWx3dRkUaoPb1FQU3L4&index=1&pp=iAQB)

Примеры с математикой постараться понять насколько вы можете.
Задача минимум понять свойства системы.
Если не хватает математической базы, доказательства можно пропустить. 

##### Список вопросов по лекции:

- Когда нужен блокчейн, а когда нет?
- Что из себя представляет блокчейн на базовом уровне?
- Основные требования к блокчейну?
- Что такое консенсус механизм и для чего он нужен?
- Как изменяется состояние в блокчейне?
- Что такое цифровая подпись?
- Как и где цифровая подпись используется в блокчейне?
- Зачем нужен публичный и приватный ключ для подписи?
- Как публичный ключ связан с адресом в Ethereum?
- Что такое MerkleTree? Какие сценарии использования? Расскажите и зарисуйте структуру.
- Что такое функция хеширования? Какими свойствами она должна обладать?
- Какие операции выполняет кошелек?
- Что такое публичный и приватный ключ кошелька?
- Что такое memonic/seed phrase на самом базовом уровне?
- Как генерируется mnemonic фраза?
- Какие типы кошельков вы знаете?
- Если вы хотите заменить программное обеспечение кошелька или блокчейн, нужно ли вам генерировать новый mnemonic phrase? Ответ детализируйте.
- Что такое BIP-39?
- Свойства функции ассиметричной криптографии?
- Зачем нужен Private и Public ключ?
- Как происходит шифрование и расшифровка сообщения? Каким ключем?
- Как происходит подпись и верификация сообщения? Какими ключами?
- Какие алгоритмы подписи, шифрования, хеширования используется в Ethereum?
- Какие эллиптические кривые используется в Bitcoin и Ethereum?

##### Дополнительные ссылки:
    
* Курс Berkley
  - [Cryptographic Hash Functions](https://www.youtube.com/watch?v=WSejk1E6fRo&list=PLS01nW3RtgopFiRQiM-onPH38S0D2DU31&index=2)
  - [Digital Signature](https://www.youtube.com/watch?v=V6y6yfr3G4o&list=PLS01nW3RtgopFiRQiM-onPH38S0D2DU31&index=3)
* Полезные сервисы
  - [DeFiLama аналитика TVL DeFi](https://defillama.com/) - must check 
* Cryptography Basic:
  - [Hash functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function) - must read
  - [Difference between SHA-256 and Keeccak-256](https://www.geeksforgeeks.org/difference-between-sha-256-and-keccak-256/) - must read
  - [Asymmetric cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) - must read
  - [RSA as a simplest example](https://neerc.ifmo.ru/wiki/index.php?title=RSA)
  - [RSA in details](https://habr.com/ru/articles/745820/) - must read
* Cryptography Extra:
  - [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
  - [Threshold cryptography](https://en.wikipedia.org/wiki/Threshold_cryptosystem)
* Algorithms Basic:
  - [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree) - must read
  - [Commit-reveal scheme (coin flipping)](https://en.wikipedia.org/wiki/Commitment_scheme)
* Algorithms Extra:
  - [Secret sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing)
* Book extra:
  - Бернет, Пэйн "Криптография. Официальное рук-во RSA Security".
В ней вы поймёте на самом высоком уровне не заумную научную криптографию с теорией чисел и прочими сложностями,
а как и где она применяется на практике, в информационных системах, для решения конкретных базовых практических задач.

##### Tasks:

* Сryptohack
  - [Hashes](https://cryptohack.org/challenges/hashes/) - must solve and read. По возможности и от вашего уровня подготовки решите максимально кол-во заданий. Задания в которых нет идей для решения и потрачено много времени просто пропускайте и пробуйте решить следующее.
  - [RSA](https://cryptohack.org/challenges/rsa/) - must solve and read. По возможности и от вашего уровня подготовки решите максимально кол-во заданий. Задания в которых нет идей для решения и потрачено много времени просто пропускайте и пробуйте решить следующее.
  - [Merkle Tree](https://cryptohack.org/challenges/hashes/) - must solve. Написать функцию верификации доказательства для MerkleTree на любом языке и получить флаг.
  - [Math](https://cryptohack.org/challenges/maths/) - если хочется познакомится с математикой лежащей в основе криптографии. Если получится разобраться с этой темой, понимать что лежит в основе станет легче.
  - [Elliptic curve cryptography](https://cryptohack.org/challenges/ecc/) - очень полезно и часто используется в блокчейне, но требует знания всех предыдущих тем.

### Lesson 2: Bitcoin

[Введение в блокчейн 23/24 лекция 2](https://youtu.be/HazbY59pjlE?si=WWTSbMGtkQp_DaZw)

Если у вас недостаточно математической базы для понимания, часть семинара с программированием эллиптических кривых постарайтесь понять как получится.
Разберитесь с написанием функций address, encode для Public Key.

Ссылки для практики:
- [Bitcoin script wiki](https://en.bitcoin.it/wiki/Script)
- [Blockchain Demo](https://andersbrownworth.com/blockchain/) - выполните примеры из первого предоставленного на сайте видео
- [Blockchain Demo: Public / Private Keys & Signing](https://andersbrownworth.com/blockchain/public-private-keys/) - выполните примеры из второго предоставленного на сайте видео
- [Bitcoin Electrum wallet](https://bitcoin.org/en/wallets/desktop/mac/electrum/)

Заведите себе кошельки, получите тестовый ETH/BTC и отправьте:
- ETH на `0xB98f7d8100B9346ffff5cA6552518A8971689692`
- BTC на `bc1qjq6n5u3mx5p4kdkz2f8w3h7n2s0etv7dgk65yn` 10000 satoshi

- Дополнительно можете попробовать сделать Multisig wallet(в Electrum) и разобраться как работает.

##### Дополнительные ссылки:

* Курс Berkley
  - [Introduction to Blockchain Technology](https://youtu.be/FmKbGHu7oAM?si=fhxr446u7T-CVW_L) - must watch
  - [DeFi MOOC: Introduction to Blockchain Technology](https://youtu.be/u70_rafPs-0?si=l_B7uNMkSl-vcVwl) - must watch
* [Введение в блокчейн технологии Innopolis](https://www.youtube.com/playlist?list=PLSlHOPC2QdQnBjeR2UWAsEPxCssDGBsuc) - если тема не полностью непонятна лекций 1001-3007. Смотреть уроки только где преподаватель рассказывает о Bitcoin.
* [Bitcoin white-paper](https://berkeley-defi.github.io/assets/material/bitcoin.pdf)

##### Список вопросов по лекции:

- Что такое mempool?
- Для чего нужны блоки? Почему используют блоки, а не отдельные транзакции?
- Размер блока в BitCoin & Ethereum? Примерное кол-во транзакций которое может вместить блок в этих сетях?
- Время создания блока Bitcoin & Ethereum? Ваши мысли почему такое время?
- Как происходит создание блока?
- Какую математическую задачку решают майнеры в POW консенсусе? Что конкретно они делают и какие критерии правильности решения задачи?
- Difficulty & Target в чем отличие?
- Может ли злонамеренный майнер, который создает блок потратить средства другого пользователя? Ответ детализируйте.
- Что такое финализация в консенсусе?
- Что такое пулы майнинга? Как они работают?
- Структура блока, какие поля имеются и для чего нужны?
- Как связаны блоки в цепочке?
- Используется ли MerkleTree в блоке? Если да, то для чего?
- Nonce 4 байт, значения могут быть от 0 to 4,294,967,295. Что делать если перебрали все nonce, но не решили математическую задачку?
- Какие параметры блока и каким образом вы стали бы проверять?(если ваша задача написать node-client)
- За счет чего достигается неизменность данных в блокчейне?
- Структура транзакций, какие поля имеются и для чего нужны?
- Как работает UTXO модель в Bitcoin?
- Как работает модель балансов в Ethereum?
- Как Public Key и Private Key связан с UTXO?
- P2PKH как работает алгоритм?
- P2SH как работает алгоритм? Примеры использования?
- Что такое SeqWit?

# Идея для занятий

5-10 встреч, где каждый студент изучает дополнительную ссылку и потом рассказывает суть и особенности всей группе.

### Lesson 3: Consensus Algorithms

[Введение в блокчейн 23/24 лекция 3](https://www.youtube.com/watch?v=fPjA5rVNvbM)

Успехом можно считать что при использовании ваших подготовленных материалов вы можете ответить на вопросы и рассказать о консенсусах, как они работают.
Посмотрите cеминар про транзакции, попробуйте повторить этот код и соотнести с полученными знаниями.
Если совсем не понимаете какие-то моменты(например математики криптографии), то просто переиспользуйте готовые, чтобы разобраться в базовых аспектах системы.

##### Список вопросов по лекции:

- Что такое консенсус алгоритм? Для чего он нужен и какую задачу выполняет?
- Что такое CFT и ее применение?
- Какие преимущества и недостатки есть в системе если использовать наивную реализацию репликации базы данных, без дополнительных механизмов?
- Что такое Quorum?
- Опишите суть проблемы последовательного принятия предложений?
Последовательное принятие propose A, propose B(разное состояние у разных нод)
- Приведите примеры конфликтов принятия решений в распределенной системе?
- Как решить проблему конфликтов?
- Можно ли использовать время из нод для сортировки proposal? Ответ детализируйте.
- Что такое Lamport timestamp, Lamport clock?
- Расскажите о механизме работы консенсуса Paxos. Какие основные роли и взаимодействие? Описывайте сразу в терминах ПО(без парламента).
- Что происходит в phase 1, phase 2? Что такое n, v?
- Что такое BFT(как метрика)?
- Что такое задача византийских генералов? Какую проблему решает?
- Какое кол-во участников может быть злонамеренными для достижения консенсуса PBFT?
- Почему нельзя достигнуть консенсуса PBFT когда злонамеренных нод > 1 / 3 ? 
- Перечислите предположения PBFT. Опишите потенциальные проблемы, которые могут произойти если пренебречь любым из предположений.
- Расскажите о механизме работы консенсуса PBFT. Какие есть фазы?
- Что происходит в pre-prepare, prepare, commit, reply?
- Что такое финализация?
- Как BFT применяется в блокчейне? Соотнесите сущности блокчейна системы с ролями или действиями BFT.
- Основная идея и механизм работы POW(Bitcoin version)?
- Какую математическую задачу решают майнеры в POW? Почему это энерго-затратно и безопасно? Что такое соревнование мощностей? 
- Расскажите о финализации блоков в Bitcoin.
- За что майнеры получают награды?
- Может ли работать блокчейн Bitcoin без наград за создание блока?
- Что такое сложность сети, от чего зависит? Как меняется сложность во времени? Что произойдет если не обновлять сложность?
- Что такое аттака 51%?
- Какая сложность сети Bitcoin на текущий момент(число в шестнадцатеричной системе исчисления)?
- Каким образом консенсус Bitcoin решает проблему форков?
- Что такое Genesis block? Какая информация там находится?
- Что такое orphan block?
- Плюсы и минусы POW.
- Основная идея и механизм работы POS(Ethereum version)? Расскажите о создании и финализации блоков в Ethereum.
- Что такое stake? Для чего он блокируется?
- Как консенсус POS определяет активного валидатора / block proposer?
- Что происходит в случае злонамеренного / ошибочного поведения?
- Соответствует ли количество валидаторов кол-ву нод в блокчейне Ethereum? Ответ детализируйте.
- Каким образом консенсус Etherium решает проблему форков?
- Расскажите о финализации блоков в Ethereum.
- Как работает механизм финализации Сasper?(основная суть)
- Преимущества и недостатки POS.
- Что такое Liquid Staking?
- Суть и идея протокола Lido?

##### Дополнительные ссылки:

* Staking
  - [Liquid vs. Illiquid Staking](https://www.stakingrewards.com/journal/guides/liquid-vs-illiquid-staking-what-is-better) - must read  
    article about staking background, types and liquid staking

### Lesson 4.1: EVM

[Введение в блокчейн 23/24 лекция 4](https://www.youtube.com/watch?v=NZxd6wJynPY)

Повторите примеры кода из семинара и в процессе разберитесь как работают функции.  
Напишите смарт-контракты с семинара и задеплойте в сеть Sepolia.  
Сделайте верификацию байт-кода контракта на Etherscan и предоставьте URL с транзакцией деплоя с вашего кошелька.  

Самые простые идеи или как работает необычный синтаксис вы можете проверять используя [RemixIDE](https://remix.ethereum.org/).
Все остальные задания решать с использованием Foundry.  
[Foundry installation guide](https://book.getfoundry.sh/getting-started/installation)

Получение API-KEY тестовых нод.(необходимо зарегистрироваться)
* [Infura node provider](https://www.infura.io/)
* [Alchemy node provider](https://www.alchemy.com/supernode)

##### Список вопросов по лекции:

- Типы аккаунтов в EVM?
- Что такое EOA? Имеет ли он приватный ключ? Может ли хранить произвольные данные ? Может ли хранить код? Кто контролирует аккаунт?
- Что такое SmartContract? Может ли иметь приватный ключ? Может ли хранить произвольные данные ? Может ли хранить код? Кто контролирует аккаунт?
- Что такое Nonce в состоянии аккаунта?
- Почему Nonce увеличивается после каждой транзакции?
- Когда еще Nonce увеличивается помимо исполнения транзакции?
- Что такое replay-attack? Как защититься?
- Как отменить транзакцию в блокчейне?
- Можно ли изменить код контракта?
- Какие преимущества и недостатки есть у неизменности контрактов?
- Можно ли сделать контракт изменяемым?
- Может ли смарт контракт инициировать транзакцию?
- Почему нужно платить fee за выполнение если транзакция отменилась из-за ошибки?
- Что такое атомарность транзакций?
- Почему порядок транзакций не гарантирован?
- Расскажите об основных полях и структуре транзакции.
- Что такое газ?
- В чем различие Gas Price и Gas Limit?
- Размерность wei, gwei, ether?
- Приведите примеры использования нативной валюты Ether.
- Приведите примеры транзакций для EOA и SmartContract аккаунтов.
- Что такое целые и вещественные числа?
- Почему блокчейн использует арифметику в целых числах?
- Как рассчитать Transaction fee?
- Как транзакция выполняется на уровне EVM? Может ли измениться code storage аккаунта? Что происходит со storage аккаунта?
- Расскажите об основных компонентах EVM? Какие сущности существуют постоянно, какие временно? Расскажите о их жизненном цикле.
- Какие ограничения есть у memory, stack, storage, code storage?
- Как EVM посчитывает доступный газ?
- Расскажите о свойствах, особенностях, ограничениях, времени жизни информации, каким образом структурирован stack.
- Расскажите о свойствах, особенностях, ограничениях, времени жизни информации, каким образом структурирован memory.
- Расскажите о свойствах, особенностях, ограничениях, времени жизни информации, каким образом структурирован storage.

##### Дополнительные ссылки:

* [Ethereum white-paper](https://ethereum.org/en/whitepaper/) - must read

### Lesson 4.2: SmartContracts

* [Ethernaut CTF](https://ethernaut.openzeppelin.com/) - 1 - 20 задача

##### Дополнительные ссылки:

* Курс Berkley
  - [Introduction to smart contracts](https://www.youtube.com/watch?v=iK93guovsXQ)
* [Wallet Gas Tutorial](https://medium.com/@maimai816/advanced-metamask-gas-tutorial-how-to-set-your-own-gas-prices-236d59f563b7) - must read
* [A Comprehensive Guide To Gas And Gas Price In Solidity](https://medium.com/stackanatomy/a-comprehensive-guide-to-gas-and-gas-price-in-solidity-bfb9c00970af) - must read

##### Дополнительные ссылки: Solidity

* Syntax
  - [Official documentation](https://docs.soliditylang.org/en/stable/) - must read
  - [ABI (contract interface serialization) specification](https://docs.soliditylang.org/en/latest/abi-spec.html)
  - [Solidity contracts inheritance article](https://www.geeksforgeeks.org/solidity-inheritance/) - must read
  - [Official Solidity style guide](https://docs.soliditylang.org/en/latest/style-guide.html)
  - [Solidity By Example](https://solidity-by-example.org/)
* Implementations of algorithms
  - [Excellent pack of Solidity usage examples](https://solidity-by-example.org/)
  - [Merkle tree OpenZeppelin implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/MerkleProof.sol)
  - [Fixed point math in Solidity](https://hackernoon.com/fixed-point-math-in-solidity-616f4508c6e8) - must read
* Misc
  - [SmartContractProgrammer YouTube](https://www.youtube.com/@smartcontractprogrammer)
  - [All about Solidity](https://medium.com/@jeancvllr) - best articles about all language details
  - [All about Solidity common article](https://medium.com/coinmonks/all-about-solidity-article-series-f57be7bf6746)
  - [Solidity common patterns](https://fravoll.github.io/solidity-patterns/) - must read
* Sending ETH
  - [transfer() ETH gas restrictions](https://consensys.io/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) - must read  
    notes why using hardcoded 2300 gas, sent with ETH when transfer() and send() is bad
  - [3 methods to send ether](https://medium.com/daox/three-methods-to-transfer-funds-in-ethereum-by-means-of-solidity-5719944ed6e9) - must read  
    transfer() / send() / call.value().gas() explained
* Sending/approving ERC20
  - [Safely using ERC20](https://decentraland.org/blog/technology/safe-erc20-transfers) - must read  
    different types of ERC20 transfers/approves
  - [ERC20 token code, annotated by Ethereum devs](https://ethereum.org/en/developers/tutorials/erc20-annotated-code/)
  - [Article with good explanations of ERC677 and how it was born](http://blockchainers.org/index.php/tag/erc-677/)
* Functions calling
  - [Delegatecall vs Call vs Library](https://www.blocksism.com/blog/solidity-delegatecall-call-library) - must read  
    small article showing differences between call types
  - [Delegatecall() - official docs for storage layout Proxy contracts](https://blockchain-academy.hs-mittweida.de/courses/solidity-coding-beginners-to-intermediate/lessons/solidity-5-calling-other-contracts-visibility-state-access/topic/delegatecall/) - must read
  - [OpenZeppelin proxies docs - main documentation about proxies standards and implementations](https://docs.openzeppelin.com/contracts/5.x/api/proxy)
  - [Proxy selectors clashing](https://medium.com/nomic-foundation-blog/malicious-backdoors-in-ethereum-proxies-62629adf3357) - must read  
    article, demonstrating function selector clashing in proxy
  - [Wormhole uninitialized proxy bug review](https://medium.com/immunefi/wormhole-uninitialized-proxy-bugfix-review-90250c41a43a) - must read  
    article, showing proxy internals, types and problems
* Gas
  - [Gas Optimisation Tips](https://github.com/devanshbatham/Solidity-Gas-Optimization-Tip) - must read

##### Дополнительные ссылки: EVM

* Instruction set & common info
  - [The EVM Handbook](https://noxx3xxon.notion.site/noxx3xxon/The-EVM-Handbook-bb38e175cc404111a391907c4975426d)  
    big pack of different useful articles
  - [EVM opcodes & instructions set](https://www.evm.codes/) - must check
  - [EVM Deep Dives: The Path to Shadowy Super Coder](https://noxx.substack.com/p/evm-deep-dives-the-path-to-shadowy) - must read  
    excellent deep articles about bytecode, opcodes, storage, calls, etc..
  - [Deconstructing a Solidity Contract](https://blog.openzeppelin.com/deconstructing-a-solidity-smart-contract-part-i-introduction-832efd2d7737) - must read  
    deep understanding of EVM flow an assembly
  - [EVM puzzles](https://github.com/fvictorio/evm-puzzles)  
    fun command-line tasks for reading EVM assembly
  - [Stack too deep error in Solidity](https://medium.com/aventus/stack-too-deep-error-in-solidity-5b8861891bae) - must read  
    deep article about EVM stackframe organization & “stack too deep” error
* Contracts deployment
  - [Init code & contract creation](https://leftasexercise.com/2021/09/05/a-deep-dive-into-solidity-contract-creation-and-the-init-code/) - must read  
    Good article with review of creation bytecode using standard CREATE. Also
    good to begin read EVM bytecode
  - [example of use CREATE2](https://hackernoon.com/using-ethereums-create2-nw2137q7) - must read  
    article about CREATE2 usage to precompute contract address
  - [example of use CREATE2](https://github.com/miguelmota/solidity-create2-example) - must read  
    examples how to precompute address in both Solidity and JS
  - [Potential security implications of CREATE2](https://ethereum-magicians.org/t/potential-security-implications-of-create2-eip-1014/2614)  
    how to use CREATE2 to change deployed code of contract
* Storage/memory/calldata organization
  - [Official docs for storage layout](https://docs.soliditylang.org/en/stable/internals/layout_in_storage.html) - must read
  - [Understanding Ethereum Smart Contract Storage](https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/) - must read  
    article, explaining how dynamically sized type are mapped to storage slots
  - [Detailed explanation of Ethereum storage type (memory,storage) and variable storage old (Solidity 4) but very detailed explanation of memory-storage](https://www.fatalerrors.org/a/19131jg.html) - must read
  - [EVM: From Solidity to byte code, memory and storage](https://www.youtube.com/watch?v=RxL_1AfV7N4) - must read  
    video, deep explaining memory&storage usage by EVM
  - [storage collision simple example](https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/06-storage-collisions/) - must read  
    short example of storage collision
  - [real life example in Acropolis contract](https://mixbytes.io/blog/collisions-solidity-storage-layouts)  
    storage collision found in audit

##### Список вопросов по лекции:

- Что такое pragma? Как указать версию  >, <, = ?
- Какую функциональность несет ключевое слово contract?
- Какие основные отличия между версиями Solidity 0.4, 0.5, 0.6, 0.7, 0.8?
- Какую функциональность добавляет ключевое слово calldata, memory? В чем отличие calldata и memory?
- Где хранятся переменные объявленные в теле смарт-контракта?
- Где хранятся переменные объявленные в теле функции смарт-контракта?
- Где хранятся переменные объявленные в параметрах функций смарт-контракта?
- Как расcчитывается номер слота для хранения переменных смарт-контракта?
- Какие типы данных есть в Solidity?
- Какими дефолтными значениями инициализируются переменные?
- Разница между Value & Reference type? Приведите примеры этих типов данных.
- Каким образом Fixed array, Dynamic array, Struct, Mapping представлены в слотах памяти?
- Как хранятся строки в смарт-контрактах?
- Особенности constant, immutable переменных.
- Как работают модификаторы видимости public, private, internal, external на уровне Solidity? Какие нюансы на уровне байткода EVM?
- Приведите примеры когда стоит делать функцию / переменную private, external на реальных примерах?
- Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?
- Дана view функция, которая попробует изменить состояние storage? Транзакция отмениться сразу, в конце выполнения функции или в другой промежуток времени?
- Дана pure функция, которая попробует прочитать состояние storage? Транзакция отмениться сразу, в конце выполнения функции или в другой промежуток времени?
- Как исполнить public, external функции смарт-контракта?
- Как исполнить view, pure функции смарт-контракта?
- Что такое modificator? Как работает на уровне Solidity и EVM?
- Какова последовательность выполнения кода нескольких модификаторов и тела функции?
- Что такое msg.sender и tx.origin? В чем отличие?
- Что такое address(0)? Это EOA или smart contract? Кто контролирует этот адрес?
- Что такое selector функции? Когда он генерируется, а когда отсутствует? Для чего используется?
- Каким образом представлено логирование? Особенности и ограничения.
- Какую функциональность несет event, emmit?
- Сколько параметров может быть в event? Как работают индексированные параметры?
- Каким образом оперативно отслеживать важные изменения в работе вашего смарт-контракта? Например: у вас есть контракт выпуска NFT и вы хотели бы знать когда и какая NFT была выпущена.
- Что такое interface в Solidity? Как представлен на уровне EVM? Какие особенности и ограничения?
- Как public работает для переменных?
- Что такое упаковка структур? Приведите примеры.
- Как работает constructor в контракте?
- Что такое initial code, runtime code??
- Как работает модификатор payable?
- Что такое msg.value?
- Разница payable и non-payable addresses?
- Если контракт не имеет payable функций, можно ли на него отправить Ether?
- Как задать произвольное кол-во газа при вызове функции из контракта?
- Назовите все возможные способы перевода Ether? Какие особенности каждого способа? Расскажите какой способ когда использовать?
- Что такое fallback функция? Когда вызывается? Как представлена на уровне байткода EVM?
- Что такое receive функция? Когда вызывается? Как представлена на уровне байткода EVM?
- Может ли произойти коллизия селекторов функции? Как решить эту проблему?
- Что такое raw call? Как представлен на уровне байткода? Когда стоит применять? Какое значение msg.sender, msg.value внутри вызова delegatecall?
- Какую информацию необходимо передать в raw call чтобы вызвать определенную функцию другого контракта? Как кодировать эти данные? Какой layout у этих данных?
- Какую информацию хранит 2 аргумент bytes memory data при возврате из raw call?
- Что такое delegatecall? Как представлен на уровне EVM? Откуда берется storage, откуда bytecode? Какое значение msg.sender, msg.value внутри вызова delegatecall? Когда стоит применять?
- Чем опасен delegatecall?
- Что происходит после выполнения selfdistruct?

#### Lesson 5.1: DeFi patterns

[Введение в блокчейн 23/24 лекция 5](https://youtu.be/wjWfI1LBjDc?si=WsfXbyMcQtFSKK8W)

Посмотрите семинар как решается Ethernaut, до 1:51:40.
Семинар содержит разбор решений части заданий Ethernaut, поэтому студентам необходимо сначала прорешать максимальное кол-во задач.
Далее просмотреть оставшуюся часть семинара и проверьте ваши мысли решения и решением в курсе.

Дополнительно изучите имплементации:
* стандарты ERC-20, ERC-721, ERC-1155 от OpenZeppelin.
* паттернов Ownable, Ownable2Step, AccessControl от OpenZeppelin
* имплементацию контрактов Proxy, ERC1967Proxy, DelegateProxy, Unstructured Storage proxy, Beacon.

OpenZeppelin repos:
* [OpenZeppelin community tutorial](https://github.com/OpenZeppelin/openzeppelin-labs)
* [OpenZeppelin contracts](https://github.com/OpenZeppelin/openzeppelin-contracts)

##### Дополнительные ссылки:

* Курс Berkley
  - [Introduction and Overview of DeFi](https://www.youtube.com/watch?v=gX3mc83CJtQ)
  - [DeFi Updated](https://www.youtube.com/playlist?list=PLS01nW3RtgopICEFsRCvT_SIjoOtGa869)
* [Comparing Centralized to Decentralized Finance](https://berkeley-defi.github.io/assets/material/arthur-cefi-vs-defi-2106.08157.pdf)
* [DeFi overview](https://berkeley-defi.github.io/assets/material/defi-sok-ariah-2101.08778.pdf)
* [Decentralized Finance: On Blockchain and Smart Contract-Based Financial Markets](https://berkeley-defi.github.io/assets/material/Fabian-Schar-decentralized-finance-on-blockchain-and-smart-contract-based-financial-markets.pdf)
* Governance
  - Article about [on-chain governance with voting from Open Zeppelin](https://docs.openzeppelin.com/contracts/5.x/governance)
* Finematics
  - [Finematics YouTube](https://www.youtube.com/@Finematics)
  - [Guide To Decentralized Finance by finematics](https://finematics.com/guide-to-decentralized-finance/)
* [MIPT defi course(russian speaker)](https://drive.google.com/drive/folders/1fnISGF6VgCPsBXBPOCDi9KeeD0_ILJza)  
    If you don't understand some topics, try to find a lesson on the right topic in this course.
    This course covers many topics of the current course. You can use it as an additional source if there is a misunderstanding after studying the required materials of various lessons of our course.

##### Список вопросов по лекции:

- Что такое EIP?
- Приведите 3-5 примеров популярных EIP и расскажите коротко о чем они?
- Что такое ERC?
- Приведите примеры популярных ERC и расскажите коротко о чем они?
- Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.
- Опишите основные функции, события и особенности поведения ERC-20 токенов? Обратите внимание на обязательные и необязательные требования стандарта.
- Какие проблемы есть у современной реализации функции transfer?
- Что такое SafeERC?
- С помощью каких функций израсходовать выданный approve ERC-20?
- Опишите суть approve front-running attack?
- Что такое double spending?
- Опишите суть, преимущества и недостатки паттерна unlimited amount approval.
- Опишите суть, преимущества и недостатки exact amount approval? Почему unlimited amount approval более распространен?
- Alice имеет 7.65 токена(в человеческой интерпретации). Какой баланс храниться на контракте: для стандартного токена OpenZeppelin или для USDC?
- Что такое unchecked блоки?
- Как работает safeERCTransfer? Что происходит по шагам.
- Опишите основные функции, события и особенности поведения ERC-721 токенов? Обратите внимание на обязательные и необязательные требования стандарта.
- С помощью каких функций израсходовать выданный approve ERC-712?
- Отличие работы transferFrom vs safeTransferFrom ERC-712?
- Какие потенциальные проблемы / уязвимости могут произойти при наличии механизма обратных вызовов?
- Опишите основные функции, события и особенности поведения ERC-721 токенов? Обратите внимание на обязательные и необязательные требования стандарта.
- С помощью каких функций израсходовать выданный approve ERC-712?
- Отличие работы safeTransferFrom vs safeBatchTransferFrom ERC-1155?
- Как и где хранить медиа-данные NFT или SFT?
- Что представляет из себя access control паттерн? Приведите примеры необходимости использования.
- Расскажите идею и возможности паттерна Ownabale. Какие функции контракт имеет? Как выдавать и забирать доступ?
- Расскажите идею и возможности паттерна Ownabale2Step. Какие функции контракт имеет? Как выдавать и забирать доступ?
- Расскажите о работе role-based AccessControl OpenZeppelin. Какие функции контракт имеет? Как выдавать и забирать доступ? Кто является админом? Как работает DEFAULT_ADMIN_ROLE?
- Что такое и как работает Multisig? Понятия quorum & threshold и как правильно выбирать эти параметры. Как происходит отправка транзакций из Multisig? Приведите популярные примеры имплементации.
- Multisig 1:2  какие могут быть проблемы?
- Какие требования следует предъявить к аккаунтам участников Multisig?
- Что такое DAO?
- Что такое и для чего необходим Governance Token? Как происходит процесс голосования? Как токен влияет на голосование?
- Voting power и баланс Governance Token это одинаковые понятия?
- При голосовании Governance Token блокируется? Как можно сделать не блокирующийся механизм?
- Что такое rug pool? Приведите примеры реальных протоколов в которых злоумышленник смог реализовать эту аттаку.
- By design EVM имеет неизменямый байткод для контрактов. За счет каких мехзанизмов получается обойти это ограничение и сделать контракт изменямым?
- Как работает delegatecall?
- Какие значения msg.value, msg.sender при call, staticcall, delegatecall?
- Расскажите подробно как работает паттерн proxy? Где храниться код, состояние, имплементация, какие есть преимущества и недостатки.
- Как изменить implementation в proxy контракте?
- Какие ограничения /ососбенности накладываются на storage proxy контракта? Каким способом согласовывать storage proxy и implementation?
- Что такое storage collision? Расскажите о этой ошибке на примере реального протокола, ее последствия и способы предотвращения.
- Разработчик пытается заменить implementation в proxy контракте, какие ограничения мы должны учитывать в новой имплементации? Можем ли мы заменить proxy implementation от OpenZeppelin NFT токена на ERC20 имплементацию?
- Какие функции есть в Openzeppelin Proxy смарт-контракте? Сколько из них имеет selector? Каким образом вызовы перенаправляются в имплементацю?
- Расскажите о стандарте ERC1967? Какая основная идея стандарта? Какой способ хранения слотов используется в этом стандарте? И почему?
- Какие типы proxy вы значете? Расскажите идею каждого. В каких протоколах и контрактах используются эти паттерны?
- Расскажите о паттерне inherited storage. Как структурирован storage импелементации? Каким образом слоты storage располагаются при наследовании? Порядок A: B and C? Как определить порядок при множестевнном наследовании A: B and D, B: C, D: C?
- Для чего используются gap переменные?
- Расскажите о паттерне инициализации смарт-контрактов. Зачем он нужен если есть конструктор? Для чего используется в proxy?
- Расскажите об аттаке захвата имплементации proxy. Почему важно иницилизировать proxy? В каких случаях захват может привести к проблемам? Как защититься?
- Что такое и как работает Ethernal storage?
- Расскажите о Unstructured storage? Как работает? Какие преимущества и недостатки? Как гарантировать отсутствие коллизиий при большом кол-ве переменных? Расчитайте вероятность колизии при использовании unstructured storage для хранения 1_000 слотов.
- Что такое Beacon? Зачем нужен, если есть обычный слот для implementation?
- Раскажите как работает TransaparentProxy. Как контракт понимает куда адресовать вызовы(в proxy или в implementation)? Какие проблемы могут быть при коллизиии селекторов? Как их избежать?
- Раскажите как работает UUPS. Как контракт понимает куда адресовать вызовы(в proxy или в implementation)?
- Что такое Oracle? Какую проблему решают? Какие данные можно получать? Приведите примеры популярных оракулов.
- Почему на блокчейне нельзя получить данные из вне?
- Как оракулы гарантируют надежность предоставляемых данных? Для чего используются и как работают P2P сети оракулов?
- Расскажите о Chainlink Price Feed. Какие данные предоставляют? Как часто обновляют данные, откуда собирают данные?
- Какие полпулярные протоколы используют оракулов и для чего?
- Расскажите о базовой архитектуре оракулов.
- Расскажите как работают onchain оракулы цены. Каким образом оракулы гарантируют надежность данных о цене не запрашивая их из вне?
- Что такое TWAP оракул? Как работает? Приведите примеры популярных реализаций?
- Расскуажите об аттаке манипуляции ценой оракула. За счет чего происходит? Как защититься? Приведите примеры популярных протоколов которые были аттакуованы этим способом.
- Как работает CREATE, CREATE2 развертывание контрактов? Каким образом расчитывается адресс развертываемого контракта через CREATE, CREATE2?

##### Tasks

- Напишите ERC-721, где абсолютно любая нфт может быть раздроблена
  на конечное число обычных токенов. Эти взаимозаменяемые токены можно
  отправлять друг другу и делать все что можно делать с обычными
  токенами включая работу с offchain signatures через permit.
  При этом взаимозаменяемые токены каждой NFT являются разными.
  NFT может быть объединена обратно, если у одного адреса больше 95% токенов.  
  Также реализуете методы, которые показывают:
  - Какие целые NFT есть у пользователя
  - Токены каких NFT есть у пользователя
  - Сколько токенов NFT есть у пользователя
- Multisig Wallet: напишите контракт кошелька, требующий нескольких подписей EOA адресов для транзакций.
функции создания кошелька и регистрации участников и параметров, изменение набора подписантов, возможность хранить неодобренные транзакции ждущие подписи, возможность отмены предложенной транзакции.
- Реализуйте максимально контракт общего Vault с возможностью распределения наград между участниками на основе rebase токена.

##### Project task

Разработать DAO для проекта школы.
Предусмотреть `student`, `mentor`, `course owner`, `super admin role`.

На текущем шаге разработать систему проверки и верификации заданий.
Возможность вести несколько отдельных групп студентов параллельно.
Кошельки учеников регистрируются в системе и им выдается роль `student`.
Для части заданий необходима ручная проверка, следовательно mentor должен иметь возможность проверить результаты работы студентов и поставить финальный approve, reject, need fix.
Система стремиться не хранить оценку, а только фактические результаты и уже на основе настраиваемого конфига рассчитывать и выдает оценку через функции.
Рассмотреть возможность переноса данных из разных сетей если задания были задеплоины в сеть отличную от той где развернут DAO.

Написать шаблон контрактов-верификаторов для проверки результатов onchain заданий и необходимые имплементации к ним.
Для offchain заданий пишем микросервис который получает данные о новых выполненных заданиях с блокчейна и либо сам порверяет или посылает уведомление mentor.
Финальный статус по решенному заданию фиксируется в специальном контракте оракула.

Все это покрыть тестами.

Для начала каждый ученик собирает все требования, представляет и утверждает архитектурную схему проекта.
Декомпозирует все на задачи на разработку и выполняет их.

Все контракты должны быть обновляемыми.

В зависимости от кол-ва работы сделаем мини команды, а лучшую имплементацию возьмем за основу.

#### Lesson 5.2: DEX protocols

[Введение в блокчейн 23/24 лекция 6](https://youtu.be/KXzyZoi76yw?si=gznJ6RK1RXN9sglm)

На семинаре повторите написание аналога AMM и разберитесь в основных операциях `swap`, `add liquidity`, `remove liquidity`.

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi: DEX](https://www.youtube.com/watch?v=pRO5YW5qb-k)
  - [DeFi MOOC: DEX](https://www.youtube.com/playlist?list=PLS01nW3RtgopoR-FHiMwfoMLT-opXlfJF)
  - [DeFi: Oracles](https://www.youtube.com/watch?v=vFcW18ZpPZ4)
  - [DeFi MOOC: Oracles](https://www.youtube.com/playlist?list=PLS01nW3Rtgoo70DT2YsBmNUol4134S9C9)
* [Understanding automated market-makers](https://www.paradigm.xyz/2021/04/understanding-automated-market-makers-part-1-price-impact) - must read  
  good article about constant-products, price impacts by Paradigm research
* [Curve white-paper](https://berkeley-defi.github.io/assets/material/StableSwap.pdf) - must read
* Uniswap
  - [UniswapV3 white-paper](https://berkeley-defi.github.io/assets/material/Uniswap%20v3%20Core.pdf) - must read
  - [All about UniswapV3](https://www.youtube.com/playlist?list=PLO5VPQH6OWdXp2_Nk8U7V-zh7suI05i0E)
  - [UniswapV3 book](https://uniswapv3book.com/)
  - [UniswapV3: Architecture Explained](https://www.youtube.com/watch?v=Ehm-OYBmlPM)
  - [UniswapV4 docs](https://docs.uniswap.org/contracts/v4/overview)
* Impermanent loss
  - [What is impermanent loss](https://www.youtube.com/watch?v=8XJ1MSTEuU0) - must read
  - [Impermanent loss](https://docs.balancer.fi/concepts/advanced/impermanent-loss.html) - must read
  - [Balancer Weighted Pools](https://docs.balancer.fi/concepts/pools/weighted.html)
* [Deleveraging Spirals and Stablecoin Attacks](https://berkeley-defi.github.io/assets/material/(In)Stability%20for%20the%20Blockchain.pdf)
* [Authentication data feed for Smart Contracts](https://berkeley-defi.github.io/assets/material/An%20Authenticated%20Data%20Feed%20for%20Smart%20Contracts.pdf)
* Finances
  - [Khan Academy: options, futures, swaps](https://www.khanacademy.org/economics-finance-domain/core-finance/derivative-securities) - must read if you don't understand how work basic financial instrument.  
    videos, explaining different financial instruments
  - [Khan Academy: Inflation](https://www.khanacademy.org/economics-finance-domain/core-finance/inflation-tutorial) - must read if you don't understand how work basic financial instrument.

##### Список вопросов по лекции:

- Какую задачу решают DEX? Приведите примеры популярных протоколов.
- Что такое orderbook? Как работает? Какую информацию содержит ордер? Какие преимущества и недостатки?
- Что такое глубина ликвидности? Что такое спред? Кто maker и taker и кто платит fee?
- Как расчитывается цена оредар в книге заказов?
- Можно ли построить orderbook на смарт-контрактах? Какие могут быть особенности работы?
- Расскажите об основных кокмпонентах onchain, offchain книги заказов. Как размещается ордер? Как заполняется ордер?
- Какие преимущества и недостатки DEX orderbook?
- Что такое AMM? Этот подход содержит offchain компоненты? Где храняться средства?
- Кто такой Liquidity Provider? Какую функцию выполняет? Что такое LP токен и для его используется?
- Что такое Liquidity pool?
- Опишите инвариант constant product? Почему инвариант k должен быть неизменным? При каких операциях инвариант должен быть неизменным: обмены, добавление ликвидности при начальной загрузки ликвидности, добавление ликвидности обычное, удаление ликвидности?
- Как расчитать кол-во получаемых LP? Почему испольщзуется минимальное из соотношений? При начальной загрузки пула total_A = 0 следовательно мы не можем высчитать LP т.к не можем делить на 0. Как обработать этот сценарий?
- Как расчитать кол-во полученных токенов A, B при сжигании LP? Можно ли получить 0 сумму одного из токенов?
- Алиса добавила 1 ETH : 1000 USDC в пул ликвидности. Далее цена впуле поменялась до 2000 USDC за ETH. Какое кол-во токенов Алиса получит при выводе всей ликвидности?
- Как расчитать dX или dY для CP? Графическое отображение имеет асимптоты x, y: Какие свойства обмена это дает?
- Как расчитать моментальную цену пула в CP? От чего зависит?
- Как пул взимает комиссии при обмене?
- Пул имеет резервы 144 ETH и 528500 USDC. Алиса производит обмен 176 USDC. Расчитайте кол-во полученного ETH и основе состояние пула. Далее боб обменивает 0.4 ETH. Расчитайте кол-во полученного ETH и основе состояние пула. Все расчеты производите с учетом fee пула в 0.3%.
- Что такое slippage? Что такое price impact? В чем разница?
- Как расчитать цену обмена в CP с учетом slippage?
- В чем разнца ожидаемого и неожидаемого проскальзывания? Чем это может быть опасно для трейдера?
- Можем ли мы получить 0 выходную сумму при проскальзывании?
- Как защититься от slippage?
- Что такое sandwitch attack? Опишите механизм работы. Когда происходит? Как защититься?
- Что такое stable / pegged asset?
- Расскажите об идее обменов stable assset. Почему CPAMM плохо подходит? Можно ли использовать формулу Constant price = x + y = k?
- Опишите формулу инварианта которую Curve используется для обмена. Расскажите основные подходы итоговой формулы.
- В чем отличия Uniswap V2 от V3?
- Что такое impermanent loss? При каких условиях происходит? Приведите пример с расчетами демонструрующий проблему.
- Как расчитать величину impermanent loss?
- Что такое concentrated liquidity? В чем основаня идея? Что происходит на границах диапазона цены?
- Объясните идею виртуальной ликвидности. Для чего делают сдвиг от реальных резервов?
- Опишите формулы virtual & real reserves.
- Почему в UniswapV3 при внесении ликвидности мы получаем NFT а не LP токены?
- Может ли цена AMM сильно отличаться от реальной на бирже?
- Как  происходит Arbitrage AMM? Для чего нужен? Кто получает profit и loss.
- Пул имеет резервы 128 ETH и 483840 USDC, цена на CEX бирже 4000 USDC за ETH. Расчитайте суммы и последовательность действий для арбитража.
- Можно ли использовать цену DEX как цену для оракула? Когда можно использовать, какие есть риски?

##### Tasks

- Напишите бек, который будет искать наиболее оптимальные пути обмена в Uniswap.
  Есть токены A, B, C. Необходимо сделать наиболее эффективный обмен через A -> B.
  Задача комевояжера.
  Нужно составить матрицу и по ней определить будет ли A->C->B, более выгоден чем A->B.
  Поддержать от 10 пулов с разными токенами и маршрутами.
- Реализуйте механизм автоматической ребалансировки ликвидности для UniswapV4 на основе хуков.
  Изначально поставщик ликвидности настраивает паттерн распределения ликвидности по тикам Uniswap и загружает ликвидность.
  В пуле могут происходить обмены и менять центр ликвидности.
  Администратор может отцентровать всю ликвидность или изменить паттерн, а также настроить параметры отклонения цены при которых происходит ребалансировка.
  Необходимо вычислять сколько будет поглощено обменом, сколько ликвидности уже есть в пуле и сколько нужно добавить.

#### Lesson 5.3: Lendings protocols

[Введение в блокчейн 23/24 лекция 7](https://youtu.be/M6AKpEwkwRE?si=iDZOA8jutGnrK4na)

На семинаре повторите написание аналога Lending protocol и разберитесь в основных операциях `deposit`, `withdraw`, `borrow`, `repay`, `liquidate`.

Попробуйте решить задачку из лекции и поделиться решением с ментором, до просмотра решения.

```
Assume you are a user interested in investing in the DeFi lending protocol, Compound
V3. Your task is to calculate the potential profit you could earn over a period of 3
months (92 days).
You have decided to invest 5 ETH. The current base interest rate per Ethereum block is
0.00003% (consider a block every 12 seconds), the slope low multiplier applied by
Compound is 0.001%, total borrows in the protocol are 100,000 ETH and total supply is
200,000 ETH. Consider all parameters remain constant throughout the period.
```

##### Список вопросов по лекции:

- Какую задачу решают Lending protocol?
- Почему lender обязан предоставлять collateral чтобы взять loan?
- Что такое leverage? От чего зависит размер кредитного плеча, который можно взять в lending protocol? Какое максимальное плечо можно взять в AAVE или Compound?
- У вас есть токены USDC. Как встать в LONG по ETH с плечом через lending protocol? Опишите порядок и операции необходимых для этого.
- У вас есть токены USDC. Как встать в SHORT по ETH с плечом через lending protocol? Опишите порядок и операции необходимых для этого.
- Какие основные типы сущности/участники Lending protocol их роли и задачи. Lender, borrower, liquidator, oracle.
- Что такое collateral? Для чего нужен?
- Что такое liquidity pool? При осуждении DEX вы можете часто слышать о liquidity pool, в чем разница с lending protocol?
- Что такое interest rate? Как рассчитывается?
- Что такое LTV? От чего зависит?
- Что такое ликвидация? Когда позиция может быть ликвидирована? Какая последовательность действий? Как зарабатывает ликвидатор? Ликвидируется всю позицию пользователя(от чего зависит)?
- Что такое bad dept? Что такое poisoned position?
- Что такое health factor? Как рассчитывается? Рассчитывается по value $ или кол-ву токенов в позиции?
- Для чего нужен liquidation threshold? Можно ли сделать liquidation threshold 0% или 100%? Какие могут быть риски? От чего зависит?
- Что такое over-collateralized lending?
- Можно ли реализовать идею under-collateralized lending на блокчейне? Какие ограничения могут быть?
- Пользователь имеет 2000 DAI в обеспечении, занял 1.25 ETH, цена ETH 1500 расcчитайте health factor, liquidation threshold 0.8. Цена ETH увеличилась на 24% расcчитайте health factor. Цена ETH увеличилась на 48% расcчитайте health factor. В каких случаях позиция стала ликвидируемой?
- Что такое liquidation spread? Как рассчитывается?
- Что такое close factor? Как рассчитывается? Почему обычно не вся позиция ликвидируется?
- Приведите расчеты демонстрирующие что частичная ликвидация позиции повышает health factor позиции.
- В чем сложность быть ликвидатором? Когда появляется возможно ликвидации позиции на блокчейне?
- Пользователь имеет 2000 DAI в обеспечении, занял 1.4 ETH, цена ETH 1500, liquidation threshold 0.75, liquidation spread 0.1, close factor 0.5. Расcчитайте health factor(до и полсе ликвидации), приведите расчеты ликвидации.
- Расскажите об идее ликвидаций на основе english auction? В чем преимущества и недостатки?
- Расскажите об идее ликвидаций на основе dutch auction? В чем преимущества и недостатки?
- Дайте определение flashloan. Каким образом пользователь может получить огромное кол-во средств без залога? Какое ограничения на возврата долга?
- Какие применения могут быть у flashloan?
- Есть 2 пула ETH/DAI в разных DEX: цена в первом 1500 DAI/ETH, цена во втором 1400 DAI/ETH. Приведите расчеты арбитража пулов используя flashloan.
- Как вычисляется interest rate в Compound?
- Что такое isolated position в протоколе займа?
- Почему AAVE, Compound предоставляют только токены из разрешенного списока для займа, а не любые?
- Что такое utilization? Как рассчитывается? Как выглядит график утилизации Compound V3? Что такое Kink кривая? Для чего нужна?
- Что такое rebase token? Поясните алгоритм работы на примере cToken проекта Compound. Какие популярные rebase токены вы знаете и для чего они используются?
- Расскажите об основной идее работы протокола Maker DAO.

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi: Lending](https://www.youtube.com/watch?v=dKk9rGWDoTI) 
  - [Liquidations](https://berkeley-defi.github.io/assets/material/Liquidations.pdf)
* Compound
  - [Compound documentation](https://docs.compound.finance/) - must read
  - [Understanding Compound liquidation](https://zengo.com/understanding-compounds-liquidation/) - must read     
    detailed article about Compound mechanics for liquidators
- [AAve v2 documentation](https://docs.aave.com/developers)
* Flashloans
  - [How to Make a Flash Loan using Aave](https://www.quicknode.com/guides/defi/lending-protocols/how-to-make-a-flash-loan-using-aave) - must read   
    workshop to take flashloan from AAVE (helps to understand flashloan usage flow)
  - [Attacking the DeFi Ecosystem with Flash Loans for Fun and Profit](https://berkeley-defi.github.io/assets/material/Attacking%20DeFi%20With%20Flash%20Loans.pdf)
* Finances
  - [Khan Academy: Interest and debt](https://www.khanacademy.org/economics-finance-domain/core-finance/interest-tutorial) - must read if you don't understand how work basic financial instrument.

##### Дополнительные ссылки: DeFi extras

Информация и ссылки о важных DeFi протоколов. Эти протоколы не входят в курс,
поэтому можно использовать для самостоятельного изучения.  

* Stablecoins
  - [MakerDAO explained](https://hackernoon.com/whats-makerdao-and-what-s-going-on-with-it-explained-with-pictures-f7ebf774e9c2)  
    article with examples and graphics, explaining how MakerDAO works
  - [DAI explained](https://www.youtube.com/watch?v=wW1IEZeWY4k)
  - [DAI whitepaper](https://makerdao.com/en/whitepaper/)
  - [UST explained](https://www.youtube.com/watch?v=U9lrH0loAns)
  - [UST crash](https://ambcrypto.com/luna-ust-postmortem-was-it-a-coordinated-attack-or-a-ponzi/)
* Vaults & yield farming
  - [Yearn finance explained](https://medium.com/iearn/yearn-finance-explained-what-are-vaults-and-strategies-96970560432)  
    good article to understand Yearn vaults

#### Lesson 5.4: Bridges

В этой секции курса смотрим материалы из курса Berkley.

##### Список вопросов по материалам:

- Какую задачу решают мосты для блокчейн экосистем?
- Могут ли блокчейны коммуницировать нативно друг с другом без использования моста? Какие условия для этого необходимы?
- Что такое interoperability применимо к блокчейнами?
- Что такое composability применимо к блокчейнами?
- Мосты нужны только для передачи токенов между блокчейнами? Приведите примеры других типов переноса информации и взаимодействия.
- Что такое XCMP, IBC?
- Расскажите об архитектуре и принципах работы Federate Bridge. Для чего валидаторам моста необходимо блокировать обеспечение? Какую функцию выполняют bridge address? Какую функцию выполняют bridge contract? Какой алгоритм действий чтобы переместить актив через мост и вернуть обратно?
- Какие преимущества и недостатки есть у активов pegged токенов переданных через мост? Почему цена обернутого актива, как правило, немного меньше чем нативного?
- Расскажите о всех потенциальных security concern для Federate Bridge.
- Расскажите о принципах работы Lock and Mint мостов. В чем суть? Какие стороны есть? Как перемещаются активы? Какие могут быть риски? Приведите 2-3 примера мостов использующих этот принцип.
- Расскажите как работает перемещение для централизованных эмитентов активов на примере WBTC. В чем преимущества и риски?
- Расскажите что такое sidechain? Принцип работы. Приведите 2-3 популярных примеров.
- Расскажите происходит перемещение токенов через мост Axelar? Какие основные участники представляют работу моста? Какие функции нужно вызвать при переводе токенов из ETH -> Avalanche?

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi MOOC: Interchain Interoperability](https://www.youtube.com/watch?v=iBNzPk7q9_0&list=PLS01nW3RtgopFiRQiM-onPH38S0D2DU31&index=5)
* Курс Berkley(необязательное)
  - [Decentralized Identity](https://www.youtube.com/watch?v=3FL-1HMKvYA)
  - [DeFi MOOC Lecture 11: Decentralized Identities](https://www.youtube.com/playlist?list=PLS01nW3RtgoqeqwxBvpe30OXwdMQ5khWi)
* [Alexar Docs](https://docs.axelar.dev/dev/intro/) - must read
* [Bridges for DeFi](https://blog.makerdao.com/what-are-blockchain-bridges-and-why-are-they-important-for-defi/) - must read

##### Task

Написать контракт, который из вашего студенческого кошелька передаст сообщение "ITMChain1024" и токены в одной транзакции Ethereum -> Avalanche.
Через мост [Axelar](https://www.axelar.network/).

#### Lesson 5.5: Layer 2 solutions

В этой секции курса смотрим материалы из курса Berkley.

##### Список вопросов по материалам:

- Какая пропускная способность сетей ETH, BTC? Почему такая низкая?
- Как пропускная способность связана с transaction fees?
- Какие основные цели преследует задача масштабирования блокчейна?
- Какие способы масштабирования блокчейна вы знаете? Расскажите кратко о каждой из идей.
- Каким образом множество транзакций упаковываются в одну посредством L2?
- Расскажите об архитектуре и принципах работу payment channels? За счет чего достигается повышение скорости работы?
- Как работает Hashed TimeLock контракт? В каких случаях следует использовать закрытие канала с подписью Alice? В каких случаях следует использовать закрытие канала с подписями Alice & Bob?
- Почему не обязательно публиковать каждую транзакцию payment chanel в блокчейне? Когда участники payment channel взаимодействуют с блокчейном?
- Расскажите об архитектуре и принципах работы двунаправленного payment channel?
- Расскажите в чем основная идея Rollup? Какие есть участники сети? Какие задачи выполняют?
- Какие действия выполняет zk coordinator rollup(sequencer)? Какие данные необходимо собрать координатору чтобы сформировать SNARK proof? Какие базовые проверки необходимо сделать? Какие данные необходимо опубликовать в L1?
- Почему транзакции внутри rollup дешевые, а когда переводишь между L2 <=> L1 дорогие?
- Как хранятся данные работы rollup сетей в блокчейне Ethereum?
- Где хранятся подробные данные обо всех блоках L2?
- Расскажите как работают optimistic rollup? В чем особенности и какие есть ограничения? Приведите примеры Optimistic L2.
- Что такое sequencer/coordinator? Для чего coordinator должен предоставить обеспечение? Когда обеспечение может быть оштрафовано?
- Почему перевод токенов между L2 optimistic и L1 имеет задержку?
- Что такое data availability layer? Для чего используется и какую проблему решает?
- Расскажите идею подхода zkSync? Где хранятся данные? Преимущества и недостатки.
- Расскажите идею подхода zkPorter? Где хранятся данные? Преимущества и недостатки.

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi MOOC: Scaling Blockchains](https://www.youtube.com/watch?v=jnd5EGx6i-Q&list=PLS01nW3RtgopFiRQiM-onPH38S0D2DU31&index=4)
* [Layer2 overview](https://github.com/LearnWeb3DAO/Layer2) - must read state channel, side chain, rollup.
* [Ethereum L2 rollups](https://medium.com/interdax/ethereum-l2-optimistic-and-zk-rollups-dffa58870c93)
* [The Case for Ethereum Scalability](https://medium.com/connext/the-case-for-ethereum-scalability-d2a8035f880f)
* [Bitcoin Lightning](https://berkeley-defi.github.io/assets/material/lightning-network-paper.pdf)

##### Task

Напишите контракт, который из вашего студенческого кошелька перенесет ETH в один из L2 optimistic rollup.  
На принимающей стороне напишите контракт, который проверяет в конструкторе, что адрес уже имеет необходимую сумму на балансе и только тогда успешно развертывается.  
Отправьте еще одно сообщение, в котором fallback & receive функция всегда возвращается. Попробуйте отправить ETH на этот аккаунт. 

### Lesson 6.1: Practical Smart Contract Security

В этой секции курса смотрим материалы из курса Berkley.

В рамках лекции и разбора багов, сначала изучите предоставленные репозитории на указанных коммитах, чтобы понять основную логику работы контракта.
А дальше вместе с Sam попробуйте разобраться в причине и способах устранения ошибки.

##### Список вопросов:

- Что означает безопасность для пользователя и для разработчика?
- Что такое безопасный перевод?
- Какие риски создает перевод ERC-721?
- Почему к любым внешним вызовам следует всегда относиться как к потенциально небезопасными?
- Что происходит на уровне смарт контракта и EVM при выполнении внешнего вызова? Что может сделать атакующий получив контроль исполнения? Приведите 3 примера реальных хаков завязанных на внешний вызов.
- Расскажите о паттерне check-effect-interaction?
- Как отличить безопасный или небезопасный внешний вызов?
- В чем опасность внешних вызовов до изменения состояния контракта?
- В чем опасность внешних вызовов если вызывающий контракт не содержит проверок состояния?
- Какую задачу решают контакты ENS Name Wrapper?
- Расскажите по шагам и покажите в коде в чем суть уязвимости ENS Name Wrapper? Как защититься или исправить проблему?
- Расскажите по шагам и покажите в коде в чем суть уязвимости Hashmasks? Как защититься или исправить проблему?
- Какие тактики поиска уязвимостей вы знаете?
- Расскажите по шагам и покажите в коде в чем суть уязвимости Ambisafe? Как защититься или исправить проблему?
- Расскажите о времени жизни транзакции в реальном блокчейне? Какие есть фазы, когда происходит переход между фазами? Какие потенциальные уязвимости могут быть на разных этапах? Приведите примеры.
- Для чего используются приватные mempool? Что и себя представляет сервис который, предоставляет защищенный mempool?
- Что такое exploit chaining?
- Расскажите по шагам и покажите в коде в чем суть уязвимости Pickle Finance? Как защититься или исправить проблему?
- Почему Duck typing не работает в блокчейне?
- Зачем контрактам нужна оптимизация? Почему это важно в контрактах?
- Какие способы оптимизации вы знаете? Какие части контракта следует оптимизировать?
- Расскажите по шагам и покажите в коде в чем суть уязвимости 0xExchangeV2? Как защититься или исправить проблему?
- Расскажите по шагам и покажите в коде в чем суть уязвимости EnsRegistry? Как защититься или исправить проблему?
- Какие уязвимости могут происходить при взаимодействии между блокчейнами? В чем сложность такого взаимодействия?
- Расскажите по шагам и покажите в коде в чем суть уязвимости AtomicLoans? Как защититься или исправить проблему?
- Расскажите об уязвимости ABI Hash Collisions? Когда возникает? Как защитится/исправить проблему?
- Расскажите об уязвимости Ambiguous Evaluation Order? Какие бывают? Когда возникает? Как защитится/исправить проблему?
- Расскажите об уязвимостях Approval Vulnerabilities¶? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимостях Exposed Data? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимостях Frontrunning? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимостях Griefing Attacks? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимости Incorrect Parameter Order? Когда возникает? Как защитится/исправить проблему?
- Расскажите об уязвимостях Oracle Manipulation Attacks? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимостях Reentrancy? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимостях Signature-related Attacks? Какие бывают? Когда возникают? Как защитится/исправить проблему?
- Расскажите об уязвимости Unexpected Ether Transfers (Force Feeding)? Когда возникает? Как защитится/исправить проблему?

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi MOOC Lecture 12: Practical Smart Contract Security](https://www.youtube.com/playlist?list=PLS01nW3Rtgoos65Y38qr9is9fqnoJ2tmU)
  - [DeFi Lecture 12: Practical Smart Contract Security](https://www.youtube.com/watch?v=pJKy5HWuFK8)
* [Smart Contract Security Field Guide](https://scsfg.io/hackers/) - must read
* [Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/) - must read

##### Task

https://damnvulnerabledefi.xyz/ - 1-8 задача.  
Если задачи Statemind Hack CTF Education станут open-source, using approved заменить на них.

### Lesson 6.1: DeFi Security

В этой секции курса смотрим материалы из курса Berkley.

С 1:03:30 представлены примеры смарт-контрактов при просмотре попробуйте ставить паузу и отлавливать уязвимости самостоятельно.
А далее проверять с лектором.

##### Список вопросов:

- Расскажите как транзакции распространяются по блокчейн сети? В чем отличие full node от майнеров?
- Для чего атакующий размещает Spy Node?
- Что такое front-running? Приведите примеры front-running атак?
- Каким образом разместить транзакцию перед транзакцией жертвы?
- Что такое back-running? Приведите примеры back-running атак?
- Каким образом разместить транзакцию сразу после транзакции жертвы?
- Что такое sandwich? Приведите примеры sandwich атак? Как защититься? Как slippage связан с атакой? Какие есть способы защиты/минимизации slippage?
- Что такое Eclipse Attacks? Как происходит? Можно ли защититься? Какие условия необходимо выполнить атакующему?
- Расскажите об атаке Double Spending. В чем суть? Когда происходит? Как защитится?
- Почему node не запрашивает данные за несколько периодов одновременно? В чем причина?
- Расскажите об атаке Selfish Mining. В чем суть? Какое влияние оказывает на мощность при майнинг в пулах?
- Расскажите об атаки The DAO? Когда возникает? Как защитится/исправить проблему?
- Расскажите по шагам и покажите в коде в чем суть The DAO attack? Как защититься или исправить проблему? Как исправили проблему в Ethereum?
- Что такое Flash-loan Attack?
- Расскажите по шагам о bZx Pump and Arbitrage Attack? Какие займы и обмены происходят и в каком порядке? На каком этапе возникает profit у атакующего?
- Расскажите по шагам о bZx Oracle Manipulation? Как злоумышленник смог изменить цену оракула? На каком этапе возникает profit у атакующего? Как можно было защитится?
- Что такое MEV? Какие участники сети влияют на MEV? Как MEV проявляется в ликвидациях или арбитраже?

##### Дополнительные ссылки:

* Курс Berkley
  - [DeFi Lecture 13: DeFi Security](https://www.youtube.com/watch?v=GIHa2GQJY1k)
  - [DeFi MOOC Lecture 13: DeFi Security](https://www.youtube.com/playlist?list=PLS01nW3RtgopsMpAceFwuyLKH42VW0Nw9)
* [Tornado cash white-papaer](https://berkeley-defi.github.io/assets/material/Tornado%20Cash%20Whitepaper.pdf)
* Blogs to read
  - [Cmichel blog](https://cmichel.io/)  
    many hacks replayed and explained
  - [samczsun blog](https://samczsun.com/)  
    articles about security

##### Task

https://damnvulnerabledefi.xyz/ - 9-18 задача.  
Если задачи Statemind Hack CTF Education станут open-source / using approved заменить на них.

Живые маленькие контракты, чтобы найти студенты во время беседы с ментором нашли уязвимости в контракте.

## Tools

* Toolchain & Tools
  - [Foundry](https://book.getfoundry.sh/) - the best toolchain in Solidity for Solidity
  - [Hardhat](https://hardhat.org/) - the most common toolchain in JS
  - [Tenderly](https://tenderly.co/)   
    Contracts testing, transactions analyzer,debugger, monitor
* IDE
  - [Remix IDE](https://remix.ethereum.org/) - for simple contract or fast check
  - [IDEA Solidity plugin](https://plugins.jetbrains.com/plugin/9475-solidity)
  - [VSCode Solidity Auditor plugin](https://marketplace.visualstudio.com/items?itemName=tintinweb.solidity-visual-auditor&ssr=false#overview)
* Tutorials and courses
  - [Foundry playlist](https://www.youtube.com/playlist?list=PLO5VPQH6OWdUrKEWPF07CSuVm3T99DQki)
  - [Ethereum Smart Contract Fuzzing overview](https://www.youtube.com/watch?v=RrdrfdtWnSo)
  - [TrailOfBits Fuzzing video-course](https://www.youtube.com/playlist?list=PLciHOL_J7Iwqdja9UH4ZzE8dP1IxtsBXI)
  - [Practice fuzzing testing](https://www.youtube.com/watch?v=83q14K-WNKM)
  - [Foundry book: Testing](https://book.getfoundry.sh/forge/tests)
  - [Foundry book: Fuzzing](https://book.getfoundry.sh/forge/fuzz-testing)
  - [Foundry book: Invariant testing](https://book.getfoundry.sh/forge/invariant-testing)
  - [Foundry book: Gas Report](https://book.getfoundry.sh/forge/gas-reports)


### Job interview

Вопросы по каждой лекции охватывают обширные знания, если студент может ответить на большую часть, то существенная часть дополнительные вопросов
будет понятна или знакома.

Дополнительный список вопросов на интервью:
- [Solidity interview questions](https://www.turing.com/interview-questions/solidity)
- [Blockchain question](https://github.com/SachinCoder1/Learn-blockchain)

### Conclusion

Для курса нужно сделать все обязательные задания к урокам, пройти беседы по каждой из темы + финальное mock интервью с Егором(работаем по хардкору 1 попытка).
Обратная связь и вопросы собираем по ходу всего курса.


Дополнительные варианты задач:
* Маловероятно что зайдет
  - Напишите свою хеш-функцию на Solidity, которая возвращает bytes4 используя только ассемблер внутри тела функции)));
    (Нужно написать определённые фаз тесты для неё тебе будет)
    Проверка: она не должна содержать коллизии для N(1_000_000) миллиона пробегов.




