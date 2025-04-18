[Вернуться к списку вопросов](3.%20Список%20вопросов.md)
## Короткий ответ

**Crash Fault Tolerance (CFT)** — это способность распределённой системы продолжать корректно работать, несмотря на сбои отдельных узлов, если они выходят из строя корректно (т.е. перестают отвечать или работать, но не ведут себя злонамеренно).

---

## Подробный разбор

### Основная идея CFT

1. **Что покрывает CFT?**
   - CFT защищает систему от отказов узлов, которые просто перестают функционировать (например, из-за сбоя оборудования или сети).
   - Не включает защиту от злонамеренного поведения (например, отправки некорректных данных).

2. **Модель сбоев**:
   - Узлы либо работают корректно, либо полностью выходят из строя.
   - Узел, работающий некорректно, в модели CFT не рассматривается.

3. **Механизм работы**:
   - Для обеспечения CFT обычно используются дублирование данных и репликация.

---

### Применение CFT

1. **Распределённые базы данных**:
   - Например, алгоритмы **Raft** и **Paxos** обеспечивают согласованность данных в системе с репликами, даже если некоторые узлы перестают отвечать.

2. **Кластерные системы**:
   - Kubernetes и другие оркестрационные системы поддерживают CFT, распределяя нагрузку между узлами и перезапуская контейнеры на доступных узлах в случае сбоя.

3. **Финансовые системы**:
   - В высоконагруженных системах (например, банковские сети) используются механизмы репликации и автоматического восстановления для обеспечения доступности.

---

### Преимущества CFT

1. **Устойчивость к отказам**:
   - Система продолжает работать, если один или несколько узлов выходят из строя.

2. **Простота реализации**:
   - CFT проще, чем алгоритмы, устойчивые к византийским сбоям (например, PBFT).

3. **Широкое применение**:
   - Подходит для систем, где узлы доверяют друг другу, а злонамеренное поведение маловероятно.

---

### Недостатки CFT

1. **Ограниченность модели**:
   - Не защищает от злонамеренных узлов.
   - Подходит только для безопасных окружений (например, корпоративных сетей).

2. **Зависимость от репликации**:
   - Увеличение числа реплик повышает затраты на хранение и обработку.

---

### Примеры систем с CFT

1. **Raft**:
   - Устойчив к отказам узлов, но не защищён от злонамеренного поведения.
   - Используется в системах типа Consul или Etcd.

2. **Paxos**:
   - Алгоритм для согласования данных между репликами.
   - Защищает от сбоев при условии, что большинство узлов остаются работоспособными.

---

### Связанные темы

- [[Что такое консенсус алгоритм? Для чего он нужен и какую задачу выполняет?]]
- [[Что такое BFT(как метрика)?]]
- [[Расскажите о механизме работы консенсуса Paxos. Какие основные роли и взаимодействие?]]

---

### Источники

1. [Raft Consensus Algorithm](https://raft.github.io/)
2. [Paxos Explained](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
3. [Distributed Systems Basics](https://distributed-systems.net)

---