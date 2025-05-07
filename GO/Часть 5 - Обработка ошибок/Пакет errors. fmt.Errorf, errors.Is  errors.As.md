# Пакет errors. fmt.Errorf, errors.Is / errors.As

## Краткий обзор

Пакет `errors` в Go предоставляет функциональность для создания, оборачивания и анализа ошибок. Основные компоненты этой экосистемы: конструктор простых ошибок (`errors.New`), форматированное создание ошибок (`fmt.Errorf`), механизм оборачивания ошибок с сохранением контекста (глагол `%w` в `fmt.Errorf`), а также функции для анализа оборачивающих ошибок (`errors.Is` и `errors.As`). Эта система позволяет создавать иерархии ошибок, добавлять контекст по мере прохождения через слои приложения, а также безопасно и типобезопасно сравнивать и приводить ошибки к определённым типам. В совокупности эти инструменты позволяют создавать мощные и гибкие механизмы обработки ошибок, соответствующие философии Go.

## Подробный разбор

### История развития обработки ошибок в Go

Подход к обработке ошибок в Go эволюционировал со временем:

1. **Go 1.0 (2012)**: Базовый пакет `errors` с функцией `errors.New()` для создания простых ошибок
2. **Go 1.13 (2019)**: Значительное обновление с добавлением функций `errors.Is`, `errors.As` и поддержки оборачивания ошибок через `%w` в `fmt.Errorf`
3. **Предложения для Go 2**: Рассматривались значительные изменения в синтаксисе обработки ошибок, но в итоге был выбран подход расширения существующей модели через пакет `errors`

### Создание ошибок

#### Базовые функции создания ошибок

1. **errors.New**: Создаёт простую строковую ошибку

   ```go
   import "errors"
   
   err := errors.New("database connection failed")
   ```

2. **fmt.Errorf**: Создаёт форматированную ошибку

   ```go
   import "fmt"
   
   err := fmt.Errorf("failed to connect to %s: timeout after %d seconds", host, timeout)
   ```

#### Внутреннее устройство ошибок

Стандартные ошибки, созданные через `errors.New`, представляют собой структуру `errorString`:

```go
// Из пакета errors
type errorString struct {
    s string
}

func (e *errorString) Error() string {
    return e.s
}

func New(text string) error {
    return &errorString{text}
}
```

Важно отметить, что два вызова `errors.New()` с одинаковым текстом создают разные экземпляры ошибок:

```go
err1 := errors.New("ошибка")
err2 := errors.New("ошибка")

// err1 и err2 имеют одинаковый текст, но err1 != err2
fmt.Println(err1 == err2) // false
```

### Оборачивание ошибок

#### Механизм %w в fmt.Errorf

В Go 1.13 был введён глагол `%w` для `fmt.Errorf`, позволяющий оборачивать ошибки с сохранением оригинальной ошибки:

```go
originalErr := errors.New("database query failed")
wrappedErr := fmt.Errorf("failed to fetch user data: %w", originalErr)
```

#### Внутреннее устройство оборачивания ошибок

Оборачивание реализовано через интерфейс `Unwrap`:

```go
// Интерфейс, который поддерживают оборачивающие ошибки
type Wrapper interface {
    Unwrap() error
}
```

Когда используется `%w` в `fmt.Errorf`, создаётся структура `wrapError`, реализующая метод `Unwrap()`:

```go
// Упрощённая версия из исходного кода
type wrapError struct {
    msg string
    err error
}

func (e *wrapError) Error() string {
    return e.msg
}

func (e *wrapError) Unwrap() error {
    return e.err
}
```

#### Создание пользовательских оборачивающих ошибок

Можно создавать собственные типы ошибок, поддерживающие развёртывание:

```go
type DatabaseError struct {
    Query string
    Err   error
}

func (e *DatabaseError) Error() string {
    return fmt.Sprintf("db error for query %q: %v", e.Query, e.Err)
}

func (e *DatabaseError) Unwrap() error {
    return e.Err
}
```

### Анализ ошибок

#### errors.Is - сравнение в цепочке ошибок

Функция `errors.Is` проверяет, содержится ли целевая ошибка где-либо в цепочке оборачивающих ошибок:

```go
// Старый способ (только прямое сравнение)
if err == io.EOF {
    // Обработка EOF
}

// Новый способ (проверка во всей цепочке)
if errors.Is(err, io.EOF) {
    // Обработка EOF, даже если оборачивается другими ошибками
}
```

#### errors.As - приведение типов в цепочке ошибок

Функция `errors.As` пытается привести ошибку (или любую ошибку в цепочке) к указанному типу:

```go
// Старый способ
var pathErr *os.PathError
if pe, ok := err.(*os.PathError); ok {
    // Используем pe
}

// Новый способ
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    // Используем pathErr, даже если ошибка была обёрнута
}
```

#### Внутренняя реализация функций errors.Is и errors.As

Функции `errors.Is` и `errors.As` рекурсивно проходят по цепочке ошибок, используя метод `Unwrap()`:

```go
// Упрощённая реализация errors.Is
func Is(err, target error) bool {
    if err == target {
        return true
    }
    
    if x, ok := err.(interface{ Is(error) bool }); ok && x.Is(target) {
        return true
    }
    
    // Проверяем цепочку ошибок
    for {
        if unwrapper, ok := err.(interface{ Unwrap() error }); ok {
            err = unwrapper.Unwrap()
            if err == nil {
                break
            }
            if err == target {
                return true
            }
            continue
        }
        break
    }
    return false
}
```

```go
// Упрощённая реализация errors.As
func As(err error, target interface{}) bool {
    if target == nil {
        panic("errors: target cannot be nil")
    }
    
    val := reflect.ValueOf(target)
    if val.Kind() != reflect.Ptr || val.IsNil() {
        panic("errors: target must be a non-nil pointer")
    }
    
    targetType := val.Type().Elem()
    
    for err != nil {
        if reflect.TypeOf(err).AssignableTo(targetType) {
            val.Elem().Set(reflect.ValueOf(err))
            return true
        }
        
        if x, ok := err.(interface{ As(interface{}) bool }); ok && x.As(target) {
            return true
        }
        
        // Проверяем цепочку ошибок
        if unwrapper, ok := err.(interface{ Unwrap() error }); ok {
            err = unwrapper.Unwrap()
        } else {
            break
        }
    }
    
    return false
}
```

### Расширенные возможности и кастомизация

#### Настройка поведения errors.Is

Можно определить метод `Is` для пользовательских ошибок, чтобы настроить логику сравнения:

```go
type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string {
    return fmt.Sprintf("query error: %s: %v", e.Query, e.Err)
}

func (e *QueryError) Unwrap() error {
    return e.Err
}

// Кастомная логика сравнения
func (e *QueryError) Is(target error) bool {
    t, ok := target.(*QueryError)
    if !ok {
        return false
    }
    return (e.Query == t.Query || t.Query == "") && errors.Is(e.Err, t.Err)
}
```

С этой реализацией, `errors.Is()` будет учитывать специальную логику сравнения:

```go
originalErr := &QueryError{Query: "SELECT * FROM users", Err: io.EOF}

// Проверяем по типу ошибки и конкретному запросу
target1 := &QueryError{Query: "SELECT * FROM users", Err: io.EOF}
fmt.Println(errors.Is(originalErr, target1)) // true

// Проверяем по типу с пустым запросом (сравнивается только Err)
target2 := &QueryError{Query: "", Err: io.EOF}
fmt.Println(errors.Is(originalErr, target2)) // true

// Разные ошибки
target3 := &QueryError{Query: "SELECT * FROM users", Err: io.ErrUnexpectedEOF}
fmt.Println(errors.Is(originalErr, target3)) // false
```

#### Настройка поведения errors.As

Аналогично, можно определить метод `As` для пользовательской логики приведения типов:

```go
func (e *QueryError) As(target interface{}) bool {
    // Попытка приведения к *io.ErrUnexpectedEOF
    if t, ok := target.(**io.ErrUnexpectedEOF); ok {
        if errors.As(e.Err, t) {
            return true
        }
    }
    return false
}
```

### Практические паттерны использования

#### Иерархии ошибок

Создание иерархий ошибок с сохранением контекста:

```go
// Базовая ошибка домена
type DomainError struct {
    Domain string
    Err    error
}

func (e *DomainError) Error() string {
    return fmt.Sprintf("%s domain error: %v", e.Domain, e.Err)
}

func (e *DomainError) Unwrap() error {
    return e.Err
}

// Производная ошибка
type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %v", e.Field, e.Err)
}

func (e *ValidationError) Unwrap() error {
    return e.Err
}

// Использование
func validateUser(user User) error {
    if err := validateEmail(user.Email); err != nil {
        return &ValidationError{Field: "email", Err: err}
    }
    return nil
}

func processUserData(user User) error {
    if err := validateUser(user); err != nil {
        return &DomainError{Domain: "user", Err: err}
    }
    return nil
}

// Обработка
err := processUserData(user)
if err != nil {
    var valErr *ValidationError
    if errors.As(err, &valErr) && valErr.Field == "email" {
        // Специфическая обработка ошибок валидации email
    }
    
    if errors.Is(err, ErrInvalidFormat) {
        // Обработка ошибок формата независимо от оборачивания
    }
}
```

#### Сентинельные ошибки vs типы ошибок

Рекомендации по выбору между сентинельными ошибками (pre-declared error values) и типами ошибок:

**Сентинельные ошибки** подходят для:

- Ошибок без дополнительного контекста
- Общих состояний (EOF, Not Found)
- API, где проверка по значению удобна

```go
var (
    ErrNotFound = errors.New("not found")
    ErrTimeout  = errors.New("operation timed out")
)

func FindItem() error {
    return ErrNotFound
}
```

**Типы ошибок** подходят для:

- Ошибок с дополнительным контекстом
- Ошибок, требующих извлечения данных
- Иерархий ошибок

```go
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}

func FindUser(id string) error {
    return &NotFoundError{Resource: "user", ID: id}
}
```

### Изменения в Go 1.13+ и их влияние

#### Больше не нужен пакет `github.com/pkg/errors`

До Go 1.13 для оборачивания ошибок часто использовался сторонний пакет `github.com/pkg/errors`. С введением `%w` в `fmt.Errorf`, `errors.Is` и `errors.As` большая часть этой функциональности стала доступна в стандартной библиотеке.

| Пакет pkg/errors          | Стандартный errors (Go 1.13+)          |
|---------------------------|----------------------------------------|
| `errors.New`              | `errors.New`                           |
| `errors.Wrap`             | `fmt.Errorf("context: %w", err)`       |
| `errors.WithMessage`      | комбинация `fmt.Errorf` и оборачивание |
| `errors.Cause`            | цикл `Unwrap()` или `errors.Is/As`     |
| `errors.Wrapf`            | `fmt.Errorf` с `%w` и форматированием  |

#### Улучшений в обработке ошибок в Go 1.13+

1. **Большая выразительность**: Можно строить более сложные иерархии ошибок
2. **Сохранение контекста**: Информация не теряется по мере прохождения через слои
3. **Типобезопасное извлечение**: `errors.As` обеспечивает безопасное приведение типов
4. **Улучшенная проверка**: `errors.Is` позволяет проверять на конкретные ошибки в цепочке

### Лучшие практики

#### 1. Добавление контекста к ошибкам

```go
// Плохо
if err != nil {
    return err // Теряется контекст
}

// Хорошо
if err != nil {
    return fmt.Errorf("failed to open config file: %w", err)
}
```

#### 2. Структурирование ошибок по домену

```go
// Определить базовые типы ошибок для каждой части системы
type StorageError struct {
    Op  string // Операция, вызвавшая ошибку
    Err error  // Исходная ошибка
}

func (e *StorageError) Error() string {
    return fmt.Sprintf("storage %s error: %v", e.Op, e.Err)
}

func (e *StorageError) Unwrap() error {
    return e.Err
}
```

#### 3. Создание фабричных методов для ошибок

```go
// Фабричные методы делают код более читаемым
func NewNotFoundError(resource, id string) error {
    return &NotFoundError{
        Resource: resource,
        ID:       id,
    }
}

// Использование
return NewNotFoundError("user", "123")
```

#### 4. Обработка всех вариантов ошибок

```go
err := someFunction()
if err != nil {
    // Проверка на конкретные ошибки
    if errors.Is(err, io.EOF) {
        // Обработка EOF
        return
    }
    
    // Попытка приведения к конкретному типу
    var pathErr *os.PathError
    if errors.As(err, &pathErr) {
        // Обработка ошибки пути
        return
    }
    
    // Общая обработка других ошибок
    return fmt.Errorf("unexpected error: %w", err)
}
```

#### 5. Избегание избыточного оборачивания

```go
// Плохо - избыточное оборачивание без добавления контекста
func f() error {
    err := g()
    if err != nil {
        return fmt.Errorf("%w", err) // Не добавляет ценности
    }
    return nil
}

// Хорошо - добавление реального контекста
func f() error {
    err := g()
    if err != nil {
        return fmt.Errorf("while processing input: %w", err)
    }
    return nil
}

// Альтернатива - просто возвращение исходной ошибки
func f() error {
    return g()
}
```

### Ограничения и проблемы

#### 1. Производительность

Цепочки оборачивающих ошибок могут влиять на производительность:

- Создание форматированных сообщений об ошибках
- Рекурсивные вызовы `Unwrap()` в `errors.Is/As`
- Выделение памяти при каждом оборачивании

#### 2. Сложность структуры ошибок

С глубокими вложенностями ошибок может быть трудно:

- Отлаживать цепочки ошибок
- Понимать истинную причину ошибки
- Предсказать поведение `errors.Is/As` с кастомными реализациями

#### 3. Отсутствие стектрейса

В отличие от исключений в других языках, стандартные Go ошибки не содержат автоматически собранного стектрейса. Для добавления этой информации часто используются сторонние библиотеки или собственные реализации.

## Связи с другими темами

- [[Конструкция defer]]
- [[Ошибки в Go. Паники. Работа с recover]]
- [[Go Runtime. Составляющие части Go Runtime]]
- [[Интерфейсы в Go]]

## Источники

1. [Go Documentation: Errors package](https://golang.org/pkg/errors/)
2. [Go Blog: Working with Errors in Go 1.13](https://blog.golang.org/go1.13-errors)
3. [Go 2 Error Handling Draft Design](https://go.googlesource.com/proposal/+/master/design/go2draft-error-handling.md)
4. [Go's Source Code: errors package](https://github.com/golang/go/blob/master/src/errors/errors.go)
5. [Go's Source Code: fmt package (errorf implementation)](https://github.com/golang/go/blob/master/src/fmt/errors.go)
6. [Practical Go: Real World Advice for Error Handling](https://dave.cheney.net/practical-go/presentations/qcon-china.html#_errors)
7. [The Evolution of Go Error Handling](https://medium.com/@val_deleplace/go-error-handling-evolution-2019-9871d0c78992)
8. [Go Error Handling Best Practices](https://earthly.dev/blog/golang-errors/)
9. [Go 1.13 Error Handling with Is and As](https://blog.dharnitski.com/2019/09/18/go-1.13-errors/)
10. [Errors are values](https://blog.golang.org/errors-are-values)
