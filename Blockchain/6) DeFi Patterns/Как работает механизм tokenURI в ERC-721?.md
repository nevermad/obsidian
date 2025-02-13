## Короткий ответ

`tokenURI` - это функция в ERC-721, которая возвращает URI для метаданных токена. Метаданные обычно содержат информацию о названии, описании и изображении NFT. URI может быть как IPFS хешем (ipfs://...), так и HTTP URL (https://...). Функция является частью расширения ERC721Metadata и возвращает строку, которая должна соответствовать определенному JSON-формату.

---

## Подробный разбор

### **1. Базовая реализация**

1. **Интерфейс ERC721Metadata:**
   ```solidity
   interface IERC721Metadata is IERC721 {
       function name() external view returns (string memory);
       function symbol() external view returns (string memory);
       function tokenURI(uint256 tokenId) external view returns (string memory);
   }
   ```

2. **Стандартная реализация:**
   ```solidity
   contract ERC721URIStorage is ERC721 {
       // Маппинг для хранения URI токенов
       mapping(uint256 => string) private _tokenURIs;
       
       function tokenURI(uint256 tokenId)
           public
           view
           virtual
           override
           returns (string memory)
       {
           require(
               _exists(tokenId),
               "URI query for nonexistent token"
           );
           
           string memory _tokenURI = _tokenURIs[tokenId];
           string memory base = _baseURI();
           
           // Если нет базового URI, возвращаем URI токена
           if (bytes(base).length == 0) {
               return _tokenURI;
           }
           // Если нет URI токена, возвращаем базовый URI
           if (bytes(_tokenURI).length == 0) {
               return base;
           }
           
           // Если есть оба, конкатенируем их
           return string(abi.encodePacked(base, _tokenURI));
       }
       
       function _setTokenURI(uint256 tokenId, string memory _tokenURI)
           internal
           virtual
       {
           require(
               _exists(tokenId),
               "URI set for nonexistent token"
           );
           _tokenURIs[tokenId] = _tokenURI;
       }
   }
   ```

### **2. Форматы метаданных**

1. **Стандартный JSON формат:**
   ```json
   {
       "name": "Asset Name",
       "description": "Asset Description",
       "image": "https://example.com/image.png",
       "attributes": [
           {
               "trait_type": "Color",
               "value": "Blue"
           },
           {
               "trait_type": "Size",
               "value": "Large"
           }
       ]
   }
   ```

2. **Генерация метаданных в контракте:**
   ```solidity
   contract DynamicNFT is ERC721URIStorage {
       using Strings for uint256;
       
       struct TokenMetadata {
           string name;
           string description;
           string image;
           Attribute[] attributes;
       }
       
       struct Attribute {
           string trait_type;
           string value;
       }
       
       function generateTokenURI(
           uint256 tokenId,
           TokenMetadata memory metadata
       ) internal pure returns (string memory) {
           return string(
               abi.encodePacked(
                   'data:application/json;base64,',
                   Base64.encode(
                       bytes(
                           abi.encodePacked(
                               '{"name":"', metadata.name, '",',
                               '"description":"', metadata.description, '",',
                               '"image":"', metadata.image, '",',
                               '"attributes":', _generateAttributes(metadata.attributes), '}'
                           )
                       )
                   )
               )
           );
       }
       
       function _generateAttributes(Attribute[] memory attributes)
           internal
           pure
           returns (string memory)
       {
           string memory attrs = '[';
           for (uint i = 0; i < attributes.length;) {
               if (i > 0) {
                   attrs = string(abi.encodePacked(attrs, ','));
               }
               attrs = string(
                   abi.encodePacked(
                       attrs,
                       '{"trait_type":"', attributes[i].trait_type, '",',
                       '"value":"', attributes[i].value, '"}'
                   )
               );
               unchecked { i++; }
           }
           return string(abi.encodePacked(attrs, ']'));
       }
   }
   ```

### **3. IPFS интеграция**

1. **Базовая реализация с IPFS:**
   ```solidity
   contract IPFSStorage is ERC721URIStorage {
       string private _baseIPFSURI;
       
       constructor(string memory baseIPFSURI) {
           _baseIPFSURI = baseIPFSURI;
       }
       
       function _baseURI() internal view override returns (string memory) {
           return _baseIPFSURI;
       }
       
       function mint(
           address to,
           uint256 tokenId,
           string memory ipfsHash
       ) public {
           _mint(to, tokenId);
           _setTokenURI(tokenId, ipfsHash);
       }
   }
   ```

2. **Расширенная реализация с проверками:**
   ```solidity
   contract SecureIPFSStorage is ERC721URIStorage {
       using Strings for uint256;
       
       event URIUpdated(uint256 indexed tokenId, string newUri);
       
       mapping(uint256 => bool) private _frozenURIs;
       
       modifier onlyUnfrozenURI(uint256 tokenId) {
           require(!_frozenURIs[tokenId], "URI is frozen");
           _;
       }
       
       function setTokenURI(
           uint256 tokenId,
           string memory newUri
       ) public onlyUnfrozenURI(tokenId) {
           require(
               _isOwnerOrApproved(tokenId),
               "Not owner or approved"
           );
           require(
               _isValidIPFSHash(newUri),
               "Invalid IPFS hash"
           );
           
           _setTokenURI(tokenId, newUri);
           emit URIUpdated(tokenId, newUri);
       }
       
       function freezeURI(uint256 tokenId) public {
           require(
               _isOwnerOrApproved(tokenId),
               "Not owner or approved"
           );
           _frozenURIs[tokenId] = true;
       }
       
       function _isValidIPFSHash(
           string memory uri
       ) internal pure returns (bool) {
           bytes memory b = bytes(uri);
           if (b.length != 46) return false; // Длина IPFS CIDv0
           if (b[0] != 'Q') return false;    // CIDv0 начинается с Q
           
           for (uint i = 1; i < b.length;) {
               bytes1 char = b[i];
               if (!(
                   (char >= '0' && char <= '9') ||
                   (char >= 'a' && char <= 'z') ||
                   (char >= 'A' && char <= 'Z')
               )) return false;
               unchecked { i++; }
           }
           return true;
       }
       
       function _isOwnerOrApproved(
           uint256 tokenId
       ) internal view returns (bool) {
           address owner = ownerOf(tokenId);
           return (
               owner == msg.sender ||
               getApproved(tokenId) == msg.sender ||
               isApprovedForAll(owner, msg.sender)
           );
       }
   }
   ```

### **4. Оптимизации и улучшения**

1. **Кэширование URI:**
   ```solidity
   contract CachedURIStorage is ERC721URIStorage {
       using Strings for uint256;
       
       // Кэш для часто запрашиваемых URI
       mapping(uint256 => string) private _uriCache;
       mapping(uint256 => uint256) private _lastAccessed;
       uint256 private constant CACHE_DURATION = 1 hours;
       
       function tokenURI(
           uint256 tokenId
       ) public view override returns (string memory) {
           if (
               _lastAccessed[tokenId] + CACHE_DURATION > block.timestamp &&
               bytes(_uriCache[tokenId]).length > 0
           ) {
               return _uriCache[tokenId];
           }
           
           string memory uri = super.tokenURI(tokenId);
           _uriCache[tokenId] = uri;
           _lastAccessed[tokenId] = block.timestamp;
           return uri;
       }
   }
   ```

2. **Пакетное обновление URI:**
   ```solidity
   contract BatchURIUpdater is ERC721URIStorage {
       function batchSetTokenURI(
           uint256[] memory tokenIds,
           string[] memory uris
       ) public {
           require(
               tokenIds.length == uris.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < tokenIds.length;) {
               require(
                   _exists(tokenIds[i]),
                   "URI set for nonexistent token"
               );
               _setTokenURI(tokenIds[i], uris[i]);
               unchecked { i++; }
           }
       }
   }
   ```

### **5. Безопасность**

```solidity
contract SecureURIStorage is ERC721URIStorage {
    using Address for address;
    
    event URIFrozen(uint256 indexed tokenId);
    event URIUpdated(uint256 indexed tokenId, string newUri);
    
    mapping(uint256 => bool) private _frozenURIs;
    mapping(uint256 => uint256) private _uriUpdateCount;
    uint256 private constant MAX_UPDATES = 5;
    
    modifier onlyUnfrozenURI(uint256 tokenId) {
        require(!_frozenURIs[tokenId], "URI is frozen");
        _;
    }
    
    function setTokenURI(
        uint256 tokenId,
        string memory newUri
    ) public onlyUnfrozenURI(tokenId) {
        require(
            _isOwnerOrApproved(tokenId),
            "Not owner or approved"
        );
        require(
            _uriUpdateCount[tokenId] < MAX_UPDATES,
            "Max updates reached"
        );
        require(
            _isValidURI(newUri),
            "Invalid URI format"
        );
        
        _setTokenURI(tokenId, newUri);
        _uriUpdateCount[tokenId]++;
        emit URIUpdated(tokenId, newUri);
    }
    
    function freezeURI(uint256 tokenId) public {
        require(
            _isOwnerOrApproved(tokenId),
            "Not owner or approved"
        );
        _frozenURIs[tokenId] = true;
        emit URIFrozen(tokenId);
    }
    
    function _isValidURI(
        string memory uri
    ) internal pure returns (bool) {
        bytes memory b = bytes(uri);
        if (b.length == 0) return false;
        
        // Проверяем, начинается ли с http://, https:// или ipfs://
        if (b.length >= 7 && 
            b[0] == 'h' && b[1] == 't' && b[2] == 't' && b[3] == 'p') {
            if (b[4] == 's') return b[5] == ':' && b[6] == '/' && b[7] == '/';
            return b[4] == ':' && b[5] == '/' && b[6] == '/';
        }
        
        if (b.length >= 7 &&
            b[0] == 'i' && b[1] == 'p' && b[2] == 'f' && b[3] == 's' &&
            b[4] == ':' && b[5] == '/' && b[6] == '/') {
            return true;
        }
        
        return false;
    }
}
```

---

## Связанные темы
- [[Как и где хранить медиа-данные NFT или SFT?]]
- [[Как работает механизм supportsInterface в ERC-165?]]
- [[Как работает механизм обратных вызовов в ERC-721 и ERC-1155?]]

---

## Источники
- [EIP-721: Non-Fungible Token Standard](https://eips.ethereum.org/EIPS/eip-721)
- [OpenZeppelin ERC721URIStorage](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721URIStorage.sol)
- [NFT Metadata Standards](https://docs.opensea.io/docs/metadata-standards) 