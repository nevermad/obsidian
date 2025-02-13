## Короткий ответ

`_beforeTokenTransfer` и `_afterTokenTransfer` - это внутренние хуки в ERC-721 и ERC-1155, которые вызываются до и после каждой операции с токенами (mint, burn, transfer). Они позволяют добавлять кастомную логику, валидацию и дополнительные действия при операциях с токенами.

---

## Подробный разбор

### **1. Механизм в ERC-721**

1. **Базовая реализация:**
   ```solidity
   contract ERC721Transfer {
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual {
           // Пустая реализация по умолчанию
       }
       
       function _afterTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual {
           // Пустая реализация по умолчанию
       }
       
       function _transfer(
           address from,
           address to,
           uint256 tokenId
       ) internal virtual {
           require(ownerOf(tokenId) == from, "Not owner");
           require(to != address(0), "Zero address");
           
           _beforeTokenTransfer(from, to, tokenId, 1);
           
           // Очищаем одобрения
           _approve(address(0), tokenId);
           
           _balances[from] -= 1;
           _balances[to] += 1;
           _owners[tokenId] = to;
           
           emit Transfer(from, to, tokenId);
           
           _afterTokenTransfer(from, to, tokenId, 1);
       }
   }
   ```

2. **Примеры расширений:**
   ```solidity
   contract PausableERC721 is ERC721 {
       bool private _paused;
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual override {
           super._beforeTokenTransfer(from, to, tokenId, batchSize);
           require(!_paused, "Token transfers are paused");
       }
   }
   
   contract EnumerableERC721 is ERC721 {
       mapping(address => mapping(uint256 => uint256)) private _ownedTokens;
       mapping(uint256 => uint256) private _ownedTokensIndex;
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual override {
           super._beforeTokenTransfer(from, to, tokenId, batchSize);
           
           if (from != address(0)) {
               // Удаляем из списка токенов отправителя
               _removeTokenFromOwnerEnumeration(from, tokenId);
           }
           if (to != address(0)) {
               // Добавляем в список токенов получателя
               _addTokenToOwnerEnumeration(to, tokenId);
           }
       }
   }
   ```

### **2. Механизм в ERC-1155**

1. **Базовая реализация:**
   ```solidity
   contract ERC1155Transfer {
       function _beforeTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual {
           // Пустая реализация по умолчанию
       }
       
       function _afterTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual {
           // Пустая реализация по умолчанию
       }
       
       function _safeTransferFrom(
           address from,
           address to,
           uint256 id,
           uint256 amount,
           bytes memory data
       ) internal virtual {
           require(to != address(0), "Zero address");
           
           address operator = msg.sender;
           uint256[] memory ids = _asSingletonArray(id);
           uint256[] memory amounts = _asSingletonArray(amount);
           
           _beforeTokenTransfer(operator, from, to, ids, amounts, data);
           
           uint256 fromBalance = _balances[id][from];
           require(fromBalance >= amount, "Insufficient balance");
           unchecked {
               _balances[id][from] = fromBalance - amount;
           }
           _balances[id][to] += amount;
           
           emit TransferSingle(operator, from, to, id, amount);
           
           _afterTokenTransfer(operator, from, to, ids, amounts, data);
           
           _doSafeTransferAcceptanceCheck(
               operator,
               from,
               to,
               id,
               amount,
               data
           );
       }
   }
   ```

2. **Примеры расширений:**
   ```solidity
   contract PausableERC1155 is ERC1155 {
       bool private _paused;
       
       function _beforeTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual override {
           super._beforeTokenTransfer(
               operator,
               from,
               to,
               ids,
               amounts,
               data
           );
           require(!_paused, "Token transfers are paused");
       }
   }
   
   contract SupplyTrackedERC1155 is ERC1155 {
       mapping(uint256 => uint256) private _totalSupply;
       
       function _beforeTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual override {
           super._beforeTokenTransfer(
               operator,
               from,
               to,
               ids,
               amounts,
               data
           );
           
           for (uint256 i = 0; i < ids.length;) {
               if (from == address(0)) {
                   // Mint - увеличиваем общее предложение
                   _totalSupply[ids[i]] += amounts[i];
               }
               if (to == address(0)) {
                   // Burn - уменьшаем общее предложение
                   _totalSupply[ids[i]] -= amounts[i];
               }
               unchecked { i++; }
           }
       }
   }
   ```

### **3. Практические применения**

1. **Ограничение максимального предложения:**
   ```solidity
   contract MaxSupplyERC721 is ERC721 {
       uint256 private constant MAX_SUPPLY = 10000;
       uint256 private _currentSupply;
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual override {
           super._beforeTokenTransfer(from, to, tokenId, batchSize);
           
           if (from == address(0)) { // Mint
               require(
                   _currentSupply + batchSize <= MAX_SUPPLY,
                   "Max supply exceeded"
               );
               _currentSupply += batchSize;
           }
           if (to == address(0)) { // Burn
               _currentSupply -= batchSize;
           }
       }
   }
   ```

2. **Блокировка токенов:**
   ```solidity
   contract LockableERC1155 is ERC1155 {
       mapping(uint256 => bool) private _locked;
       
       function _beforeTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual override {
           super._beforeTokenTransfer(
               operator,
               from,
               to,
               ids,
               amounts,
               data
           );
           
           for (uint256 i = 0; i < ids.length;) {
               require(!_locked[ids[i]], "Token is locked");
               unchecked { i++; }
           }
       }
       
       function lockToken(uint256 id) external onlyOwner {
           _locked[id] = true;
       }
   }
   ```

### **4. Безопасность и оптимизация**

1. **Защита от reentrancy:**
   ```solidity
   contract ReentrancyProtectedERC721 is ERC721 {
       uint256 private _status;
       
       modifier nonReentrant() {
           require(_status == 0, "Reentrant call");
           _status = 1;
           _;
           _status = 0;
       }
       
       function _beforeTokenTransfer(
           address from,
           address to,
           uint256 tokenId,
           uint256 batchSize
       ) internal virtual override nonReentrant {
           super._beforeTokenTransfer(from, to, tokenId, batchSize);
       }
   }
   ```

2. **Оптимизация газа:**
   ```solidity
   contract GasOptimizedERC1155 is ERC1155 {
       function _beforeTokenTransfer(
           address operator,
           address from,
           address to,
           uint256[] memory ids,
           uint256[] memory amounts,
           bytes memory data
       ) internal virtual override {
           // Минимизируем количество storage операций
           uint256 idsLength = ids.length;
           for (uint256 i = 0; i < idsLength;) {
               // Используем memory вместо storage где возможно
               uint256 id = ids[i];
               uint256 amount = amounts[i];
               
               // Логика проверок
               
               unchecked { i++; }
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Как работает механизм _mint и _burn в ERC-721 и ERC-1155?]]
- [[Как работает механизм обратных вызовов в ERC-721 и ERC-1155?]]
- [[Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.]]

---

## Источники
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [OpenZeppelin ERC721](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC721)
- [OpenZeppelin ERC1155](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC1155) 