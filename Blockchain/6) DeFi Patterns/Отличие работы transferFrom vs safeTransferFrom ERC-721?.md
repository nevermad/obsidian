## Короткий ответ

Основное отличие между `transferFrom` и `safeTransferFrom` в ERC-721 заключается в том, что `safeTransferFrom` проверяет способность получателя (если это контракт) принимать NFT через вызов `onERC721Received`. Это предотвращает потерю токенов при отправке на контракты, не поддерживающие ERC-721. `transferFrom` такой проверки не делает.

---

## Подробный разбор

### **1. Базовая реализация**

1. **transferFrom:**
   ```solidity
   contract ERC721Base {
       function transferFrom(
           address from,
           address to,
           uint256 tokenId
       ) public {
           require(
               _isApprovedOrOwner(msg.sender, tokenId),
               "Not approved"
           );
           
           // Прямой трансфер без проверок
           _transfer(from, to, tokenId);
       }
       
       function _transfer(
           address from,
           address to,
           uint256 tokenId
       ) internal {
           require(ownerOf(tokenId) == from, "Wrong owner");
           require(to != address(0), "Zero address");
           
           _beforeTokenTransfer(from, to, tokenId);
           
           _balances[from] -= 1;
           _balances[to] += 1;
           _owners[tokenId] = to;
           
           emit Transfer(from, to, tokenId);
       }
   }
   ```

2. **safeTransferFrom:**
   ```solidity
   contract ERC721Safe {
       function safeTransferFrom(
           address from,
           address to,
           uint256 tokenId,
           bytes memory data
       ) public {
           require(
               _isApprovedOrOwner(msg.sender, tokenId),
               "Not approved"
           );
           
           _safeTransfer(from, to, tokenId, data);
       }
       
       function _safeTransfer(
           address from,
           address to,
           uint256 tokenId,
           bytes memory data
       ) internal {
           _transfer(from, to, tokenId);
           
           if (to.code.length > 0) {
               try IERC721Receiver(to).onERC721Received(
                   msg.sender,
                   from,
                   tokenId,
                   data
               ) returns (bytes4 retval) {
                   require(
                       retval == IERC721Receiver.onERC721Received.selector,
                       "Invalid receiver"
                   );
               } catch (bytes memory reason) {
                   if (reason.length == 0) {
                       revert("Non-receiver contract");
                   } else {
                       assembly {
                           revert(add(32, reason), mload(reason))
                       }
                   }
               }
           }
       }
   }
   ```

### **2. Интерфейс получателя**

1. **ERC721Receiver:**
   ```solidity
   interface IERC721Receiver {
       function onERC721Received(
           address operator,
           address from,
           uint256 tokenId,
           bytes calldata data
       ) external returns (bytes4);
   }
   ```

2. **Пример имплементации:**
   ```solidity
   contract NFTReceiver is IERC721Receiver {
       function onERC721Received(
           address operator,
           address from,
           uint256 tokenId,
           bytes calldata data
       ) external override returns (bytes4) {
           // Логика обработки полученного NFT
           
           return IERC721Receiver.onERC721Received.selector;
       }
   }
   ```

### **3. Примеры использования**

1. **Небезопасный контракт:**
   ```solidity
   contract UnsafeContract {
       IERC721 public nft;
       
       // Токены будут заблокированы при использовании transferFrom
       function deposit(uint256 tokenId) external {
           nft.transferFrom(msg.sender, address(this), tokenId);
       }
   }
   ```

2. **Безопасный контракт:**
   ```solidity
   contract SafeContract is IERC721Receiver {
       IERC721 public nft;
       mapping(uint256 => address) public depositors;
       
       function onERC721Received(
           address operator,
           address from,
           uint256 tokenId,
           bytes calldata
       ) external override returns (bytes4) {
           require(msg.sender == address(nft), "Wrong NFT");
           depositors[tokenId] = from;
           return IERC721Receiver.onERC721Received.selector;
       }
       
       function deposit(uint256 tokenId) external {
           // Токены будут приняты корректно
           nft.safeTransferFrom(msg.sender, address(this), tokenId);
       }
   }
   ```

### **4. Edge Cases и Безопасность**

1. **Рекурсивные вызовы:**
   ```solidity
   contract MaliciousReceiver is IERC721Receiver {
       IERC721 public nft;
       
       function onERC721Received(
           address operator,
           address from,
           uint256 tokenId,
           bytes calldata
       ) external override returns (bytes4) {
           // Попытка рекурсивного вызова
           if (nft.ownerOf(tokenId) == address(this)) {
               nft.safeTransferFrom(
                   address(this),
                   from,
                   tokenId
               );
           }
           return IERC721Receiver.onERC721Received.selector;
       }
   }
   ```

2. **Защита от рекурсии:**
   ```solidity
   contract SecureNFTReceiver is IERC721Receiver {
       uint256 private _locked;
       
       modifier nonReentrant() {
           require(_locked == 0, "Reentrant call");
           _locked = 1;
           _;
           _locked = 0;
       }
       
       function onERC721Received(
           address operator,
           address from,
           uint256 tokenId,
           bytes calldata data
       ) external override nonReentrant returns (bytes4) {
           // Безопасная обработка
           return IERC721Receiver.onERC721Received.selector;
       }
   }
   ```

### **5. Оптимизации и улучшения**

1. **Газовые оптимизации:**
   ```solidity
   contract GasOptimizedNFT is ERC721 {
       // Кэширование селектора
       bytes4 private constant _ERC721_RECEIVED = 
           IERC721Receiver.onERC721Received.selector;
       
       function _checkOnERC721Received(
           address from,
           address to,
           uint256 tokenId,
           bytes memory data
       ) private returns (bool) {
           if (to.code.length == 0) {
               return true;
           }
           
           try IERC721Receiver(to).onERC721Received(
               msg.sender,
               from,
               tokenId,
               data
           ) returns (bytes4 retval) {
               return retval == _ERC721_RECEIVED;
           } catch {
               return false;
           }
       }
   }
   ```

2. **Расширенная функциональность:**
   ```solidity
   contract EnhancedNFT is ERC721 {
       event TransferFailed(
           address indexed from,
           address indexed to,
           uint256 indexed tokenId,
           bytes reason
       );
       
       function safeBatchTransfer(
           address[] calldata from,
           address[] calldata to,
           uint256[] calldata tokenIds,
           bytes[] calldata data
       ) external {
           require(
               from.length == to.length &&
               to.length == tokenIds.length &&
               tokenIds.length == data.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < tokenIds.length;) {
               try this.safeTransferFrom(
                   from[i],
                   to[i],
                   tokenIds[i],
                   data[i]
               ) {
                   // Успешный трансфер
               } catch (bytes memory reason) {
                   emit TransferFailed(
                       from[i],
                       to[i],
                       tokenIds[i],
                       reason
                   );
               }
               
               unchecked { i++; }
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Опишите основные функции, события и особенности поведения ERC-721 токенов?]]
- [[С помощью каких функций израсходовать выданный approve ERC-721?]]
- [[Какие потенциальные проблемы / уязвимости могут произойти при наличии механизма обратных вызовов?]]

---

## Источники
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [OpenZeppelin ERC721 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC721)
- [NFT Security Best Practices](https://consensys.github.io/smart-contract-best-practices/tokens/) 