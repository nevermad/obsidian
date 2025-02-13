## Короткий ответ

Наиболее значимые EIP включают: EIP-1559 (механизм сжигания базовой комиссии), EIP-4844 (proto-danksharding для L2 масштабирования), EIP-3675 (переход на PoS), EIP-1967 (унифицированное хранение для прокси), EIP-2535 (Diamond Standard для модульных смарт-контрактов).

---

## Подробный разбор

### **1. EIP-1559: Fee Market Change**

1. **Технические детали:**
   ```solidity
   struct Transaction {
       // Новые поля после EIP-1559
       uint256 maxPriorityFeePerGas;  // Чаевые майнеру
       uint256 maxFeePerGas;          // Максимальная общая комиссия
       // ... остальные поля
   }
   ```

2. **Механизм работы:**
   - Базовая комиссия (`base_fee`) автоматически корректируется
   - Формула расчета: `new_base_fee = old_base_fee * (1 + 1/8 * (target_gas_used - actual_gas_used)/target_gas_used)`
   - Базовая комиссия сжигается
   - Майнеры получают только чаевые (`priority_fee`)

3. **Влияние на газ:**
   ```javascript
   effective_gas_price = min(base_fee + priority_fee_per_gas, max_fee_per_gas)
   ```

### **2. EIP-4844: Shard Blob Transactions**

1. **Технические аспекты:**
   ```solidity
   struct BlobTransaction {
       uint256 blobVersionedHash;    // Хеш блоба
       bytes[] blobs;                 // Массив блобов
       bytes[] commitments;          // KZG коммитменты
       bytes[] proofs;               // KZG доказательства
   }
   ```

2. **Особенности реализации:**
   - Использует KZG коммитменты для верификации данных
   - Данные доступны только временно (1-3 месяца)
   - Отдельный рынок газа для блобов

3. **Пример использования в L2:**
   ```solidity
   contract L2Bridge {
       function submitBatch(
           bytes32 blobHash,
           uint256 blobIndex
       ) external {
           require(verifyBlobAvailability(blobHash, blobIndex));
           // Обработка данных из блоба
       }
   }
   ```

### **3. EIP-3675: Upgrade to PoS**

1. **Ключевые изменения:**
   ```solidity
   interface IBeacon {
       function getValidators() external view returns (address[] memory);
       function getEpoch() external view returns (uint256);
       function getSlot() external view returns (uint256);
   }
   ```

2. **Технические аспекты:**
   - Замена PoW на PoS консенсус
   - Введение слотов и эпох
   - Финальность через Casper FFG

3. **Механизм стейкинга:**
   ```solidity
   contract DepositContract {
       function deposit(
           bytes calldata pubkey,
           bytes calldata withdrawal_credentials,
           bytes calldata signature,
           bytes32 deposit_data_root
       ) external payable {
           require(msg.value == 32 ether);
           // Логика депозита
       }
   }
   ```

### **4. EIP-1967: Standard Proxy Storage Slots**

1. **Стандартные слоты:**
   ```solidity
   bytes32 constant IMPLEMENTATION_SLOT = 
       0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
   
   bytes32 constant ADMIN_SLOT = 
       0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
   
   bytes32 constant BEACON_SLOT = 
       0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50;
   ```

2. **Пример использования:**
   ```solidity
   contract StandardProxy {
       function _setImplementation(address newImplementation) internal {
           assembly {
               sstore(IMPLEMENTATION_SLOT, newImplementation)
           }
       }
       
       function _implementation() internal view returns (address impl) {
           assembly {
               impl := sload(IMPLEMENTATION_SLOT)
           }
       }
   }
   ```

### **5. EIP-2535: Diamond Standard**

1. **Структура Diamond:**
   ```solidity
   struct FacetCut {
       address facetAddress;
       FacetCutAction action;
       bytes4[] functionSelectors;
   }
   
   enum FacetCutAction {Add, Replace, Remove}
   ```

2. **Пример реализации:**
   ```solidity
   contract Diamond {
       struct FacetAddressAndPosition {
           address facetAddress;
           uint96 functionSelectorPosition;
       }
   
       bytes32 constant DIAMOND_STORAGE_POSITION = 
           keccak256("diamond.standard.diamond.storage");
           
       function diamondCut(
           FacetCut[] calldata _diamondCut,
           address _init,
           bytes calldata _calldata
       ) external {
           // Логика обновления фасетов
       }
   }
   ```

3. **Особенности:**
   - Модульная архитектура
   - Неограниченное количество функций
   - Возможность частичного обновления

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое EIP?]]
- [[Что такое ERC?]]
- [[By design EVM имеет неизменяемый байткод для контрактов. За счет каких механизмов получается обойти это ограничение и сделать контракт изменяемым?]]

---

## Источники
- [EIP-1559 Specification](https://eips.ethereum.org/EIPS/eip-1559)
- [EIP-4844 Specification](https://eips.ethereum.org/EIPS/eip-4844)
- [EIP-3675 Specification](https://eips.ethereum.org/EIPS/eip-3675)
- [EIP-1967 Specification](https://eips.ethereum.org/EIPS/eip-1967)
- [EIP-2535 Specification](https://eips.ethereum.org/EIPS/eip-2535) 