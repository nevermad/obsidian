## Короткий ответ

Уязвимость неинициализированных прокси в Wormhole позволила злоумышленникам захватить контроль над контрактом, установив свою логику через `delegatecall`. Проблема была вызвана отсутствием проверки инициализации прокси. Решение заключалось в добавлении механизма инициализации с защитой от повторного вызова.

---

## Подробный разбор

### **1) Описание уязвимости**

#### **Проблема:**
- **Неинициализированный прокси:**
  - Если прокси не инициализирован, злоумышленник может установить свою логику.
  - Это позволяет выполнить произвольный код через `delegatecall`.
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

#### **Последствия:**
- Злоумышленник мог изменить логику контракта, вывести средства или захватить контроль.

---

### **2) Анализ проблемы**

#### **Технические детали:**
- **На уровне EVM:**
  - `DELEGATECALL` использует storage вызывающего контракта.
  - Неинициализированный прокси позволяет установить любую логику.
- **Пример атаки:**
  ```solidity
  contract MaliciousLogic {
      address public owner;

      function setOwner(address _owner) public {
          owner = _owner; // Захват контроля
      }
  }

  contract Attacker {
      function attack(address proxyAddress, address maliciousLogic) public {
          VulnerableProxy(proxyAddress).setImplementation(maliciousLogic);
      }
  }
  ```

#### **Подводные камни:**
- Отсутствие проверки инициализации делает прокси уязвимым.
- Неправильное использование `delegatecall` может привести к изменению storage.

---

### **3) Решение**

#### **Исправление:**
- **Добавление проверки инициализации:**
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

#### **Механизм защиты:**
- **Флаг инициализации:**
  - Проверка `initialized` предотвращает повторную инициализацию.
- **Ограничение доступа:**
  - Только администратор может вызвать функцию инициализации.

---

### **4) Лучшие практики**

#### **Рекомендации:**
- **Инициализация:**
  - Всегда проверяйте инициализацию прокси перед использованием.
- **Доступ:**
  - Используйте модификаторы для ограничения доступа к критическим функциям.
- **Аудит:**
  - Регулярно проводите аудиты кода для выявления уязвимостей.

#### **Пример реализации:**
```solidity
contract SecureProxy {
    address public implementation;
    bool public initialized;
    address public admin;

    constructor(address _admin) {
        admin = _admin;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not authorized");
        _;
    }

    function initialize(address _implementation) public onlyAdmin {
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

---

### **5) Технические детали на уровне EVM**

#### **Опкоды:**
- **`DELEGATECALL`:**
  - Выполняет код целевого контракта в контексте вызывающего.
  - Использует storage вызывающего контракта.
- **`SSTORE`/`SLOAD`:**
  - Операции записи/чтения в storage.

#### **Газовые затраты:**
- Инициализация прокси требует дополнительных операций записи в storage (`SSTORE`), что увеличивает затраты газа.

---

### **6) Заключение**

Уязвимость неинициализированных прокси в Wormhole была вызвана отсутствием проверки инициализации. Решение заключалось в добавлении механизма инициализации с защитой от повторного вызова. Профессиональный подход требует тщательного проектирования, тестирования и аудита для предотвращения таких уязвимостей.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое delegatecall? Как представлен на уровне EVM? Откуда берется storage, откуда bytecode? Какое значение msg.sender, msg.value внутри вызова delegatecall? Когда стоит применять?]]
- [[Как работают модификаторы изменения состояния pure, view на уровне Solidity? Какие нюансы на уровне байткода EVM?]]

---

## Источники
- [Wormhole Uninitialized Proxy Bugfix Review](https://medium.com/immunefi/wormhole-uninitialized-proxy-bugfix-review-90250c41a43a)
- [Understanding Delegatecall in Solidity](https://ethereum.stackexchange.com/questions/3667/difference-between-call-callcode-and-delegatecall)
---