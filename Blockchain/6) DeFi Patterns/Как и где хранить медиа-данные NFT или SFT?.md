## Короткий ответ

Медиа-данные NFT или SFT можно хранить несколькими способами: в IPFS (децентрализованное хранение), в централизованных хранилищах (AWS S3, Google Cloud Storage), в Arweave (постоянное хранение), или прямо в смарт-контракте (для очень маленьких данных). Каждый метод имеет свои преимущества и недостатки в отношении стоимости, децентрализации и долговечности.

---

## Подробный разбор

### **1. IPFS хранение**

1. **Базовая структура:**
   ```solidity
   contract IPFSStorage is ERC721 {
       string private _baseIPFSURI;
       
       constructor(string memory baseURI) {
           _baseIPFSURI = baseURI; // например "ipfs://"
       }
       
       function _baseURI() internal view override returns (string memory) {
           return _baseIPFSURI;
       }
       
       function setBaseURI(string memory newBaseURI) public onlyOwner {
           _baseIPFSURI = newBaseURI;
       }
       
       function tokenURI(uint256 tokenId) 
           public 
           view 
           override 
           returns (string memory) 
       {
           require(_exists(tokenId), "Token does not exist");
           return string(
               abi.encodePacked(
                   _baseIPFSURI,
                   _tokenURIs[tokenId]
               )
           );
       }
   }
   ```

2. **Пример метаданных в IPFS:**
   ```json
   {
       "name": "Asset Name",
       "description": "Asset Description",
       "image": "ipfs://QmXxxx...", // IPFS хеш изображения
       "animation_url": "ipfs://QmYyyy...", // Для анимаций/видео
       "attributes": [
           {
               "trait_type": "Background",
               "value": "Blue"
           }
       ]
   }
   ```

### **2. Централизованное хранение**

1. **AWS S3 интеграция:**
   ```solidity
   contract S3Storage is ERC721 {
       string private _baseS3URI;
       mapping(uint256 => string) private _s3Keys;
       
       constructor(string memory baseURI) {
           _baseS3URI = baseURI; // например "https://bucket.s3.amazonaws.com/"
       }
       
       function setTokenS3Key(
           uint256 tokenId,
           string memory s3Key
       ) public onlyOwner {
           require(_exists(tokenId), "Token does not exist");
           _s3Keys[tokenId] = s3Key;
       }
       
       function tokenURI(uint256 tokenId) 
           public 
           view 
           override 
           returns (string memory) 
       {
           require(_exists(tokenId), "Token does not exist");
           return string(
               abi.encodePacked(
                   _baseS3URI,
                   _s3Keys[tokenId]
               )
           );
       }
   }
   ```

### **3. Arweave хранение**

1. **Базовая интеграция:**
   ```solidity
   contract ArweaveStorage is ERC721 {
       string private constant ARWEAVE_PREFIX = "https://arweave.net/";
       mapping(uint256 => string) private _arweaveHashes;
       
       function setTokenArweaveHash(
           uint256 tokenId,
           string memory arweaveHash
       ) public onlyOwner {
           require(_exists(tokenId), "Token does not exist");
           require(
               _isValidArweaveHash(arweaveHash),
               "Invalid Arweave hash"
           );
           _arweaveHashes[tokenId] = arweaveHash;
       }
       
       function tokenURI(uint256 tokenId) 
           public 
           view 
           override 
           returns (string memory) 
       {
           require(_exists(tokenId), "Token does not exist");
           return string(
               abi.encodePacked(
                   ARWEAVE_PREFIX,
                   _arweaveHashes[tokenId]
               )
           );
       }
       
       function _isValidArweaveHash(
           string memory hash
       ) internal pure returns (bool) {
           bytes memory b = bytes(hash);
           if (b.length != 43) return false;
           
           for (uint i = 0; i < b.length;) {
               bytes1 char = b[i];
               if (!(
                   (char >= '0' && char <= '9') ||
                   (char >= 'a' && char <= 'z') ||
                   (char >= 'A' && char <= 'Z') ||
                   char == '-' ||
                   char == '_'
               )) return false;
               unchecked { i++; }
           }
           return true;
       }
   }
   ```

### **4. Хранение в смарт-контракте**

1. **Для маленьких данных:**
   ```solidity
   contract OnChainStorage is ERC721 {
       struct TokenData {
           string name;
           string description;
           bytes svgImage; // SVG данные
           string[] attributes;
       }
       
       mapping(uint256 => TokenData) private _tokenData;
       
       function mintWithData(
           address to,
           uint256 tokenId,
           string memory name,
           string memory description,
           bytes memory svgImage,
           string[] memory attributes
       ) public {
           _mint(to, tokenId);
           _tokenData[tokenId] = TokenData(
               name,
               description,
               svgImage,
               attributes
           );
       }
       
       function tokenURI(uint256 tokenId) 
           public 
           view 
           override 
           returns (string memory) 
       {
           require(_exists(tokenId), "Token does not exist");
           
           TokenData memory data = _tokenData[tokenId];
           string memory json = Base64.encode(
               bytes(
                   string(
                       abi.encodePacked(
                           '{"name":"', data.name, '",',
                           '"description":"', data.description, '",',
                           '"image":"data:image/svg+xml;base64,',
                           Base64.encode(data.svgImage), '",',
                           '"attributes":', _generateAttributes(data.attributes),
                           '}'
                       )
                   )
               )
           );
           
           return string(
               abi.encodePacked(
                   "data:application/json;base64,",
                   json
               )
           );
       }
   }
   ```

### **5. Гибридное хранение**

```solidity
contract HybridStorage is ERC721 {
    enum StorageType { IPFS, Arweave, S3, OnChain }
    
    struct StorageData {
        StorageType storageType;
        string location; // URI или onchain данные
    }
    
    mapping(uint256 => StorageData) private _storage;
    
    string private _baseIPFSURI;
    string private _baseS3URI;
    
    event StorageUpdated(
        uint256 indexed tokenId,
        StorageType storageType,
        string location
    );
    
    function setTokenStorage(
        uint256 tokenId,
        StorageType storageType,
        string memory location
    ) public onlyOwner {
        require(_exists(tokenId), "Token does not exist");
        
        if (storageType == StorageType.IPFS) {
            require(
                _isValidIPFSHash(location),
                "Invalid IPFS hash"
            );
        } else if (storageType == StorageType.Arweave) {
            require(
                _isValidArweaveHash(location),
                "Invalid Arweave hash"
            );
        }
        
        _storage[tokenId] = StorageData(storageType, location);
        emit StorageUpdated(tokenId, storageType, location);
    }
    
    function tokenURI(uint256 tokenId) 
        public 
        view 
        override 
        returns (string memory) 
    {
        require(_exists(tokenId), "Token does not exist");
        
        StorageData memory data = _storage[tokenId];
        
        if (data.storageType == StorageType.IPFS) {
            return string(
                abi.encodePacked(_baseIPFSURI, data.location)
            );
        } else if (data.storageType == StorageType.Arweave) {
            return string(
                abi.encodePacked("https://arweave.net/", data.location)
            );
        } else if (data.storageType == StorageType.S3) {
            return string(
                abi.encodePacked(_baseS3URI, data.location)
            );
        } else {
            // OnChain данные уже содержат полный URI
            return data.location;
        }
    }
}
```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Как работает механизм tokenURI в ERC-721?]]
- [[Как работает механизм supportsInterface в ERC-165?]]
- [[Как работает механизм обратных вызовов в ERC-721 и ERC-1155?]]

---

## Источники
- [IPFS Documentation](https://docs.ipfs.io/)
- [Arweave Documentation](https://docs.arweave.org/)
- [OpenSea Metadata Standards](https://docs.opensea.io/docs/metadata-standards)
- [NFT Storage](https://nft.storage/) 