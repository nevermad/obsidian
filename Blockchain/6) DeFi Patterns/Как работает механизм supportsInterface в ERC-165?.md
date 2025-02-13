## Короткий ответ

`supportsInterface` - это механизм в ERC-165, который позволяет смарт-контрактам объявлять, какие интерфейсы они поддерживают. Функция принимает bytes4 идентификатор интерфейса (XOR всех селекторов функций) и возвращает boolean. Это позволяет другим контрактам программно определять, поддерживает ли контракт определенный интерфейс.

---

## Подробный разбор

### **1. Базовая реализация**

1. **Интерфейс ERC-165:**
   ```solidity
   interface IERC165 {
       function supportsInterface(bytes4 interfaceId) 
           external 
           view 
           returns (bool);
   }
   ```

2. **Стандартная реализация:**
   ```solidity
   contract ERC165 is IERC165 {
       // Маппинг для хранения поддерживаемых интерфейсов
       mapping(bytes4 => bool) private _supportedInterfaces;
       
       // Конструктор регистрирует интерфейс ERC165
       constructor() {
           _registerInterface(type(IERC165).interfaceId);
       }
       
       function supportsInterface(bytes4 interfaceId) 
           public 
           view 
           virtual 
           override 
           returns (bool) 
       {
           return _supportedInterfaces[interfaceId];
       }
       
       function _registerInterface(bytes4 interfaceId) 
           internal 
           virtual 
       {
           require(interfaceId != 0xffffffff, "Invalid interface");
           _supportedInterfaces[interfaceId] = true;
       }
   }
   ```

### **2. Вычисление interfaceId**

1. **Ручное вычисление:**
   ```solidity
   contract InterfaceIdCalculator {
       function calculateERC721InterfaceId() public pure returns (bytes4) {
           return type(IERC721).interfaceId;
           
           // Или вручную:
           return bytes4(
               keccak256('balanceOf(address)') ^
               keccak256('ownerOf(uint256)') ^
               keccak256('approve(address,uint256)') ^
               keccak256('getApproved(uint256)') ^
               keccak256('setApprovalForAll(address,bool)') ^
               keccak256('isApprovedForAll(address,address)') ^
               keccak256('transferFrom(address,address,uint256)') ^
               keccak256('safeTransferFrom(address,address,uint256)') ^
               keccak256('safeTransferFrom(address,address,uint256,bytes)')
           );
       }
   }
   ```

2. **Автоматическое вычисление:**
   ```solidity
   contract InterfaceIdGenerator {
       function getInterfaceId(string[] memory signatures) 
           public 
           pure 
           returns (bytes4) 
       {
           bytes4 interfaceId;
           for (uint i = 0; i < signatures.length; i++) {
               interfaceId ^= bytes4(keccak256(bytes(signatures[i])));
           }
           return interfaceId;
       }
   }
   ```

### **3. Примеры использования**

1. **Базовый контракт с ERC-165:**
   ```solidity
   contract MyToken is ERC165 {
       bytes4 private constant _INTERFACE_ID_ERC721 = 0x80ac58cd;
       bytes4 private constant _INTERFACE_ID_ERC721_METADATA = 0x5b5e139f;
       
       constructor() {
           _registerInterface(_INTERFACE_ID_ERC721);
           _registerInterface(_INTERFACE_ID_ERC721_METADATA);
       }
   }
   ```

2. **Проверка поддержки интерфейса:**
   ```solidity
   contract InterfaceChecker {
       function checkSupport(
           address contractAddress,
           bytes4 interfaceId
       ) public view returns (bool) {
           try IERC165(contractAddress).supportsInterface(interfaceId) 
               returns (bool support) {
               return support;
           } catch {
               return false;
           }
       }
       
       function isERC721(address contractAddress) 
           public 
           view 
           returns (bool) 
       {
           bytes4 ERC721_INTERFACE_ID = 0x80ac58cd;
           return checkSupport(contractAddress, ERC721_INTERFACE_ID);
       }
   }
   ```

### **4. Безопасное использование**

1. **Проверка с учетом газа:**
   ```solidity
   contract SafeInterfaceChecker {
       function safeCheckInterface(
           address contractAddress,
           bytes4 interfaceId
       ) public view returns (bool, bool) {
           // Первый bool - поддерживается ли интерфейс
           // Второй bool - успешно ли выполнена проверка
           
           if (contractAddress.code.length == 0) {
               return (false, false);
           }
           
           try IERC165(contractAddress).supportsInterface{gas: 30000}(
               type(IERC165).interfaceId
           ) returns (bool erc165Support) {
               if (!erc165Support) {
                   return (false, true);
               }
               
               try IERC165(contractAddress).supportsInterface{gas: 30000}(
                   interfaceId
               ) returns (bool support) {
                   return (support, true);
               } catch {
                   return (false, false);
               }
           } catch {
               return (false, false);
           }
       }
   }
   ```

2. **Защита от реентрабельности:**
   ```solidity
   contract SecureERC165 is ERC165 {
       bool private _initializing;
       
       modifier initializer() {
           require(
               !_initializing,
               "Initialization in progress"
           );
           _initializing = true;
           _;
           _initializing = false;
       }
       
       function _registerInterfaces(bytes4[] memory interfaceIds) 
           internal 
           initializer 
       {
           for (uint256 i = 0; i < interfaceIds.length;) {
               _registerInterface(interfaceIds[i]);
               unchecked { i++; }
           }
       }
   }
   ```

### **5. Расширенные возможности**

```solidity
contract AdvancedERC165 is ERC165 {
    event InterfaceRegistered(bytes4 indexed interfaceId);
    event InterfaceDeregistered(bytes4 indexed interfaceId);
    
    mapping(bytes4 => string) private _interfaceNames;
    
    function registerInterfaceWithName(
        bytes4 interfaceId,
        string memory name
    ) public {
        _registerInterface(interfaceId);
        _interfaceNames[interfaceId] = name;
        emit InterfaceRegistered(interfaceId);
    }
    
    function deregisterInterface(bytes4 interfaceId) public {
        require(
            interfaceId != type(IERC165).interfaceId,
            "Cannot deregister ERC165"
        );
        _supportedInterfaces[interfaceId] = false;
        delete _interfaceNames[interfaceId];
        emit InterfaceDeregistered(interfaceId);
    }
    
    function getInterfaceName(bytes4 interfaceId) 
        public 
        view 
        returns (string memory) 
    {
        return _interfaceNames[interfaceId];
    }
    
    function getSupportedInterfaces() 
        public 
        view 
        returns (bytes4[] memory, string[] memory) 
    {
        uint256 count = 0;
        for (uint256 i = 0; i < type(uint32).max; i++) {
            bytes4 interfaceId = bytes4(i);
            if (_supportedInterfaces[interfaceId]) {
                count++;
            }
        }
        
        bytes4[] memory interfaces = new bytes4[](count);
        string[] memory names = new string[](count);
        
        uint256 index = 0;
        for (uint256 i = 0; i < type(uint32).max; i++) {
            bytes4 interfaceId = bytes4(i);
            if (_supportedInterfaces[interfaceId]) {
                interfaces[index] = interfaceId;
                names[index] = _interfaceNames[interfaceId];
                index++;
            }
        }
        
        return (interfaces, names);
    }
}
```

---

## Связанные темы
- [[Как работает механизм обратных вызовов в ERC-721 и ERC-1155?]]
- [[Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.]]
- [[Как работает механизм approve в ERC-721?]]

---

## Источники
- [EIP-165: Standard Interface Detection](https://eips.ethereum.org/EIPS/eip-165)
- [OpenZeppelin ERC165](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/utils/introspection)
- [ERC165 Interface Detection in Practice](https://medium.com/@chiqing/ethereum-standard-erc165-explained-63b54ca0d273) 