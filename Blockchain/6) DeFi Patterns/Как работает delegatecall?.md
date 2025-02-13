## Короткий ответ

`delegatecall` - это специальный тип вызова в Ethereum, который позволяет выполнить код другого контракта в контексте текущего контракта. При этом storage, msg.sender и msg.value берутся из контекста вызывающего контракта, а код выполняется из вызываемого контракта.

---

## Подробный разбор

### **1. Механизм работы**

```solidity
contract Caller {
    // Storage slot 0
    uint256 public value;
    
    function delegateCall(address target) external payable {
        // Выполняет код target контракта в контексте текущего контракта
        (bool success, ) = target.delegatecall(
            abi.encodeWithSignature("setValue(uint256)", 123)
        );
        require(success, "Delegatecall failed");
    }
}

contract Target {
    // Storage slot 0 (должен совпадать с Caller)
    uint256 public value;
    
    function setValue(uint256 newValue) external {
        value = newValue; // Изменяет storage вызывающего контракта
    }
}
```

### **2. Особенности контекста**

1. **Storage:**
   ```solidity
   contract DelegateCallContext {
       // Storage layout должен совпадать!
       uint256 public value;     // slot 0
       address public owner;     // slot 1
       mapping(address => uint256) public balances; // slot 2
       
       function compareStorage(address target) external {
           // При delegatecall используется storage текущего контракта
           (bool success, ) = target.delegatecall(
               abi.encodeWithSignature("updateStorage()")
           );
           require(success, "Delegatecall failed");
       }
   }
   ```

2. **Контекстные переменные:**
   ```solidity
   contract ContextVariables {
       event Context(
           address msgSender,
           address txOrigin,
           uint256 msgValue
       );
       
       function checkContext() external payable {
           emit Context(
               msg.sender,  // Адрес вызывающего контракта
               tx.origin,   // Оригинальный отправитель транзакции
               msg.value    // Значение ETH из вызывающего контракта
           );
       }
   }
   ```

### **3. Безопасность**

1. **Storage коллизии:**
   ```solidity
   contract Unsafe {
       // Неправильный layout
       address public owner;     // slot 0
       uint256 public value;     // slot 1
       
       // Может привести к перезаписи owner!
       function unsafeDelegateCall(address target) external {
           target.delegatecall(
               abi.encodeWithSignature("setValue(uint256)", 123)
           );
       }
   }
   ```

2. **Защитные механизмы:**
   ```solidity
   contract SafeDelegateCall {
       // Проверка совместимости
       function safeDelegateCall(
           address target,
           bytes4 selector
       ) external {
           // Проверяем поддержку интерфейса
           require(
               IERC165(target).supportsInterface(selector),
               "Incompatible target"
           );
           
           // Проверяем размер кода
           require(target.code.length > 0, "Not a contract");
           
           (bool success, ) = target.delegatecall(
               abi.encodeWithSelector(selector)
           );
           require(success, "Delegatecall failed");
       }
   }
   ```

### **4. Применение**

1. **Proxy паттерн:**
   ```solidity
   contract Proxy {
       address public implementation;
       
       fallback() external payable {
           address _implementation = implementation;
           assembly {
               // Копируем calldata
               calldatacopy(0, 0, calldatasize())
               
               // Выполняем delegatecall
               let success := delegatecall(
                   gas(),
                   _implementation,
                   0,
                   calldatasize(),
                   0,
                   0
               )
               
               // Копируем returndata
               returndatacopy(0, 0, returndatasize())
               
               switch success
               case 0 { revert(0, returndatasize()) }
               default { return(0, returndatasize()) }
           }
       }
   }
   ```

2. **Библиотеки:**
   ```solidity
   library SafeMath {
       function add(uint256 a, uint256 b) internal pure returns (uint256) {
           uint256 c = a + b;
           require(c >= a, "SafeMath: addition overflow");
           return c;
       }
   }
   
   contract Calculator {
       using SafeMath for uint256;
       
       function calculate(uint256 a, uint256 b) external pure returns (uint256) {
           // delegatecall к библиотеке происходит автоматически
           return a.add(b);
       }
   }
   ```

---

## Связанные темы

- [[6. Список вопросов]]
- [[Какие значения msg.value, msg.sender при call, staticcall, delegatecall?]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое storage collision?]]

---

## Источники
- [Solidity Documentation - Delegatecall](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries)
- [OpenZeppelin Proxy Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/proxy)
- [Understanding Delegatecall](https://eip2535diamonds.substack.com/p/understanding-delegatecall-and-how) 