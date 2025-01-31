## Короткий ответ
Малварные бэкдоры в Ethereum прокси-контрактах могут возникать из-за коллизий селекторов функций, неинициализированных прокси или неправильного использования `delegatecall`. Эти уязвимости позволяют злоумышленникам захватывать контроль над контрактами, изменять их логику или выводить средства.

---

## Подробный разбор

### **1) Коллизии селекторов функций**

#### **Проблема:**
- **Определение:**
  - Коллизия селекторов происходит, если два селектора функций совпадают.
  - Это может привести к непредсказуемым вызовам функций в прокси-контрактах.
- **Пример проблемы:**
  ```solidity
  contract Proxy {
      function admin() public pure returns (address) {
          return address(0x123);
      }

      fallback() external payable {
          address(logic).delegatecall(msg.data); // Конфликт с функцией admin()
      }
  }
  ```

#### **Решение:**
- Используйте уникальные имена функций или добавьте префиксы для предотвращения коллизий.
- Пример:
  ```solidity
  contract Logic {
      function setAdminLogic(address _admin) public {
          // Логика
      }
  }

  contract Proxy {
      function setAdminProxy(address _admin) public {
          // Логика
      }
  }
  ```

#### **Технические детали:**
- **На уровне EVM:**
  - Селекторы функций вычисляются как первые 4 байта хэша Keccak-256 от сигнатуры функции.

---

### **2) Неинициализированные прокси**

#### **Проблема:**
- **Описание:**
  - Если прокси не инициализирован, злоумышленник может установить свою логику.
- **Пример уязвимости:**
  ```solidity
  contract VulnerableProxy {
      address public implementation;

      function setImplementation(address _implementation) public {
          implementation = _implementation; // Уязвимость при отсутствии проверки
      }

      fallback() external payable {
          address(implementation).delegatecall(msg.data);
      }
  }
  ```

#### **Решение:**
- Добавьте проверку инициализации:
  ```solidity
  contract SecureProxy {
      address public implementation;
      bool public initialized;

      function initialize(address _implementation) public {
          require(!initialized, "Already initialized");
          implementation = _implementation;
          initialized = true;
      }

      fallback() external payable {
          require(initialized, "Not initialized");
          address(implementation).delegatecall(msg.data);
      }
  }
  ```

#### **Технические детали:**
- **На уровне EVM:**
  - Неинициализированные прокси могут быть использованы для изменения storage через `DELEGATECALL`.

---

### **3) Неправильное использование `delegatecall`**

#### **Проблема:**
- **Описание:**
  - Неправильное использование `delegatecall` может привести к изменению неожиданных переменных в storage.
- **Пример проблемы:**
  ```solidity
  contract Logic {
      uint public value;

      function setValue(uint _value) public {
          value = _value;
      }
  }

  contract Proxy {
      uint public balance;
      address public logic;

      constructor(address _logic) {
          logic = _logic;
      }

      fallback() external payable {
          address(logic).delegatecall(msg.data); // Изменение balance вместо value
      }
  }
  ```

#### **Решение:**
- Убедитесь, что структура storage вызывающего и целевого контрактов совпадает.

#### **Технические детали:**
- **На уровне EVM:**
  - `DELEGATECALL` использует storage вызывающего контракта.

---

### **4) Малварные бэкдоры**

#### **Пример атаки:**
- **Описание:**
  - Злоумышленник внедряет злонамеренную логику в контракт через прокси.
- **Пример:**
  ```solidity
  contract MaliciousLogic {
      address public owner;

      function setOwner(address _owner) public {
          owner = _owner; // Захват контроля
      }
  }

  contract Proxy {
      address public implementation;

      function setImplementation(address _implementation) public {
          implementation = _implementation;
      }

      fallback() external payable {
          address(implementation).delegatecall(msg.data);
      }
  }
  ```

#### **Решение:**
- Используйте модификаторы доступа для защиты критических функций.
- Пример:
  ```solidity
  contract SecureProxy {
      address public implementation;
      address public admin;

      constructor(address _admin) {
          admin = _admin;
      }

      function setImplementation(address _implementation) public {
          require(msg.sender == admin, "Not authorized");
          implementation = _implementation;
      }

      fallback() external payable {
          address(implementation).delegatecall(msg.data);
      }
  }
  ```

---

### **5) Рекомендации по безопасности**

#### **Лучшие практики:**
- **Инициализация:**
  - Всегда проверяйте инициализацию прокси перед использованием.
- **Селекторы:**
  - Проверяйте уникальность селекторов функций.
- **Доступ:**
  - Используйте модификаторы для ограничения доступа к критическим функциям.
- **Аудит:**
  - Регулярно проводите аудиты кода для выявления уязвимостей.

---

### **Заключение**

Малварные бэкдоры в Ethereum прокси-контрактах могут возникать из-за коллизий селекторов, неинициализированных прокси или неправильного использования `delegatecall`. Профессиональный подход требует тщательного проектирования, тестирования и аудита для предотвращения таких уязвимостей.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое delegatecall? Как представлен на уровне EVM? Откуда берется storage, откуда bytecode? Какое значение msg.sender, msg.value внутри вызова delegatecall? Когда стоит применять?]]
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]

---

## Источники
- [Malicious Backdoors in Ethereum Proxies](https://medium.com/nomic-foundation-blog/malicious-backdoors-in-ethereum-proxies-62629adf3357)
- [Understanding Delegatecall in Solidity](https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall)
---