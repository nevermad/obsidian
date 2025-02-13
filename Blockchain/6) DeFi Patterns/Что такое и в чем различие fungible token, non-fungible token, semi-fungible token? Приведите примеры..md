## Короткий ответ

Fungible tokens (FT) - взаимозаменяемые токены, где каждая единица идентична (ERC-20). Non-fungible tokens (NFT) - уникальные токены с индивидуальными характеристиками (ERC-721). Semi-fungible tokens (SFT) - токены, которые могут быть как взаимозаменяемыми, так и уникальными в зависимости от контекста (ERC-1155).

---

## Подробный разбор

### **1. Fungible Tokens (FT)**

1. **Характеристики:**
   ```solidity
   interface IFungibleToken {
       // Каждый токен идентичен другому
       function balanceOf(address account) external view returns (uint256);
       
       // Дробное деление возможно
       function decimals() external view returns (uint8);
       
       // Взаимозаменяемость
       function transfer(address to, uint256 amount) external returns (bool);
   }
   ```

2. **Примеры реализации:**
   ```solidity
   contract ERC20Token is IERC20 {
       mapping(address => uint256) private _balances;
       uint256 private _totalSupply;
       
       // Любые 100 токенов равны любым другим 100 токенам
       function transfer(address to, uint256 amount) external override returns (bool) {
           address owner = msg.sender;
           _transfer(owner, to, amount);
           return true;
       }
   }
   ```

3. **Реальные примеры:**
   - USDT (Tether)
   - WETH (Wrapped Ether)
   - UNI (Uniswap)

### **2. Non-Fungible Tokens (NFT)**

1. **Характеристики:**
   ```solidity
   interface INonFungibleToken {
       // Каждый токен уникален
       function ownerOf(uint256 tokenId) external view returns (address);
       
       // Метаданные для каждого токена
       function tokenURI(uint256 tokenId) external view returns (string memory);
       
       // Передача конкретного токена
       function transferFrom(address from, address to, uint256 tokenId) external;
   }
   ```

2. **Пример реализации:**
   ```solidity
   contract ERC721Token is IERC721 {
       // Маппинг для хранения владельцев
       mapping(uint256 => address) private _owners;
       
       // Маппинг для хранения метаданных
       mapping(uint256 => string) private _tokenURIs;
       
       function mint(address to, uint256 tokenId, string memory uri) external {
           require(_owners[tokenId] == address(0), "Token already exists");
           _owners[tokenId] = to;
           _tokenURIs[tokenId] = uri;
           emit Transfer(address(0), to, tokenId);
       }
       
       function tokenURI(uint256 tokenId) external view returns (string memory) {
           require(_owners[tokenId] != address(0), "Token does not exist");
           return _tokenURIs[tokenId];
       }
   }
   ```

3. **Реальные примеры:**
   - CryptoPunks
   - Bored Ape Yacht Club
   - Art Blocks

### **3. Semi-Fungible Tokens (SFT)**

1. **Характеристики:**
   ```solidity
   interface ISemiFungibleToken {
       // Поддержка как fungible, так и non-fungible токенов
       function balanceOf(address account, uint256 id) external view returns (uint256);
       
       // Пакетные операции
       function balanceOfBatch(
           address[] calldata accounts,
           uint256[] calldata ids
       ) external view returns (uint256[] memory);
   }
   ```

2. **Пример реализации:**
   ```solidity
   contract ERC1155Token is IERC1155 {
       // Маппинг для хранения балансов
       mapping(uint256 => mapping(address => uint256)) private _balances;
       
       // Маппинг для хранения метаданных
       mapping(uint256 => string) private _uris;
       
       function mint(
           address to,
           uint256 id,
           uint256 amount,
           string memory uri
       ) external {
           _balances[id][to] += amount;
           _uris[id] = uri;
           emit TransferSingle(msg.sender, address(0), to, id, amount);
       }
       
       function uri(uint256 id) external view returns (string memory) {
           return _uris[id];
       }
   }
   ```

3. **Примеры использования:**
   ```solidity
   contract GameItems is ERC1155 {
       uint256 public constant GOLD = 0;      // Fungible
       uint256 public constant SILVER = 1;    // Fungible
       uint256 public constant SWORD = 2;     // Semi-fungible
       uint256 public constant SHIELD = 3;    // Semi-fungible
       uint256 public constant CROWN = 4;     // Non-fungible
       
       constructor() ERC1155("https://game.example/api/item/{id}.json") {
           _mint(msg.sender, GOLD, 10**18, "");    // 1M золота
           _mint(msg.sender, SILVER, 10**27, "");  // 1B серебра
           _mint(msg.sender, SWORD, 1000, "");     // 1000 мечей
           _mint(msg.sender, SHIELD, 1000, "");    // 1000 щитов
           _mint(msg.sender, CROWN, 1, "");        // 1 уникальная корона
       }
   }
   ```

### **Сравнительный анализ**

1. **Хранение данных:**
   ```solidity
   // FT (ERC-20)
   mapping(address => uint256) balances;
   
   // NFT (ERC-721)
   mapping(uint256 => address) owners;
   mapping(uint256 => string) tokenURIs;
   
   // SFT (ERC-1155)
   mapping(uint256 => mapping(address => uint256)) balances;
   mapping(uint256 => string) uris;
   ```

2. **Газовые затраты:**
   | Операция | FT | NFT | SFT |
   |----------|----|----|-----|
   | Трансфер | ~65k | ~85k | ~70k |
   | Минт | ~50k | ~70k | ~60k |
   | Пакетный трансфер | N/A | N/A | ~40k/item |

3. **Применение:**
   - **FT:** Финансовые инструменты, стейблкоины
   - **NFT:** Цифровое искусство, коллекционные предметы
   - **SFT:** Игровые предметы, билеты, варранты

---

## Связанные темы
- [[6. Список вопросов]]
- [[Опишите основные функции, события и особенности поведения ERC-20 токенов?]]
- [[Опишите основные функции, события и особенности поведения ERC-721 токенов?]]
- [[Отличие работы safeTransferFrom vs safeBatchTransferFrom ERC-1155?]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-1155: Multi Token Standard](https://eips.ethereum.org/EIPS/eip-1155)
- [OpenZeppelin ERC Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token) 