## Короткий ответ

При различных типах вызовов значения `msg.sender` и `msg.value` ведут себя по-разному:
- `call`: `msg.sender` = адрес вызывающего контракта, `msg.value` = переданное значение
- `staticcall`: `msg.sender` = адрес вызывающего контракта, `msg.value` = 0 (не может передавать ETH)
- `delegatecall`: `msg.sender` = оригинальный отправитель, `msg.value` = значение из оригинального вызова

---

## Подробный разбор

### **1. Call**

```solidity
contract Caller {
    function makeCall(address target) external payable {
        // msg.sender в Target будет адрес этого контракта
        // msg.value в Target будет переданное значение
        (bool success, ) = target.call{value: msg.value}("");
        require(success, "Call failed");
    }
}

contract Target {
    event Received(address sender, uint256 value);
    
    receive() external payable {
        // sender = адрес Caller
        // value = переданное значение
        emit Received(msg.sender, msg.value);
    }
}
```

### **2. Staticcall**

```solidity
contract StaticCaller {
    function makeStaticCall(address target) external {
        // msg.sender в Target будет адрес этого контракта
        // msg.value всегда 0
        (bool success, ) = target.staticcall(
            abi.encodeWithSignature("getValue()")
        );
        require(success, "Staticcall failed");
    }
}

contract StaticTarget {
    uint256 public value;
    
    function getValue() external view returns (uint256) {
        // sender = адрес StaticCaller
        // value = 0
        require(msg.value == 0, "Cannot send ETH with staticcall");
        return value;
    }
}
```

### **3. Delegatecall**

```solidity
contract DelegateCaller {
    uint256 public value;
    
    function makeDelegateCall(
        address target
    ) external payable {
        // msg.sender в Target будет оригинальный отправитель
        // msg.value будет из оригинального вызова
        (bool success, ) = target.delegatecall(
            abi.encodeWithSignature("setValue()")
        );
        require(success, "Delegatecall failed");
    }
}

contract DelegateTarget {
    uint256 public value;
    
    function setValue() external payable {
        // sender = оригинальный отправитель (не DelegateCaller)
        // value = значение из оригинального вызова
        value = msg.value;
    }
}
```

### **4. Сравнительный анализ**

```solidity
contract ComparisonExample {
    event Context(
        string callType,
        address msgSender,
        uint256 msgValue
    );
    
    function compareContexts(address target) external payable {
        // 1. Call
        target.call{value: 1 ether}(
            abi.encodeWithSignature("logContext(string)", "call")
        );
        
        // 2. Staticcall
        target.staticcall(
            abi.encodeWithSignature("logContext(string)", "staticcall")
        );
        
        // 3. Delegatecall
        target.delegatecall(
            abi.encodeWithSignature("logContext(string)", "delegatecall")
        );
    }
}

contract ContextLogger {
    event ContextLog(
        string callType,
        address msgSender,
        uint256 msgValue
    );
    
    function logContext(string memory callType) external payable {
        emit ContextLog(
            callType,
            msg.sender,
            msg.value
        );
    }
}
```

### **5. Практические примеры**

1. **Proxy паттерн:**
   ```solidity
   contract Proxy {
       address public implementation;
       
       fallback() external payable {
           address _implementation = implementation;
           assembly {
               // Сохраняем оригинальный msg.sender и msg.value
               let ptr := mload(0x40)
               calldatacopy(ptr, 0, calldatasize())
               
               let result := delegatecall(
                   gas(),
                   _implementation,
                   ptr,
                   calldatasize(),
                   0,
                   0
               )
               
               let size := returndatasize()
               returndatacopy(ptr, 0, size)
               
               switch result
               case 0 { revert(ptr, size) }
               default { return(ptr, size) }
           }
       }
   }
   ```

2. **Безопасные вызовы:**
   ```solidity
   contract SafeCaller {
       function safeCall(
           address target,
           bytes memory data,
           uint256 value
       ) external payable {
           require(msg.value >= value, "Insufficient ETH");
           
           bool success;
           bytes memory result;
           
           if (value > 0) {
               (success, result) = target.call{value: value}(data);
           } else {
               (success, result) = target.staticcall(data);
           }
           
           require(success, "Call failed");
           
           if (result.length > 0) {
               require(
                   abi.decode(result, (bool)),
                   "Operation failed"
               );
           }
       }
   }
   ```

---

## Связанные темы
- [[Как работает delegatecall?]]
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое raw call?]]

---

## Источники
- [Solidity Documentation - Message Calls](https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html#message-calls)
- [OpenZeppelin Proxy Patterns](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies)
- [Understanding Ethereum Smart Contract Storage](https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/) 