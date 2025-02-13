## Короткий ответ

Наиболее популярные ERC стандарты включают: ERC-20 (взаимозаменяемые токены), ERC-721 (невзаимозаменяемые токены), ERC-1155 (мульти-токены), ERC-4626 (токенизированные хранилища), ERC-2981 (роялти для NFT).

---

## Подробный разбор

### **1. ERC-20: Token Standard**

1. **Основной интерфейс:**
   ```solidity
   interface IERC20 {
       function totalSupply() external view returns (uint256);
       function balanceOf(address account) external view returns (uint256);
       function transfer(address to, uint256 amount) external returns (bool);
       function allowance(address owner, address spender) external view returns (uint256);
       function approve(address spender, uint256 amount) external returns (bool);
       function transferFrom(address from, address to, uint256 amount) external returns (bool);
       
       event Transfer(address indexed from, address indexed to, uint256 value);
       event Approval(address indexed owner, address indexed spender, uint256 value);
   }
   ```

2. **Особенности:**
   - Атомарные операции
   - Механизм allowance
   - Единый интерфейс для DEX
   - Поддержка делегированных трансферов

### **2. ERC-721: Non-Fungible Token**

1. **Ключевые функции:**
   ```solidity
   interface IERC721 {
       function balanceOf(address owner) external view returns (uint256);
       function ownerOf(uint256 tokenId) external view returns (address);
       function safeTransferFrom(address from, address to, uint256 tokenId, bytes calldata data) external;
       function safeTransferFrom(address from, address to, uint256 tokenId) external;
       function transferFrom(address from, address to, uint256 tokenId) external;
       function approve(address to, uint256 tokenId) external;
       function setApprovalForAll(address operator, bool approved) external;
       function getApproved(uint256 tokenId) external view returns (address);
       function isApprovedForAll(address owner, address operator) external view returns (bool);
   }
   ```

2. **Расширения:**
   ```solidity
   interface IERC721Metadata {
       function name() external view returns (string memory);
       function symbol() external view returns (string memory);
       function tokenURI(uint256 tokenId) external view returns (string memory);
   }
   
   interface IERC721Enumerable {
       function totalSupply() external view returns (uint256);
       function tokenOfOwnerByIndex(address owner, uint256 index) external view returns (uint256);
       function tokenByIndex(uint256 index) external view returns (uint256);
   }
   ```

### **3. ERC-1155: Multi Token Standard**

1. **Основной функционал:**
   ```solidity
   interface IERC1155 {
       function balanceOf(address account, uint256 id) external view returns (uint256);
       function balanceOfBatch(address[] calldata accounts, uint256[] calldata ids) 
           external view returns (uint256[] memory);
       
       function setApprovalForAll(address operator, bool approved) external;
       function isApprovedForAll(address account, address operator) external view returns (bool);
       
       function safeTransferFrom(
           address from,
           address to,
           uint256 id,
           uint256 amount,
           bytes calldata data
       ) external;
       
       function safeBatchTransferFrom(
           address from,
           address to,
           uint256[] calldata ids,
           uint256[] calldata amounts,
           bytes calldata data
       ) external;
   }
   ```

2. **Преимущества:**
   - Пакетные операции
   - Поддержка fungible и non-fungible токенов
   - Оптимизация газа
   - Атомарные свопы

### **4. ERC-4626: Tokenized Vault**

1. **Интерфейс хранилища:**
   ```solidity
   interface IERC4626 is IERC20 {
       function asset() external view returns (address assetTokenAddress);
       
       // Депозит/Вывод
       function deposit(uint256 assets, address receiver) external returns (uint256 shares);
       function mint(uint256 shares, address receiver) external returns (uint256 assets);
       function withdraw(uint256 assets, address receiver, address owner) external returns (uint256 shares);
       function redeem(uint256 shares, address receiver, address owner) external returns (uint256 assets);
       
       // Бухгалтерия
       function totalAssets() external view returns (uint256);
       function convertToShares(uint256 assets) external view returns (uint256);
       function convertToAssets(uint256 shares) external view returns (uint256);
       function previewDeposit(uint256 assets) external view returns (uint256);
       function previewMint(uint256 shares) external view returns (uint256);
       function previewWithdraw(uint256 assets) external view returns (uint256);
       function previewRedeem(uint256 shares) external view returns (uint256);
       
       // Лимиты
       function maxDeposit(address receiver) external view returns (uint256);
       function maxMint(address receiver) external view returns (uint256);
       function maxWithdraw(address owner) external view returns (uint256);
       function maxRedeem(address owner) external view returns (uint256);
   }
   ```

2. **Применение:**
   - Yield-фарминг протоколы
   - Стейкинг пулы
   - Автоматизированные стратегии

### **5. ERC-2981: NFT Royalty Standard**

1. **Базовый интерфейс:**
   ```solidity
   interface IERC2981 {
       function royaltyInfo(
           uint256 tokenId,
           uint256 salePrice
       ) external view returns (
           address receiver,
           uint256 royaltyAmount
       );
   }
   ```

2. **Пример имплементации:**
   ```solidity
   contract ERC2981Implementation is IERC2981 {
       struct RoyaltyInfo {
           address receiver;
           uint96 royaltyFraction;
       }
       
       mapping(uint256 => RoyaltyInfo) private _tokenRoyaltyInfo;
       RoyaltyInfo private _defaultRoyaltyInfo;
       
       function royaltyInfo(
           uint256 tokenId,
           uint256 salePrice
       ) external view override returns (
           address receiver,
           uint256 royaltyAmount
       ) {
           RoyaltyInfo memory royalty = _tokenRoyaltyInfo[tokenId];
           if (royalty.receiver == address(0)) {
               royalty = _defaultRoyaltyInfo;
           }
           
           return (
               royalty.receiver,
               (salePrice * royalty.royaltyFraction) / _feeDenominator()
           );
       }
       
       function _feeDenominator() internal pure virtual returns (uint96) {
           return 10000;
       }
   }
   ```

---

## Связанные темы
- [[Что такое ERC?]]
- [[Опишите основные функции, события и особенности поведения ERC-20 токенов?]]
- [[Что такое и в чем различие fungible token, non-fungible token, semi-fungible token? Приведите примеры.]]

---

## Источники
- [ERC-20 Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [ERC-721 Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [ERC-1155 Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [ERC-4626 Tokenized Vault Standard](https://eips.ethereum.org/EIPS/eip-4626)
- [ERC-2981 NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981) 