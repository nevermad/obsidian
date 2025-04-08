# Zero-Value в Go

## Краткий обзор

Zero-Value (нулевое значение) в Go – это значение по умолчанию, которым инициализируются все переменные при их объявлении, если не указано иное. В отличие от многих языков, Go гарантирует, что все переменные всегда инициализированы. Эта концепция является частью философии "явного лучше, чем неявного" и исключает ошибки, связанные с неинициализированными переменными, повышая безопасность программ.

## Подробный разбор

### Zero-Value для разных типов

Каждый тип в Go имеет свое нулевое значение:

| Тип                      | Zero-Value            |
|--------------------------|------------------------|
| bool                     | false                  |
| integers (int, int8...) | 0                      |
| floating point (float32) | 0.0                   |
| string                   | "" (пустая строка)    |
| pointers                 | nil                    |
| slices                   | nil                    |
| maps                     | nil                    |
| channels                 | nil                    |
| interfaces               | nil                    |
| functions                | nil                    |
| structs                  | каждое поле со своим zero-value |
| arrays                   | каждый элемент со своим zero-value |

```go
var i int       // i == 0
var f float64   // f == 0.0
var b bool      // b == false
var s string    // s == ""
var p *int      // p == nil
var slice []int // slice == nil
var m map[string]int // m == nil
var c chan int       // c == nil
var fn func()        // fn == nil
var i interface{}    // i == nil

// Структуры
type Person struct {
    Name string
    Age  int
}
var person Person // person == Person{Name: "", Age: 0}

// Массивы
var arr [3]int // arr == [0, 0, 0]
```

### Важные особенности Zero-Value

#### 1. Безопасность и предсказуемость

Концепция Zero-Value исключает ошибки, связанные с неинициализированными переменными:

```go
// В других языках это могло бы вызвать неопределенное поведение
var counter int
counter++ // безопасно, counter == 1
```

#### 2. Сложные типы с Zero-Value nil

Важно понимать, что хотя некоторые типы имеют Zero-Value равное `nil`, их поведение при этом различается:

```go
// Слайсы с nil безопасны для чтения длины
var s []int
fmt.Println(len(s)) // 0, безопасно

// Мапы с nil нельзя использовать для записи (будет паника)
var m map[string]int
// m["key"] = 1 // паника: assignment to entry in nil map

// Каналы с nil блокируют чтение и запись
var c chan int
// <-c        // блокируется навсегда
// c <- 1     // блокируется навсегда

// Интерфейсы с nil ведут себя по-разному в зависимости от конкретной реализации
var writer io.Writer // nil
// writer.Write([]byte("hello")) // паника: nil pointer dereference
```

#### 3. Инициализация составных типов с нулевыми значениями

Структуры и массивы могут быть инициализированы с zero-value для невыбранных полей:

```go
// Только некоторые поля инициализированы, остальные получают zero-value
type Config struct {
    Host     string
    Port     int
    Timeout  int
    MaxConns int
    TLS      bool
}

// Port, MaxConns и TLS получат нулевые значения
config := Config{
    Host:    "localhost",
    Timeout: 30,
}
```

### Внутренняя реализация Zero-Value (Senior Level)

#### Компиляция и бинарный уровень

На уровне компилятора и рантайма, zero-values реализованы следующим образом:

1. **Статическая память**: Глобальные переменные размещаются в сегменте данных программы (`.bss` для неинициализированных и `.data` для инициализированных). Сегмент `.bss` заполняется нулями операционной системой при загрузке программы.

2. **Стек**: При выделении места на стеке для локальных переменных, Go не инициализирует их нулями явно. Вместо этого компилятор вставляет код инициализации перед первым использованием.

3. **Куча**: При выделении памяти в куче, рантайм Go всегда инициализирует память нулями. Это гарантирует, что все объекты начинают существование с zero-value.

#### Оптимизации компилятора

Компилятор Go выполняет ряд оптимизаций, связанных с zero-value:

1. **Удаление ненужной инициализации**: Если компилятор видит, что переменная будет инициализирована до первого использования, он может пропустить явную инициализацию нулевыми значениями.

2. **Создание предварительно нулевых областей памяти**: В некоторых случаях компилятор или рантайм могут предварительно обнулить большие блоки памяти.

### Zero-Value и производительность

#### Инициализация нулями и влияние на производительность

Автоматическая инициализация нулями имеет свою цену:

1. **Для стека**: При выделении большого количества локальных переменных, инициализация нулями может быть заметной.

2. **Для кучи**: Операции выделения памяти в куче включают обнуление, что добавляет накладные расходы. Для больших объектов эти расходы могут быть значительными.

```go
// Выделение и инициализация большого массива нулевыми значениями
data := make([]byte, 1024*1024*100) // 100 МБ
```

В таких случаях, компилятор и рантайм Go используют оптимизированные методы для обнуления больших блоков памяти, например, вызывая системные функции типа `memclr`.

#### Использование make и предварительное выделение памяти

Для динамических типов (slices, maps, channels) использование `make` позволяет экономить память и время на повторных аллокациях:

```go
// Выделение слайса с начальной емкостью
data := make([]int, 0, 1000) // len=0, cap=1000

// Предварительное выделение мапы
cache := make(map[string]interface{}, 100) // начальная емкость 100
```

### Паттерны и лучшие практики с Zero-Value (Senior Level)

#### 1. Zero-Value Useability (Полезность нулевых значений)

Следуйте принципу "полезности нулевых значений", проектируя типы так, чтобы их нулевые значения были функциональными:

```go
// Плохо: нулевое значение не функционально
type Config struct {
    host string // неэкспортируемое поле, нельзя инициализировать
}

func NewConfig() *Config {
    return &Config{host: "default"}
}

func (c *Config) Host() string {
    return c.host
}

// Хорошо: нулевое значение функционально
type BetterConfig struct {
    Host string // экспортируемое поле
}

func (c BetterConfig) GetHost() string {
    if c.Host == "" {
        return "default"
    }
    return c.Host
}
```

#### 2. Struct Initialization Patterns

Несколько подходов к инициализации структур с учетом Zero-Value:

```go
// Подход 1: Опциональные функциональные опции
type Server struct {
    addr     string
    port     int
    handlers map[string]Handler
}

// Конструктор, использующий функциональные опции
func NewServer(options ...func(*Server)) *Server {
    // Значения по умолчанию
    s := &Server{
        addr: "localhost",
        port: 8080,
        handlers: make(map[string]Handler),
    }
    
    // Применяем опции
    for _, option := range options {
        option(s)
    }
    
    return s
}

// Определение опций
func WithAddress(addr string) func(*Server) {
    return func(s *Server) {
        s.addr = addr
    }
}

func WithPort(port int) func(*Server) {
    return func(s *Server) {
        s.port = port
    }
}

// Использование
server := NewServer(
    WithAddress("example.com"),
    WithPort(443),
)

// Подход 2: Умное использование нулевых значений
type Config struct {
    LogLevel int // 0=Debug, 1=Info, 2=Warning, 3=Error
    MaxConns int
    Timeout  time.Duration
}

func (c *Config) applyDefaults() {
    if c.MaxConns <= 0 {
        c.MaxConns = 100 // дефолт только если не установлено
    }
    if c.Timeout == 0 {
        c.Timeout = 30 * time.Second
    }
}

func NewService(cfg *Config) *Service {
    if cfg == nil {
        cfg = &Config{} // используем нулевые значения
    }
    cfg.applyDefaults()
    
    // ... создание сервиса с конфигом
}
```

#### 3. Nilable и Non-Nilable типы

Рекомендуется четко определять, может ли тип принимать значение `nil` в вашем дизайне API:

```go
// Non-Nilable тип
type Logger interface {
    Log(msg string)
}

// Реализация по умолчанию, используемая вместо nil
type defaultLogger struct{}

func (l defaultLogger) Log(msg string) {
    // Ничего не делает или реализация по умолчанию
}

// Функция, обеспечивающая non-nilable логгер
func ensureLogger(logger Logger) Logger {
    if logger == nil {
        return defaultLogger{}
    }
    return logger
}

func Process(data []byte, logger Logger) {
    // Всегда получаем валидный логгер
    log := ensureLogger(logger)
    
    // Безопасно используем логгер без проверки на nil
    log.Log("Processing data...")
}
```

#### 4. Использование нулевых значений для оптимизации

В высоконагруженных системах можно использовать знание о нулевых значениях для оптимизаций:

```go
// Оптимизации в горячих путях при работе со строками
func fastProcess(data string) string {
    // Если строка пустая (нулевое значение), пропускаем обработку
    if data == "" {
        return ""
    }
    
    // Обрабатываем только непустые строки
    return transform(data)
}

// Избегаем аллокаций в куче, используя zero-value слайсы
func collectIDs(items []Item) []int {
    if len(items) == 0 {
        return nil // возвращаем nil вместо пустого слайса для экономии аллокаций
    }
    
    result := make([]int, 0, len(items))
    for _, item := range items {
        if item.ShouldInclude() {
            result = append(result, item.ID)
        }
    }
    
    if len(result) == 0 {
        return nil // если после фильтрации ничего не осталось, возвращаем nil
    }
    
    return result
}
```

### Zero-Value в интерфейсах (Senior Level)

Интерфейсы в Go имеют особое поведение с нулевыми значениями. Интерфейс содержит два поля: тип и указатель на значение. Когда оба поля нулевые, интерфейс равен `nil`.

```go
// Нулевой интерфейс
var i interface{} // i == nil

// Интерфейс с нулевым значением конкретного типа != nil
var p *int
var i interface{} = p // i != nil, хотя p == nil
```

Это приводит к важному поведению - интерфейс, содержащий нулевой указатель, не равен `nil`:

```go
func doSomething() error {
    var err *CustomError // nil значение типа *CustomError
    return err // возвращает non-nil error!
}

func main() {
    err := doSomething()
    fmt.Println(err == nil) // false!
    
    // Правильный подход:
    if err != nil {
        if customErr, ok := err.(*CustomError); ok && customErr == nil {
            // обрабатываем особый случай nil-значения в ненулевом интерфейсе
        }
    }
}
```

### Zero-Value в многопоточной среде

При использовании Zero-Value в многопоточной среде есть особые моменты:

```go
// Использование sync.Mutex
var mu sync.Mutex // Zero-Value для mutex - разблокированное состояние

// Безопасно в многопоточной среде
mu.Lock()
// критическая секция
mu.Unlock()

// Использование sync.Map вместо nil map в многопоточной среде
var cache sync.Map // Zero-Value для sync.Map - рабочий потокобезопасный экземпляр

// Безопасно в многопоточной среде
cache.Store("key", value)
value, ok := cache.Load("key")
```

## Связанные заметки

- [[Базовые типы данных]]
- [[Указатели]]
- [[Куча и стек. Escape Analysis]]
- [[Пустой интерфейс и пустая структура]]

## Источники

- [Go Specification: The zero value](https://golang.org/ref/spec#The_zero_value)
- [Effective Go: Zero Values](https://golang.org/doc/effective_go#allocation_new)
- [Go Blog: Declaration Syntax](https://go.dev/blog/declaration-syntax)
- [The Go Memory Model](https://golang.org/ref/mem)
- [Dave Cheney: Zero values and nil](https://dave.cheney.net/2017/08/09/typed-nils-in-go)
- [Go 101: Zero Values and Initialization](https://go101.org/article/value-part.html)
