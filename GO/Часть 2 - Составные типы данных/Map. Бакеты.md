# Бакеты

## Краткий обзор

Бакеты (buckets) в Go — это основные структурные блоки хеш-таблицы, составляющие внутреннюю реализацию map. Каждый бакет способен хранить до 8 пар ключ-значение и имеет оптимизированную структуру памяти для улучшения производительности кеш-процессора. Особенностью реализации является группировка однотипных данных: сначала массив хеш-значений (tophash), затем массив ключей, затем массив значений, и в конце — указатель на overflow-бакет. Эффективность работы с бакетами достигается за счёт оптимизации локальности данных, быстрой фильтрации по tophash и минимизации количества проверок на полное совпадение ключей. При заполнении бакета создаются overflow-бакеты, образующие связанные списки для разрешения коллизий.

## Подробный разбор

### Структура бакета

Бакет в Go map представляет собой структуру данных, способную хранить до 8 пар ключ-значение. Внутренняя структура бакета определена в исходном коде Go следующим образом:

```go
// Упрощенное представление структуры бакета из runtime/map.go
type bmap struct {
    // tophash содержит 8 верхних байтов хеша соответствующих ключей
    // или специальные маркеры для пустых и удаленных ячеек
    tophash [bucketCnt]uint8
    
    // В реальности за этим следуют неявные поля:
    // keys    [bucketCnt]keytype      // хранилище ключей
    // values  [bucketCnt]valuetype    // хранилище значений
    // overflow *bmap                  // указатель на следующий бакет при переполнении
}
```

Где `bucketCnt` равен 8 — это константа, определяющая максимальное количество элементов в бакете.

### Оптимизация размещения данных

Ключевой особенностью бакетов в Go является оптимизированная компоновка данных для эффективного использования кеша процессора:

```
Область памяти бакета:
+---------------+---------------+---------------+---------------+
| tophash[0..7] | keys[0..7]    | values[0..7]  | overflow_ptr  |
+---------------+---------------+---------------+---------------+
```

В отличие от традиционных реализаций, где каждая пара ключ-значение хранится вместе, Go размещает все компоненты одного типа последовательно:

1. Все хеш-метки `tophash` (8 байт) — для быстрого сканирования
2. Все ключи (8 * размер_ключа байт) — вместе
3. Все значения (8 * размер_значения байт) — вместе
4. Указатель на overflow-бакет (8 байт на 64-битных системах)

```go
// Псевдокод получения адреса ключа и значения в бакете
func keyaddr(b *bmap, i uint8) unsafe.Pointer {
    return unsafe.Pointer(uintptr(unsafe.Pointer(b)) + dataOffset + uintptr(i)*keysize)
}

func valueaddr(b *bmap, i uint8) unsafe.Pointer {
    return unsafe.Pointer(uintptr(unsafe.Pointer(b)) + dataOffset + bucketCnt*keysize + uintptr(i)*valuesize)
}
```

Преимущества такой компоновки:

1. **Улучшение пространственной локальности**: близкие по доступу данные находятся рядом в памяти
2. **Эффективное использование кеш-линий**: однотипные данные часто помещаются в одну кеш-линию
3. **Оптимизация предсказания ветвлений**: линейное сканирование массива tophash хорошо предсказуемо

### Выбор бакета по хеш-значению

Процесс выбора бакета для ключа включает несколько шагов:

```go
// Псевдокод выбора бакета
func bucketIdx(h *hmap, hash uintptr) uintptr {
    // Используем только нижние B бит хеша для определения индекса бакета
    // B - это логарифм по основанию 2 от количества бакетов
    return hash & bucketMask(h.B)
}

// bucketMask возвращает маску для выделения B младших бит
func bucketMask(B uint8) uintptr {
    return (1 << B) - 1
}
```

Для map с `2^B` бакетами алгоритм использует нижние B бит хеша для определения индекса бакета. Например:

- Если B = 4, map содержит 16 бакетов, и выбор идёт по 4 нижним битам хеша (маска 0xF)
- Если B = 10, map содержит 1024 бакета, и выбор идёт по 10 нижним битам хеша (маска 0x3FF)

### Работа с tophash

Поле `tophash` играет ключевую роль в оптимизации поиска:

```go
// Вычисление tophash (верхних 8 бит хеша)
func tophash(hash uintptr) uint8 {
    // Берем верхние 8 бит хеша (или минимум значение emptyOne + 1)
    top := uint8(hash >> (ptrSize*8 - 8))
    if top < minTopHash {
        top += minTopHash
    }
    return top
}
```

Значения `tophash` имеют специальные маркеры для особых состояний ячеек:

```go
// Константы для специальных значений tophash
const (
    emptyRest      = 0  // ячейка пуста, и все следующие тоже пусты
    emptyOne       = 1  // ячейка пуста
    evacuatedX     = 2  // ключ/значение действительны, но перемещены в первую часть таблицы
    evacuatedY     = 3  // ключ/значение действительны, но перемещены во вторую часть таблицы
    evacuatedEmpty = 4  // ячейка пуста, и эвакуирована из старого бакета
    minTopHash     = 5  // минимальное нормальное значение tophash
)
```

Эти маркеры позволяют:

1. Быстро определить пустые ячейки
2. Отслеживать эвакуированные элементы при рехешировании
3. Оптимизировать поиск, останавливаясь на `emptyRest`

### Алгоритмы поиска, вставки и удаления

#### Поиск элемента

Алгоритм поиска в бакете оптимизирован для быстрого отсеивания несовпадений:

```go
// Псевдокод поиска ключа в бакете
func mapaccess(h *hmap, key interface{}) (value interface{}, ok bool) {
    // Вычисляем хеш ключа
    hash := alg.hash(key, uintptr(h.hash0))
    
    // Определяем индекс бакета
    bucket := hash & bucketMask(h.B)
    
    // Вычисляем tophash для быстрого сравнения
    top := tophash(hash)
    
    // Получаем указатель на бакет
    b := (*bmap)(add(h.buckets, bucket*uintptr(t.bucketsize)))
    
    // Проверяем oldbuckets при рехешировании
    if h.growing() {
        // ... логика проверки старых бакетов ...
    }
    
    // Итерация по бакету и всей цепочке overflow
    for ; b != nil; b = b.overflow(t) {
        // Проверяем все 8 слотов в бакете
        for i := uintptr(0); i < bucketCnt; i++ {
            // Быстрое сравнение по tophash
            if b.tophash[i] != top {
                // Если это emptyRest, остальные слоты тоже пусты
                if b.tophash[i] == emptyRest {
                    break bucketloop
                }
                continue
            }
            
            // Полное сравнение ключей (только если tophash совпал)
            k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
            if !alg.equal(key, k) {
                continue
            }
            
            // Ключ найден, возвращаем значение
            v := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.valuesize))
            return v, true
        }
    }
    
    // Ключ не найден
    return nil, false
}
```

Этот алгоритм использует двухуровневую фильтрацию:

1. Быстрая проверка по `tophash` (только сравнение байтов)
2. Полное сравнение ключей (только если `tophash` совпал)

#### Вставка элемента

Вставка в бакет требует найти свободное место или определить, что его нет:

```go
// Псевдокод вставки элемента
func mapassign(h *hmap, key, value interface{}) {
    // ... вычисление хеша и определение бакета ...
    
    // Проверка на необходимость увеличения размера map
    if !h.growing() && (overLoadFactor(h.count+1, h.B) || tooManyOverflowBuckets(h.noverflow, h.B)) {
        hashGrow(h)
        // ... обновление указателей после роста ...
    }
    
    // Поиск места для вставки
    var inserti *uint8
    var insertk unsafe.Pointer
    var insertv unsafe.Pointer
    
    for ; b != nil; b = b.overflow(t) {
        for i := uintptr(0); i < bucketCnt; i++ {
            // Если нашли пустую ячейку, запоминаем её
            if b.tophash[i] == emptyOne || b.tophash[i] == emptyRest {
                if inserti == nil {
                    inserti = &b.tophash[i]
                    insertk = add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
                    insertv = add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.valuesize))
                }
                if b.tophash[i] == emptyRest {
                    break bucketloop
                }
                continue
            }
            
            // Проверяем, не существует ли уже такой ключ
            if b.tophash[i] != top {
                continue
            }
            k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
            if !alg.equal(key, k) {
                continue
            }
            
            // Ключ существует, обновляем значение
            v := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.valuesize))
            *v = value
            return
        }
    }
    
    // Если не нашли место для вставки, создаем overflow бакет
    if inserti == nil {
        newb := h.newoverflow(t, b)
        inserti = &newb.tophash[0]
        insertk = add(unsafe.Pointer(newb), dataOffset)
        insertv = add(unsafe.Pointer(newb), dataOffset+bucketCnt*uintptr(t.keysize))
    }
    
    // Вставляем новый элемент
    *inserti = top
    *insertk = key
    *insertv = value
    h.count++
}
```

При вставке Go сначала проверяет, не требуется ли увеличить размер map, затем ищет место в существующих бакетах или создаёт новый overflow-бакет.

### Управление overflow-бакетами

Overflow-бакеты создаются, когда основной бакет заполнен:

```go
// Псевдокод создания overflow-бакета
func (h *hmap) newoverflow(t *maptype, b *bmap) *bmap {
    var ovf *bmap
    
    // Пытаемся использовать предварительно выделенные overflow-бакеты
    if h.extra != nil && h.extra.nextOverflow != nil {
        ovf = h.extra.nextOverflow
        // Проверяем, не последний ли это из предварительно выделенных бакетов
        if ovf.overflow(t) == nil {
            // Последний предварительно выделенный бакет
            h.extra.nextOverflow = nil
        } else {
            // Ещё есть предварительно выделенные бакеты
            h.extra.nextOverflow = ovf.overflow(t)
            ovf.setoverflow(t, nil)
        }
    } else {
        // Предварительно выделенные бакеты закончились, выделяем новый
        ovf = (*bmap)(newobject(t.bucket))
    }
    
    // Увеличиваем счетчик overflow-бакетов
    h.noverflow++
    
    // Присоединяем к текущей цепочке
    b.setoverflow(t, ovf)
    return ovf
}
```

Для оптимизации производительности Go предварительно выделяет некоторое количество overflow-бакетов при создании map, что уменьшает частоту обращений к аллокатору памяти.

### Предварительное выделение overflow-бакетов

При создании или увеличении map, Go может предварительно выделить дополнительные overflow-бакеты:

```go
// Псевдокод предварительного выделения overflow-бакетов
func makeBucketArray(t *maptype, b uint8, dirtyalloc unsafe.Pointer) (buckets unsafe.Pointer, nextOverflow *bmap) {
    base := bucketShift(b)
    nbuckets := base
    
    // Для достаточно больших map выделяем дополнительные overflow-бакеты
    if b >= 4 {
        // Добавляем ~2.5% от основного количества бакетов
        nbuckets += bucketShift(b - 4)
        
        // Округляем до степени 2
        sz := t.bucket.size * nbuckets
        up := roundupsize(sz)
        if up != sz {
            nbuckets = up / t.bucket.size
        }
    }
    
    // Выделяем память под все бакеты
    buckets = newarray(t.bucket, int(nbuckets))
    
    // Настраиваем overflow-бакеты
    if base != nbuckets {
        // Количество overflow-бакетов
        nextOverflow = (*bmap)(add(buckets, base*uintptr(t.bucketsize)))
        // Связываем overflow-бакеты в список
        last := (*bmap)(add(buckets, (nbuckets-1)*uintptr(t.bucketsize)))
        last.setoverflow(t, (*bmap)(buckets))
    }
    
    return buckets, nextOverflow
}
```

Этот механизм:

1. Уменьшает фрагментацию памяти
2. Ускоряет создание overflow-бакетов
3. Оптимизирует локальность памяти для связанных бакетов

## Связи с другими темами

- [[Map. Внутреннее устройство]] — роль бакетов в общей структуре map
- [[Map. Хэширование]] — как хеш-значения используются для выбора бакета
- [[Map. Коллизии. Алгоритмы разрешения коллизий]] — как бакеты помогают разрешать коллизии
- [[Map. Эвакуация]] — как происходит перемещение данных между бакетами при рехешировании
- [[Производительность составных типов]] — влияние структуры бакетов на производительность map

## Источники информации

1. [Go Runtime: map.go](https://github.com/golang/go/blob/master/src/runtime/map.go)
2. [Russ Cox on Go Data Structures](https://research.swtch.com/godata)
3. [Keith Randall's talk on Go Map Internals](https://www.youtube.com/watch?v=Tl7mi9QmLns)
4. [Go Maps Implementation Overview](https://dave.cheney.net/2018/05/29/how-the-go-runtime-implements-maps-efficiently-without-generics)
5. [Go Blog: Maps in Action](https://go.dev/blog/maps)
6. [Deep Dive into Go Maps](https://medium.com/@blanchon.vincent/go-map-design-by-example-part-i-3f78a064a352)
7. [Go Maps Under the Hood](https://www.ardanlabs.com/blog/2013/12/macro-view-of-map-internals-in-go.html)
8. [Memory Layout Optimizations in Go](https://go101.org/article/memory-layout.html)
9. [Optimizing Go Programs by Russ Cox](https://www.youtube.com/watch?v=pLFWagv4Wd0)
