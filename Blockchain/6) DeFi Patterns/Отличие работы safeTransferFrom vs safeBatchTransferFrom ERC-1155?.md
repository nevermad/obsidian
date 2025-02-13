## Короткий ответ

`safeTransferFrom` и `safeBatchTransferFrom` в ERC-1155 отличаются тем, что первая функция передает один тип токена в указанном количестве, а вторая позволяет передавать несколько типов токенов за одну транзакцию. Обе функции проверяют способность получателя принимать токены через `onERC1155Received` или `onERC1155BatchReceived` соответственно.

---

## Подробный разбор

### **1. Базовая реализация**

1. **safeTransferFrom:**
   ```solidity
   contract ERC1155Base {
       function safeTransferFrom(
           address from,
           address to,
           uint256 id,
           uint256 amount,
           bytes memory data
       ) public {
           require(
               from == msg.sender || isApprovedForAll(from, msg.sender),
               "Not approved"
           );
           
           _safeTransferFrom(from, to, id, amount, data);
       }
       
       function _safeTransferFrom(
           address from,
           address to,
           uint256 id,
           uint256 amount,
           bytes memory data
       ) internal {
           require(to != address(0), "Zero address");
           
           _beforeTokenTransfer(
               from,
               to,
               _asSingletonArray(id),
               _asSingletonArray(amount),
               data
           );
           
           uint256 fromBalance = _balances[id][from];
           require(fromBalance >= amount, "Insufficient balance");
           unchecked {
               _balances[id][from] = fromBalance - amount;
           }
           _balances[id][to] += amount;
           
           emit TransferSingle(
               msg.sender,
               from,
               to,
               id,
               amount
           );
           
           _doSafeTransferAcceptanceCheck(
               msg.sender,
               from,
               to,
               id,
               amount,
               data
           );
       }
   }
   ```

2. **safeBatchTransferFrom:**
   ```solidity
   contract ERC1155Batch {
       function safeBatchTransferFrom(
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) public {
           require(
               from == msg.sender || isApprovedForAll(from, msg.sender),
               "Not approved"
           );
           
           _safeBatchTransferFrom(from, to, ids, amounts, data);
       }
       
       function _safeBatchTransferFrom(
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal {
           require(to != address(0), "Zero address");
           require(
               ids.length == amounts.length,
               "Length mismatch"
           );
           
           _beforeTokenTransfer(from, to, ids, amounts, data);
           
           for (uint256 i = 0; i < ids.length;) {
               uint256 id = ids[i];
               uint256 amount = amounts[i];
               
               uint256 fromBalance = _balances[id][from];
               require(fromBalance >= amount, "Insufficient balance");
               unchecked {
                   _balances[id][from] = fromBalance - amount;
                   _balances[id][to] += amount;
                   i++;
               }
           }
           
           emit TransferBatch(
               msg.sender,
               from,
               to,
               ids,
               amounts
           );
           
           _doSafeBatchTransferAcceptanceCheck(
               msg.sender,
               from,
               to,
               ids,
               amounts,
               data
           );
       }
   }
   ```

### **2. Интерфейсы получателя**

1. **Одиночный трансфер:**
   ```solidity
   interface IERC1155Receiver {
       function onERC1155Received(
           address operator,
           address from,
           uint256 id,
           uint256 value,
           bytes calldata data
       ) external returns (bytes4);
   }
   ```

2. **Пакетный трансфер:**
   ```solidity
   interface IERC1155Receiver {
       function onERC1155BatchReceived(
           address operator,
           address from,
           uint256[] calldata ids,
           uint256[] calldata values,
           bytes calldata data
       ) external returns (bytes4);
   }
   ```

### **3. Оптимизации и особенности**

1. **Газовые оптимизации:**
   ```solidity
   contract OptimizedERC1155 is ERC1155 {
       // Кэширование селекторов
       bytes4 private constant _ERC1155_RECEIVED = 
           IERC1155Receiver.onERC1155Received.selector;
       
       bytes4 private constant _ERC1155_BATCH_RECEIVED = 
           IERC1155Receiver.onERC1155BatchReceived.selector;
       
       // Оптимизированная проверка получателя
       function _doSafeTransferAcceptanceCheck(
           address operator,
           address from,
           address to,
           uint256 id,
           uint256 amount,
           bytes memory data
       ) private {
           if (to.code.length > 0) {
               try IERC1155Receiver(to).onERC1155Received(
                   operator,
                   from,
                   id,
                   amount,
                   data
               ) returns (bytes4 response) {
                   if (response != _ERC1155_RECEIVED) {
                       revert("ERC1155: invalid receiver");
                   }
               } catch Error(string memory reason) {
                   revert(reason);
               } catch {
                   revert("ERC1155: transfer failed");
               }
           }
       }
   }
   ```

2. **Атомарность операций:**
   ```solidity
   contract AtomicERC1155 is ERC1155 {
       function atomicBatchTransfer(
           address[] memory from,
           address[] memory to,
           uint256[][] memory ids,
           uint256[][] memory amounts,
           bytes[] memory data
       ) external {
           require(
               from.length == to.length &&
               to.length == ids.length &&
               ids.length == amounts.length &&
               amounts.length == data.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < from.length;) {
               safeBatchTransferFrom(
                   from[i],
                   to[i],
                   ids[i],
                   amounts[i],
                   data[i]
               );
               
               unchecked { i++; }
           }
       }
   }
   ```

### **4. Безопасность и проверки**

1. **Проверки безопасности:**
   ```solidity
   contract SecureERC1155 is ERC1155 {
       modifier validBatchTransfer(
           uint256[] memory ids,
           uint256[] memory amounts
       ) {
           require(ids.length > 0, "Empty transfer");
           require(
               ids.length == amounts.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < amounts.length;) {
               require(amounts[i] > 0, "Zero amount");
               unchecked { i++; }
           }
           _;
       }
       
       function safeBatchTransferFrom(
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) public override validBatchTransfer(ids, amounts) {
           super.safeBatchTransferFrom(
               from,
               to,
               ids,
               amounts,
               data
           );
       }
   }
   ```

2. **Обработка ошибок:**
   ```solidity
   contract RobustERC1155 is ERC1155 {
       event BatchTransferFailed(
           address indexed from,
           address indexed to,
           uint256[] ids,
           uint256[] amounts,
           bytes reason
       );
       
       function tryBatchTransfer(
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) external returns (bool) {
           try this.safeBatchTransferFrom(
               from,
               to,
               ids,
               amounts,
               data
           ) {
               return true;
           } catch (bytes memory reason) {
               emit BatchTransferFailed(
                   from,
                   to,
                   ids,
                   amounts,
                   reason
               );
               return false;
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.]]
- [[Как и где хранить медиа-данные NFT или SFT?]]
- [[Какие потенциальные проблемы / уязвимости могут произойти при наличии механизма обратных вызовов?]]

---

## Источники
- [EIP-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [OpenZeppelin ERC1155 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC1155)
- [ERC1155 Security Considerations](https://consensys.github.io/smart-contract-best-practices/tokens/) 