## Короткий ответ

После получения approve в ERC-721 можно использовать функции `transferFrom` или `safeTransferFrom` для перемещения одобренного токена. Approve может быть выдан как на конкретный токен через `approve(address, tokenId)`, так и на все токены владельца через `setApprovalForAll(address, bool)`.

---

## Подробный разбор

### **1. Типы одобрений**

1. **Одобрение на конкретный токен:**
   ```solidity
   interface IERC721 {
       // Одобрение на один токен
       function approve(address to, uint256 tokenId) external;
       
       // Проверка одобрения
       function getApproved(
           uint256 tokenId
       ) external view returns (address operator);
   }
   ```

2. **Одобрение на все токены:**
   ```solidity
   interface IERC721 {
       // Одобрение оператору на все токены
       function setApprovalForAll(
           address operator,
           bool approved
       ) external;
       
       // Проверка одобрения
       function isApprovedForAll(
           address owner,
           address operator
       ) external view returns (bool);
   }
   ```

### **2. Использование одобрений**

1. **Базовый трансфер:**
   ```solidity
   contract NFTMarketplace {
       IERC721 public nft;
       
       function executeTransfer(
           address from,
           address to,
           uint256 tokenId
       ) external {
           // Проверка одобрения
           require(
               nft.getApproved(tokenId) == address(this) ||
               nft.isApprovedForAll(from, address(this)),
               "Not approved"
           );
           
           // Выполнение трансфера
           nft.transferFrom(from, to, tokenId);
       }
   }
   ```

2. **Безопасный трансфер:**
   ```solidity
   contract SafeNFTMarketplace {
       IERC721 public nft;
       
       function executeSafeTransfer(
           address from,
           address to,
           uint256 tokenId,
           bytes calldata data
       ) external {
           // Проверка одобрения
           require(
               nft.getApproved(tokenId) == address(this) ||
               nft.isApprovedForAll(from, address(this)),
               "Not approved"
           );
           
           // Безопасный трансфер
           nft.safeTransferFrom(from, to, tokenId, data);
       }
   }
   ```

### **3. Примеры использования в DeFi**

1. **NFT Маркетплейс:**
   ```solidity
   contract NFTMarket {
       struct Listing {
           address seller;
           uint256 price;
           bool active;
       }
       
       IERC721 public nft;
       mapping(uint256 => Listing) public listings;
       
       function listNFT(uint256 tokenId, uint256 price) external {
           require(
               nft.ownerOf(tokenId) == msg.sender,
               "Not owner"
           );
           
           // Получаем одобрение на токен
           nft.approve(address(this), tokenId);
           
           listings[tokenId] = Listing({
               seller: msg.sender,
               price: price,
               active: true
           });
       }
       
       function buyNFT(uint256 tokenId) external payable {
           Listing storage listing = listings[tokenId];
           require(listing.active, "Not listed");
           require(msg.value >= listing.price, "Insufficient payment");
           
           // Используем одобрение
           nft.transferFrom(listing.seller, msg.sender, tokenId);
           
           // Очищаем листинг
           delete listings[tokenId];
           
           // Отправляем оплату продавцу
           payable(listing.seller).transfer(msg.value);
       }
   }
   ```

2. **NFT Стейкинг:**
   ```solidity
   contract NFTStaking {
       IERC721 public nft;
       mapping(uint256 => address) public tokenStaker;
       mapping(address => uint256) public stakedSince;
       
       function stake(uint256 tokenId) external {
           require(
               nft.ownerOf(tokenId) == msg.sender,
               "Not owner"
           );
           
           // Получаем токен
           nft.transferFrom(msg.sender, address(this), tokenId);
           
           // Записываем стейк
           tokenStaker[tokenId] = msg.sender;
           stakedSince[msg.sender] = block.timestamp;
       }
       
       function unstake(uint256 tokenId) external {
           require(
               tokenStaker[tokenId] == msg.sender,
               "Not staker"
           );
           
           // Возвращаем токен
           nft.transferFrom(address(this), msg.sender, tokenId);
           
           // Очищаем записи
           delete tokenStaker[tokenId];
           delete stakedSince[msg.sender];
       }
   }
   ```

### **4. Безопасное использование**

1. **Проверки безопасности:**
   ```solidity
   contract SafeNFTOperator {
       IERC721 public nft;
       
       modifier onlyApproved(uint256 tokenId) {
           require(
               nft.getApproved(tokenId) == address(this) ||
               nft.isApprovedForAll(nft.ownerOf(tokenId), address(this)),
               "Not approved"
           );
           _;
       }
       
       function executeTransfer(
           address from,
           address to,
           uint256 tokenId
       ) external onlyApproved(tokenId) {
           // Проверка существования токена
           require(
               nft.ownerOf(tokenId) == from,
               "Not owner"
           );
           
           // Проверка получателя
           require(to != address(0), "Zero address");
           
           // Выполнение трансфера
           nft.safeTransferFrom(from, to, tokenId);
       }
   }
   ```

2. **Обработка ошибок:**
   ```solidity
   contract RobustNFTOperator {
       IERC721 public nft;
       
       event TransferFailed(
           uint256 tokenId,
           address from,
           address to,
           bytes reason
       );
       
       function tryTransfer(
           address from,
           address to,
           uint256 tokenId
       ) external returns (bool) {
           try nft.transferFrom(from, to, tokenId) {
               return true;
           } catch (bytes memory reason) {
               emit TransferFailed(tokenId, from, to, reason);
               return false;
           }
       }
   }
   ```

### **5. Оптимизации**

1. **Пакетные операции:**
   ```solidity
   contract BatchNFTOperator {
       IERC721 public nft;
       
       function batchTransfer(
           address[] calldata from,
           address[] calldata to,
           uint256[] calldata tokenIds
       ) external {
           require(
               from.length == to.length &&
               to.length == tokenIds.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < tokenIds.length;) {
               require(
                   nft.getApproved(tokenIds[i]) == address(this) ||
                   nft.isApprovedForAll(from[i], address(this)),
                   "Not approved"
               );
               
               nft.transferFrom(from[i], to[i], tokenIds[i]);
               
               unchecked { i++; }
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Опишите основные функции, события и особенности поведения ERC-721 токенов?]]
- [[Отличие работы transferFrom vs safeTransferFrom ERC-721?]]
- [[Какие потенциальные проблемы / уязвимости могут произойти при наличии механизма обратных вызовов?]]

---

## Источники
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [OpenZeppelin ERC721 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC721)
- [NFT Security Considerations](https://consensys.github.io/smart-contract-best-practices/tokens/) 