
**Короткий ответ**: Difficulty — это мера сложности задачи для майнеров, выраженная в относительных единицах. Target — это конкретное числовое значение, задающее верхний предел хэша, который должен быть найден. Difficulty и Target взаимосвязаны: чем выше сложность, тем ниже Target.

---

## Подробный разбор

### Определения

1. **Target**:
   - Числовое значение, задающее верхний предел для хэша блока:
     $$
     Hash(BlockHeader) \leq Target
     $$
   - Чем ниже значение Target, тем сложнее найти подходящий хэш.
   - Target изменяется каждые 2016 блоков, чтобы поддерживать стабильное время создания блока (~10 минут).

2. **Difficulty**:
   - Относительная метрика, показывающая, насколько сложнее находить блоки по сравнению с самой простой сложностью (difficulty = 1).
   - Вычисляется как:
     $$
     Difficulty = \frac{Maximum\ Target}{Target}
     $$
   - **Maximum Target** — это самое большое значение Target, соответствующее минимальной сложности (difficulty = 1). Оно фиксировано протоколом Bitcoin.

---

### Как они связаны?

- **Maximum Target**:
  - В Bitcoin Maximum Target равен \( 0x1d00ffff \) в шестнадцатеричном формате.
  - Это эквивалентно \( 2^{224} - 1 \) в десятичном формате.
  
- Пример связи:
  - При difficulty = 1:
    $$
    Target = Maximum\ Target
    $$
  - При difficulty = 10:
    $$
    Target = \frac{Maximum\ Target}{10}
    $$
  - Чем выше difficulty, тем меньше Target и тем сложнее найти хэш.

---

### Пример

#### Для Maximum Target (\( 0x1d00ffff \)):
- Это самое простое состояние, где difficulty = 1.
- Хэш блока должен быть меньше или равен:
  $$
  0x1d00ffff = 2^{224} - 1
  $$

#### При difficulty = 2:
- Target уменьшается вдвое:
  $$
  Target = \frac{Maximum\ Target}{2}
  $$
- Значение Target: \( 2^{223} - 1 \).

#### При difficulty = 10:
- Target уменьшается в 10 раз:
  $$
  Target = \frac{Maximum\ Target}{10}
  $$
- Значение Target: \( 2^{224} / 10 \).

#### Вывод:
- Чем выше сложность, тем ниже Target, что делает поиск подходящего хэша более трудным.

---

### Регулировка сложности

1. **Почему нужна регулировка?**
   - Чтобы поддерживать стабильное время создания блока (~10 минут), независимо от изменения вычислительных мощностей в сети.

2. **Как изменяется сложность?**
   - Каждые 2016 блоков (~2 недели) сложность пересчитывается:
     $$
     New\ Difficulty = Current\ Difficulty \times \frac{Actual\ Time}{Expected\ Time}
     $$
   - Если блоки создавались быстрее 10 минут, сложность увеличивается.

---

### Пример с блоками

1. Текущее время на создание 2016 блоков: 14 дней.
2. Ожидаемое время: 10 минут на блок × 2016 блоков = 14 дней.
3. Если фактическое время меньше:
   - Сложность увеличивается.
   - Target уменьшается.

---

### Связанные темы
- [[Какую математическую задачку решают майнеры в POW консенсусе? Что конкретно они делают и какие критерии правильности решения задачи?]]
- [[Nonce 4 байт, значения могут быть от 0 to 4,294,967,295. Что делать если перебрали все nonce, но не решили математическую задачку?]]
- [[Как происходит создание блока?]]

---

### Источники
1. [Bitcoin Developer Guide: Difficulty](https://bitcoin.org/en/developer-guide#difficulty)
2. [Target and Difficulty Explained](https://en.bitcoin.it/wiki/Difficulty)
3. [Mastering Bitcoin by Andreas M. Antonopoulos](https://github.com/bitcoinbook/bitcoinbook)