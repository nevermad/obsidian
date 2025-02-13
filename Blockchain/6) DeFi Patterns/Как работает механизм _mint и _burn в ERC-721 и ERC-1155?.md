## Короткий ответ

`_mint` и `_burn` - это внутренние функции в ERC-721 и ERC-1155, которые отвечают за создание и уничтожение токенов. В ERC-721 они работают с уникальными токенами, а в ERC-1155 могут обрабатывать как уникальные, так и взаимозаменяемые токены, включая пакетные операции.

---

## Подробный разбор

### **1. Механизм в ERC-721**

1. **Функция _mint:**
   ```solidity
   contract ERC721Mint {
       function _mint(address to, uint256 tokenId) internal virtual {
           require(to != address(0), "ERC721: mint to zero address");
           require(!_exists(tokenId), "ERC721: token already minted");
           
           _beforeTokenTransfer(address(0), to, tokenId, 1);
           
           // Увеличиваем баланс
           _balances[to] += 1;
           // Устанавливаем владельца
           _owners[tokenId] = to;
           
           emit Transfer(address(0), to, tokenId);
           
           _afterTokenTransfer(address(0), to, tokenId, 1);
       }
   }
   ```

   **Технические детали:**
   - Проверяет валидность адреса получателя
   - Проверяет, что токен еще не существует
   - Вызывает хуки `_beforeTokenTransfer` и `_afterTokenTransfer`
   - Обновляет маппинги `_balances` и `_owners`
   - Эмитит событие `Transfer` с нулевого адреса

2. **Функция _burn:**
   ```solidity
   contract ERC721Burn {
       function _burn(uint256 tokenId) internal virtual {
           address owner = ownerOf(tokenId);
           
           _beforeTokenTransfer(owner, address(0), tokenId, 1);
           
           // Очищаем одобрения
           delete _tokenApprovals[tokenId];
           
           // Уменьшаем баланс
           _balances[owner] -= 1;
           delete _owners[tokenId];
           
           emit Transfer(owner, address(0), tokenId);
           
           _afterTokenTransfer(owner, address(0), tokenId, 1);
       }
   }
   ```

   **Технические детали:**
   - Проверяет существование токена через `ownerOf`
   - Очищает все одобрения для токена
   - Уменьшает баланс владельца
   - Удаляет запись о владельце
   - Эмитит событие `Transfer` на нулевой адрес

### **2. Механизм в ERC-1155**

1. **Функция _mint:**
   ```solidity
   contract ERC1155Mint {
       function _mint(
           address to,
           uint256 id,
           uint256 amount,
           bytes memory data
       ) internal virtual {
           require(to != address(0), "ERC1155: mint to zero address");
           
           address operator = _msgSender();
           uint256[] memory ids = _asSingletonArray(id);
           uint256[] memory amounts = _asSingletonArray(amount);
           
           _beforeTokenTransfer(operator, address(0), to, ids, amounts, data);
           
           // Увеличиваем баланс
           _balances[id][to] += amount;
           
           emit TransferSingle(operator, address(0), to, id, amount);
           
           _afterTokenTransfer(operator, address(0), to, ids, amounts, data);
           
           _doSafeTransferAcceptanceCheck(
               operator,
               address(0),
               to,
               id,
               amount,
               data
           );
       }
   }
   ```

   **Технические детали:**
   - Поддерживает создание нескольких токенов одного ID
   - Использует более сложную структуру маппингов для балансов
   - Включает проверку безопасного приема токенов
   - Поддерживает дополнительные данные при минте
   - Эмитит событие `TransferSingle`

2. **Функция _mintBatch:**
   ```solidity
   contract ERC1155MintBatch {
       function _mintBatch(
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual {
           require(to != address(0), "ERC1155: mint to zero address");
           require(
               ids.length == amounts.length,
               "ERC1155: lengths mismatch"
           );
           
           address operator = _msgSender();
           
           _beforeTokenTransfer(operator, address(0), to, ids, amounts, data);
           
           for (uint256 i = 0; i < ids.length;) {
               _balances[ids[i]][to] += amounts[i];
               unchecked { i++; }
           }
           
           emit TransferBatch(operator, address(0), to, ids, amounts);
           
           _afterTokenTransfer(operator, address(0), to, ids, amounts, data);
           
           _doSafeBatchTransferAcceptanceCheck(
               operator,
               address(0),
               to,
               ids,
               amounts,
               data
           );
       }
   }
   ```

   **Технические детали:**
   - Оптимизирован для пакетных операций
   - Использует unchecked для оптимизации газа в цикле
   - Проверяет соответствие длин массивов
   - Эмитит одно событие `TransferBatch` вместо множества `TransferSingle`

### **3. Безопасность и проверки**

1. **Проверки в ERC-721:**
   ```solidity
   contract ERC721Checks {
       function _exists(uint256 tokenId) internal view returns (bool) {
           return _owners[tokenId] != address(0);
       }
       
       function _isApprovedOrOwner(
           address spender,
           uint256 tokenId
       ) internal view returns (bool) {
           address owner = ownerOf(tokenId);
           return (
               spender == owner ||
               isApprovedForAll(owner, spender) ||
               getApproved(tokenId) == spender
           );
       }
   }
   ```

2. **Проверки в ERC-1155:**
   ```solidity
   contract ERC1155Checks {
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
                   if (response != IERC1155Receiver.onERC1155Received.selector) {
                       revert("ERC1155: ERC1155Receiver rejected tokens");
                   }
               } catch Error(string memory reason) {
                   revert(reason);
               } catch {
                   revert("ERC1155: transfer to non-ERC1155Receiver");
               }
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Опишите основные функции, события и особенности поведения ERC-721 токенов?]]
- [[Опишите основные функции, события и особенности поведения ERC-1155 токенов?]]
- [[Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.]]

---

## Источники
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [OpenZeppelin ERC721 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol)
- [OpenZeppelin ERC1155 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol) 