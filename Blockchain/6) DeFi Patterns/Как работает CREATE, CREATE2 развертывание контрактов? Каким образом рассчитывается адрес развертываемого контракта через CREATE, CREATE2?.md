## Короткий ответ

CREATE и CREATE2 - это два механизма развертывания смарт-контрактов в Ethereum. CREATE генерирует адрес нового контракта на основе адреса создателя и его nonce. CREATE2 позволяет предсказать адрес контракта до его развертывания, используя фиксированный salt вместо nonce. CREATE2 часто используется в фабриках контрактов и для детерминированного развертывания.

---

## Подробный разбор

### **1. Механизм CREATE**

```solidity
contract ContractFactory {
    event ContractCreated(address newContract);
    
    // Создание контракта через CREATE
    function createContract(
        bytes memory bytecode
    ) external returns (address) {
        address newContract;
        
        assembly {
            // Создание контракта:
            // 1. Берем адрес создателя
            // 2. Используем nonce создателя
            // 3. address = keccak256(rlp([creator, nonce]))
            newContract := create(
                0,              // value в wei
                add(bytecode, 0x20), // смещение байткода
                mload(bytecode)      // длина байткода
            )
            
            // Проверка успешности создания
            if iszero(extcodesize(newContract)) {
                revert(0, 0)
            }
        }
        
        emit ContractCreated(newContract);
        return newContract;
    }
}
```

### **2. Механизм CREATE2**

```solidity
contract Create2Factory {
    event ContractCreated(
        address newContract,
        bytes32 salt
    );
    
    // Вычисление адреса до развертывания
    function computeAddress(
        bytes32 salt,
        bytes32 bytecodeHash
    ) public view returns (address) {
        return address(uint160(uint256(keccak256(abi.encodePacked(
            bytes1(0xff),
            address(this),
            salt,
            bytecodeHash
        )))));
    }
    
    // Создание контракта через CREATE2
    function createContract(
        bytes memory bytecode,
        bytes32 salt
    ) external returns (address) {
        address newContract;
        
        assembly {
            // Создание контракта:
            // address = keccak256(0xff ++ creator ++ salt ++ keccak256(bytecode))
            newContract := create2(
                0,              // value в wei
                add(bytecode, 0x20), // смещение байткода
                mload(bytecode),     // длина байткода
                salt            // соль
            )
            
            if iszero(extcodesize(newContract)) {
                revert(0, 0)
            }
        }
        
        emit ContractCreated(newContract, salt);
        return newContract;
    }
}
```

### **3. Фабрика клонов**

```solidity
contract CloneFactory {
    // Минимальный прокси-байткод
    bytes constant MINIMAL_PROXY_BYTECODE = hex"3d602d80600a3d3981f3363d3d373d3d3d363d73";
    bytes constant MINIMAL_PROXY_BYTECODE_SUFFIX = hex"5af43d82803e903d91602b57fd5bf3";
    
    // Создание клона через CREATE
    function createClone(
        address implementation
    ) external returns (address) {
        bytes memory bytecode = _generateBytecode(implementation);
        address clone;
        
        assembly {
            clone := create(
                0,
                add(bytecode, 0x20),
                mload(bytecode)
            )
        }
        
        return clone;
    }
    
    // Создание клона через CREATE2
    function createClone2(
        address implementation,
        bytes32 salt
    ) external returns (address) {
        bytes memory bytecode = _generateBytecode(implementation);
        address clone;
        
        assembly {
            clone := create2(
                0,
                add(bytecode, 0x20),
                mload(bytecode),
                salt
            )
        }
        
        return clone;
    }
    
    // Генерация байткода для клона
    function _generateBytecode(
        address implementation
    ) internal pure returns (bytes memory) {
        return abi.encodePacked(
            MINIMAL_PROXY_BYTECODE,
            implementation,
            MINIMAL_PROXY_BYTECODE_SUFFIX
        );
    }
}
```

### **4. Детерминированное развертывание**

```solidity
contract DeterministicDeployment {
    // Структура для хранения информации о развертывании
    struct Deployment {
        bytes32 salt;
        bytes32 bytecodeHash;
        address deployedAt;
    }
    
    mapping(bytes32 => Deployment) public deployments;
    
    // Развертывание с проверкой существования
    function deployDeterministic(
        bytes memory bytecode,
        bytes32 salt
    ) external returns (address) {
        bytes32 bytecodeHash = keccak256(bytecode);
        
        // Проверка существующего развертывания
        Deployment storage deployment = deployments[bytecodeHash];
        if (deployment.deployedAt != address(0)) {
            require(
                deployment.salt == salt,
                "Different salt for existing bytecode"
            );
            return deployment.deployedAt;
        }
        
        // Вычисление ожидаемого адреса
        address expectedAddress = computeAddress(salt, bytecodeHash);
        
        // Проверка, что адрес свободен
        require(
            expectedAddress.code.length == 0,
            "Address already used"
        );
        
        // Развертывание
        address newContract;
        assembly {
            newContract := create2(
                0,
                add(bytecode, 0x20),
                mload(bytecode),
                salt
            )
        }
        
        require(
            newContract == expectedAddress,
            "Deployment address mismatch"
        );
        
        // Сохранение информации
        deployments[bytecodeHash] = Deployment({
            salt: salt,
            bytecodeHash: bytecodeHash,
            deployedAt: newContract
        });
        
        return newContract;
    }
}
```

### **5. Безопасное использование**

```solidity
contract SafeDeployment {
    // Проверка инициализации
    modifier ensureInitialized(address deployment) {
        require(
            IInitializable(deployment).initialized(),
            "Not initialized"
        );
        _;
    }
    
    // Безопасное развертывание с инициализацией
    function deploySafe(
        bytes memory bytecode,
        bytes memory initData
    ) external returns (address) {
        // Развертывание
        address newContract = createContract(bytecode);
        
        // Инициализация
        (bool success, ) = newContract.call(initData);
        require(success, "Initialization failed");
        
        // Проверка инициализации
        require(
            IInitializable(newContract).initialized(),
            "Not initialized after deployment"
        );
        
        return newContract;
    }
    
    // Проверка байткода
    function verifyBytecode(
        address deployment,
        bytes32 expectedHash
    ) external view returns (bool) {
        bytes32 deployedHash;
        assembly {
            let size := extcodesize(deployment)
            let ptr := mload(0x40)
            extcodecopy(deployment, ptr, 0, size)
            deployedHash := keccak256(ptr, size)
        }
        
        return deployedHash == expectedHash;
    }
}
```

### **6. Примеры использования**

```solidity
contract DeploymentExamples {
    // Фабрика токенов с предсказуемыми адресами
    function deployToken(
        string memory name,
        string memory symbol,
        bytes32 salt
    ) external returns (address) {
        bytes memory bytecode = abi.encodePacked(
            type(ERC20Token).creationCode,
            abi.encode(name, symbol)
        );
        
        return createContract2(bytecode, salt);
    }
    
    // Развертывание прокси с имплементацией
    function deployProxyWithImpl(
        address implementation,
        bytes memory initData,
        bytes32 salt
    ) external returns (address) {
        // Развертывание прокси
        bytes memory proxyBytecode = _generateProxyBytecode(
            implementation
        );
        
        address proxy = createContract2(proxyBytecode, salt);
        
        // Инициализация
        (bool success, ) = proxy.call(initData);
        require(success, "Proxy initialization failed");
        
        return proxy;
    }
}
```

---

## Связанные темы
- [[Расскажите подробно как работает паттерн proxy?]]
- [[Что такое Eternal storage?]]
- [[Расскажите о паттерне инициализации смарт-контрактов]]

---

## Источники
- [EIP-1014: Skinny CREATE2](https://eips.ethereum.org/EIPS/eip-1014)
- [OpenZeppelin: CREATE2 Documentation](https://docs.openzeppelin.com/cli/2.8/deploying-with-create2)
- [Understanding CREATE2](https://blog.openzeppelin.com/getting-the-most-out-of-create2/) 