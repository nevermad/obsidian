# Пакет builtin. Операции new / make

## Краткий обзор

Пакет `builtin` в Go содержит предварительно объявленные идентификаторы (встроенные типы, функции и константы), встроенные в язык. Функции `new()` и `make()` - ключевые операции выделения памяти в Go: `new()` выделяет память и инициализирует ее нулевым значением, возвращая указатель, а `make()` инициализирует и возвращает непустой экземпляр `slice`, `map` или `channel`. Понимание внутренней реализации и особенностей этих операций критически важно для высокопроизводительных Go-программ.

## Подробный разбор

### Пакет builtin

Пакет `builtin` - не совсем обычный пакет. Фактически, он является частью компилятора Go и содержит предварительно объявленные идентификаторы:

```go
// псевдо-описание пакета
package builtin

// Базовые типы
type bool bool
type byte = uint8
type rune = int32
type int int
type int8 int8
type int16 int16
type int32 int32
type int64 int64
type uint uint
type uint8 uint8
type uint16 uint16
type uint32 uint32
type uint64 uint64
type uintptr uintptr
type float32 float32
type float64 float64
type complex64 complex64
type complex128 complex128
type string string
type error interface { Error() string }

// Составные типы
type Array [0]byte           // только для документации
type Slice []byte            // только для документации
type Map map[string]int      // только для документации
type Chan chan int           // только для документации
type Func func()             // только для документации

// Встроенные функции
func new(Type) *Type
func make(t Type, size ...IntegerType) Type
func append(slice []Type, elems ...Type) []Type
func copy(dst, src []Type) int
func delete(m map[Type]Type1, key Type)
func len(v Type) int
func cap(v Type) int
func close(c chan<- Type)
func complex(r, i FloatType) ComplexType
func real(c ComplexType) FloatType
func imag(c ComplexType) FloatType
func panic(v interface{})
func recover() interface{}
func print(args ...Type)
func println(args ...Type)

// Константы
const true = 0 == 0
const false = 0 != 0
const iota = 0
const nil = nil
```

#### Особенности пакета builtin

1. **Не требует импорта**: Идентификаторы из пакета `builtin` доступны в любом файле Go без импорта.

2. **Документационная цель**: Основная цель этого пакета - документирование встроенных типов и функций.

3. **Псевдо-реализация**: Некоторые типы (как Array, Slice) определены только для документации.

4. **Недоступный исходный код**: Реальная реализация встроенных функций встроена в компилятор и рантайм Go.

#### Малоизвестные функции пакета builtin

Помимо широко используемых функций, есть несколько менее известных или устаревших:

1. **print/println**: Низкоуровневые функции отладки, не рекомендуемые для обычного использования. Они обходят стандартные механизмы форматирования.

   ```go
   print("Debug:", x) // Выводит напрямую на stderr
   ```

2. **complex/real/imag**: Функции для работы с комплексными числами.

   ```go
   c := complex(3.0, 4.0) // 3+4i
   r := real(c)           // 3.0
   i := imag(c)           // 4.0
   ```

### Функция new()

Функция `new(T)` выделяет память для переменной типа T, инициализирует ее нулевым значением (zero-value) и возвращает указатель на нее (`*T`).

```go
p := new(int)    // p имеет тип *int, указывает на 0
*p = 42          // устанавливаем значение по указателю
```

#### Внутренняя реализация new()

На низком уровне, `new()` делает следующее:

1. Определяет размер требуемой памяти для типа
2. Запрашивает выделение этой памяти от системы выделения Go
3. Инициализирует память нулевым значением
4. Возвращает указатель на начало выделенной памяти

Интересно, что `new()` - это встроенная функция, но компилятор часто заменяет ее вызов на прямые инструкции по выделению памяти.

#### Оптимизации компилятора для new()

Компилятор Go выполняет несколько оптимизаций для вызовов `new()`:

1. **Escape Analysis**: Если переменная не "убегает" из функции (например, не возвращается и не сохраняется в глобальной переменной), компилятор может разместить ее на стеке, а не в куче.

2. **Инлайнинг**: Вызов `new()` может быть встроен в код вызывающей функции.

3. **Объединение аллокаций**: Несколько вызовов `new()` для малых объектов могут быть объединены в одну операцию выделения памяти.

#### Практическое применение new()

Функция `new()` обычно используется для создания указателей на:

1. **Простые типы данных**:

   ```go
   p := new(int)
   q := new(bool)
   ```

2. **Структуры**:

   ```go
   type Person struct {
       Name string
       Age  int
   }
   
   p := new(Person) // p указывает на Person{"", 0}
   ```

3. **Массивы**:

   ```go
   arr := new([10]int) // arr имеет тип *[10]int
   ```

#### Эквивалентность &T{...} и new(T)

Для некоторых типов, можно использовать литерал составного типа с адресным оператором `&`:

```go
// Эти выражения эквивалентны
p1 := new(Person)
p2 := &Person{}

// Но литерал позволяет инициализировать поля
p3 := &Person{Name: "Alice", Age: 30}
```

Компилятор Go оптимизирует оба подхода одинаково.

### Функция make()

Функция `make(T, args)` создает и инициализирует объект типа `slice`, `map`, или `channel`.

```go
slice := make([]int, 5, 10)  // slice с len=5, cap=10
m := make(map[string]int)    // пустая map
ch := make(chan bool, 10)    // буферизованный канал
```

В отличие от `new()`, функция `make()`:

1. Работает только с `slice`, `map` и `channel`
2. Возвращает инициализированное значение типа T, а не указатель `*T`
3. Требует специфичные для типа аргументы

#### Внутренняя реализация make() для разных типов

##### Для слайсов (Slice)

```go
slice := make([]T, length, capacity)
```

Внутренняя реализация:

1. Выделяет непрерывный блок памяти размером `capacity * sizeof(T)`
2. Устанавливает указатель на начало этого блока
3. Устанавливает длину (length) и емкость (capacity)

```go
// Внутренняя структура slice
type SliceHeader struct {
    Data uintptr // указатель на базовый массив
    Len  int     // текущая длина
    Cap  int     // емкость
}
```

Когда `capacity` не указана, она равна `length`.

##### Для ассоциативных массивов (Map)

```go
m := make(map[K]V, hint)
```

Внутренняя реализация:

1. Создает структуру с хеш-таблицей
2. Выделяет начальные бакеты (buckets)
3. Устанавливает начальный размер (необязательный аргумент `hint`)

```go
// Упрощенная внутренняя структура map
type hmap struct {
    count     int    // количество элементов
    flags     uint8  // флаги
    B         uint8  // log_2 of buckets count
    noverflow uint16 // количество переполненных бакетов
    hash0     uint32 // seed для хеш-функции
    buckets    unsafe.Pointer // указатель на массив 2^B бакетов
    oldbuckets unsafe.Pointer // предыдущий массив бакетов при расширении
    nevacuate  uintptr       // прогресс эвакуации
    // ...
}
```

##### Для каналов (Channel)

```go
ch := make(chan T, capacity)
```

Внутренняя реализация:

1. Выделяет структуру канала
2. Выделяет кольцевой буфер размером `capacity`
3. Инициализирует мьютексы и структуры ожидания

```go
// Упрощенная внутренняя структура канала
type hchan struct {
    qcount   uint           // количество элементов в очереди
    dataqsiz uint           // размер буфера
    buf      unsafe.Pointer // указатель на кольцевой буфер
    elemsize uint16         // размер элемента
    closed   uint32         // флаг закрытия
    elemtype *_type         // тип элемента
    sendx    uint           // индекс отправки
    recvx    uint           // индекс приема
    recvq    waitq          // список ожидающих получения
    sendq    waitq          // список ожидающих отправки
    lock     mutex          // защищает доступ
}
```

#### Оптимизации для make()

Компилятор Go применяет несколько оптимизаций:

1. **Малые слайсы**: Для слайсов с малой емкостью (обычно < 32 элементов) может использоваться более эффективное выделение.

2. **Предварительное выделение для map**: Предоставление хорошего начального размера map может значительно улучшить производительность.

3. **Оптимизация стека**: Как и для `new()`, компилятор может разместить результат `make()` на стеке, если это безопасно.

#### Практические рекомендации по использованию make()

##### Для слайсов

```go
// Антипаттерн: постепенное наращивание маленькими порциями
s := make([]int, 0)
for i := 0; i < 10000; i++ {
    s = append(s, i) // Много повторных выделений памяти
}

// Лучше: выделение с учётом планируемого размера
s := make([]int, 0, 10000)
for i := 0; i < 10000; i++ {
    s = append(s, i) // Нет повторных выделений
}

// Альтернатива: с предварительным размером
s := make([]int, 10000)
for i := 0; i < 10000; i++ {
    s[i] = i // Прямой доступ по индексу
}
```

##### Для map

```go
// Предварительное выделение для больших map
userMap := make(map[int]User, 10000)

// Антипаттерн: неэффективное использование delete
for k := range userMap {
    delete(userMap, k)
}
// Лучше: создать новую map
userMap = make(map[int]User)
```

##### Для channels

```go
// Небуферизованный канал
ch := make(chan int)

// Буферизованный канал (для уменьшения блокировок)
ch := make(chan int, 100)

// Канал для сигналов (обычно без буфера)
done := make(chan struct{})
```

### Сравнение new() и make()

| Аспект                  | new()                  | make()                |
|-------------------------|------------------------|------------------------|
| Применимость            | Любой тип              | Только slices, maps, channels |
| Возвращаемое значение   | Указатель (*T)        | Значение типа T       |
| Инициализация           | Нулевое значение      | Полная инициализация  |
| Аргументы               | Только тип            | Тип + спец. параметры |
| Размещение              | Стек или куча         | Обычно куча (для больших) |

```go
// Создание слайса с new() - редко используется
p := new([]int)        // p имеет тип *[]int, указывает на nil слайс
*p = make([]int, 10)   // инициализируем слайс через присваивание

// Обычно используется make()
s := make([]int, 10)   // s имеет тип []int, готов к использованию
```

### Взаимодействие с системой управления памятью Go

#### Система аллокации памяти в Go

Go использует управляемую среду выполнения с собственным аллокатором памяти:

1. **Tcmalloc-подобный аллокатор**: Основан на ранних версиях Tcmalloc с оптимизациями для Go.

2. **Размерные классы**: Объекты группируются по размерам для эффективной аллокации.

3. **Арена-подход**: Память запрашивается у ОС большими блоками ("арены") по 64KB.

4. **Локальные кэши для горутин**: Каждая P (процессор) имеет локальный кэш для быстрого выделения.

#### Как new() и make() работают с системой аллокации

1. **Малые объекты**: Выделяются из локального кэша процессора.

2. **Средние объекты**: Выделяются из центрального кэша.

3. **Большие объекты** (> 32KB): Выделяются непосредственно из кучи.

Обе функции используют одну и ту же систему выделения памяти под капотом, но с разными параметрами инициализации.

#### Взаимодействие со сборщиком мусора

Память, выделенная с помощью `new()` и `make()`, управляется сборщиком мусора Go:

1. **Триггеры GC**: Выделение памяти может запустить цикл сборки мусора, если достигнут порог.

2. **Помощь GC**: Большие аллокации через `make()` могут заставить горутину помогать в сборке мусора.

3. **Освобождение**: Объекты автоматически освобождаются, когда становятся недостижимыми.

### Расширенные техники и шаблоны (Senior Level)

#### Синхронизированные структуры данных

```go
// Потокобезопасный счетчик с использованием sync.Mutex
type Counter struct {
    mu    sync.Mutex
    count int
}

func NewCounter() *Counter {
    return new(Counter) // Возвращает указатель на Counter с нулевыми значениями
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}
```

#### Кастомные инициализаторы с паттерном опций

```go
type ServerConfig struct {
    // многие поля
}

func NewServerConfig(options ...func(*ServerConfig)) *ServerConfig {
    config := new(ServerConfig) // Базовая инициализация
    
    // Применение дефолтных значений
    config.Port = 8080
    
    // Применение пользовательских опций
    for _, option := range options {
        option(config)
    }
    
    return config
}

// Использование
config := NewServerConfig(
    func(c *ServerConfig) { c.Port = 443 },
    func(c *ServerConfig) { c.TLS = true },
)
```

#### Оптимизация памяти со слайсами фиксированного размера

```go
// Непрерывный блок для улучшения локальности кэша
type Matrix struct {
    data []float64
    rows, cols int
}

func NewMatrix(rows, cols int) *Matrix {
    return &Matrix{
        data: make([]float64, rows*cols), // один непрерывный блок
        rows: rows,
        cols: cols,
    }
}

func (m *Matrix) At(i, j int) float64 {
    return m.data[i*m.cols + j]
}

func (m *Matrix) Set(i, j int, val float64) {
    m.data[i*m.cols + j] = val
}
```

#### Предвыделение и пулы объектов

```go
// Пул буферов фиксированного размера
var bufferPool = sync.Pool{
    New: func() interface{} {
        buffer := make([]byte, 4096)
        return &buffer
    },
}

func processData(data []byte) []byte {
    // Получаем буфер из пула
    bufPtr := bufferPool.Get().(*[]byte)
    buf := *bufPtr
    
    // Используем буфер
    // ...
    
    // Возвращаем буфер в пул
    bufferPool.Put(bufPtr)
    
    return result
}
```

#### Предотвращение аллокаций с предварительно выделенными слайсами

```go
// Избегаем аллокаций в горячем пути
func processItems(items []Item) []Result {
    // Предвыделяем результирующий слайс
    results := make([]Result, 0, len(items))
    
    for _, item := range items {
        result := process(item)
        results = append(results, result)
    }
    
    return results
}
```

### Особые случаи и неочевидное поведение

#### nil слайс vs пустой слайс

```go
var nilSlice []int      // nil слайс (nil, 0, 0)
emptySlice := make([]int, 0) // пустой слайс (ptr, 0, 0)

fmt.Println(nilSlice == nil)    // true
fmt.Println(emptySlice == nil)  // false

// Оба работают с append
nilSlice = append(nilSlice, 1)
emptySlice = append(emptySlice, 1)
```

#### make с нулевой длиной или емкостью

```go
// Валидные выражения:
s1 := make([]int, 0)    // len=0, cap=0
s2 := make([]int, 0, 0) // len=0, cap=0
m := make(map[string]int, 0) // пустая map
c := make(chan int, 0) // небуферизованный канал

// Невалидные:
// make([]int, -1)    // компилятор или runtime error
// make(chan int, -1) // компилятор или runtime error
```

#### Использование new для slice, map и channel

```go
ps := new([]int)     // *[]int со значением nil
pm := new(map[string]int) // *map[string]int со значением nil
pc := new(chan int)  // *chan int со значением nil

// Требуется дополнительная инициализация
*ps = make([]int, 10)
*pm = make(map[string]int)
*pc = make(chan int)

// Редко используемый паттерн
```

#### Диагностика проблем с аллокациями

```go
// Компиляция с отладочной информацией о размещении переменных
// go build -gcflags="-m" program.go

// Профилирование аллокаций
import "runtime/pprof"

f, _ := os.Create("mem-profile.pprof")
defer f.Close()
pprof.WriteHeapProfile(f)

// Анализ через Go tool pprof
// go tool pprof -alloc_space mem-profile.pprof
```

## Связанные заметки

- [[Базовые типы данных]]
- [[Zero-Value]]
- [[Куча и стек. Escape Analysis]]
- [[Выравнивание структур]]

## Источники

- [Go Specification: Built-in functions](https://golang.org/ref/spec#Built-in_functions)
- [Исходный код пакета builtin](https://golang.org/src/builtin/builtin.go)
- [Go Blog: The Go Memory Model](https://golang.org/ref/mem)
- [Go Blog: Slices](https://blog.golang.org/slices-intro)
- [Go Internals: Channels](https://golang.design/under-the-hood/zh-cn/part2runtime/ch06sched/chan)
- [Go Runtime Source: Map Implementation](https://github.com/golang/go/blob/master/src/runtime/map.go)
- [Dave Cheney: High Performance Go Workshop](https://dave.cheney.net/high-performance-go-workshop/gophercon-2019.html)
