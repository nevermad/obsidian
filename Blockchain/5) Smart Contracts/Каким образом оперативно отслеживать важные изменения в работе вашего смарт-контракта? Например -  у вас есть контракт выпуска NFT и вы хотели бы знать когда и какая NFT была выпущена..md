
## Короткий ответ

Для оперативного отслеживания важных изменений в работе смарт-контракта, таких как выпуск NFT, можно использовать события (`events`) с индексированными параметрами. Внешние приложения могут подписаться на эти события через ABI контракта и получать уведомления в реальном времени.

---

## Подробный разбор

### **Как отслеживать выпуск NFT?**
1. **Использование событий:**
   - События позволяют записывать важные данные в блокчейн для последующего анализа.
   - Внешние приложения могут подписаться на события и реагировать на них в реальном времени.

2. **Пример для выпуска NFT:**
   ```solidity
   contract NFT {
       event Minted(address indexed owner, uint indexed tokenId, string tokenURI);

       mapping(uint => address) public owners;
       mapping(uint => string) public tokenURIs;
       uint public nextTokenId;

       function mint(string memory uri) public {
           uint tokenId = nextTokenId;
           owners[tokenId] = msg.sender;
           tokenURIs[tokenId] = uri;
           nextTokenId++;
           emit Minted(msg.sender, tokenId, uri); // Запись события о выпуске NFT
       }
   }
   ```

   - В этом примере:
     - Событие `Minted` записывает владельца, ID токена и его URI.
     - Внешнее приложение может отслеживать это событие и получать информацию о новых NFT.

---

### **Как отслеживать события извне?**
1. **Web3.js:**
   - Используйте библиотеку Web3.js для подписки на события контракта.
   - Пример:
     ```javascript
     const Web3 = require('web3');
     const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID');

     const abi = [/* ABI контракта */];
     const contractAddress = '0xYourContractAddress';
     const contract = new web3.eth.Contract(abi, contractAddress);

     contract.events.Minted({
         fromBlock: 0,
         toBlock: 'latest'
     }, (error, event) => {
         if (!error) {
             console.log("New NFT minted:", event.returnValues);
         }
     });
     ```

   - В этом примере:
     - Приложение подписывается на событие `Minted`.
     - При каждом выпуске NFT выводится информация о владельце, ID токена и его URI.

2. **Ethers.js:**
   - Аналогично можно использовать библиотеку Ethers.js:
     ```javascript
     const { ethers } = require('ethers');
     const provider = new ethers.providers.InfuraProvider('mainnet', 'YOUR_PROJECT_ID');
     const abi = [/* ABI контракта */];
     const contractAddress = '0xYourContractAddress';
     const contract = new ethers.Contract(contractAddress, abi, provider);

     contract.on('Minted', (owner, tokenId, tokenURI) => {
         console.log("New NFT minted:", { owner, tokenId, tokenURI });
     });
     ```

---

### **Особенности отслеживания событий**
1. **Indexed параметры:**
   - Индексированные параметры позволяют фильтровать события.
   - Например, можно отслеживать только те события, где определенный адрес является владельцем:
     ```javascript
     contract.events.Minted({
         filter: { owner: '0xYourAddress' },
         fromBlock: 0,
         toBlock: 'latest'
     }, (error, event) => {
         if (!error) {
             console.log("NFT minted for specific owner:", event.returnValues);
         }
     });
     ```

2. **Non-indexed параметры:**
   - Неиндексированные параметры содержат больше информации, но не поддерживают фильтрацию.
   - Они полезны для хранения дополнительных данных, таких как URI токена.

---

### **Пример комбинированного использования**
```solidity
contract NFT {
    event Minted(address indexed owner, uint indexed tokenId, string tokenURI);

    mapping(uint => address) public owners;
    mapping(uint => string) public tokenURIs;
    uint public nextTokenId;

    function mint(string memory uri) public {
        uint tokenId = nextTokenId;
        owners[tokenId] = msg.sender;
        tokenURIs[tokenId] = uri;
        nextTokenId++;
        emit Minted(msg.sender, tokenId, uri); // Запись события о выпуске NFT
    }
}
```

- В этом примере:
  - Событие `Minted` записывает владельца, ID токена и его URI.
  - Внешнее приложение может отслеживать это событие и получать полную информацию о новом NFT.

---

### **Как это работает на уровне EVM?**
1. **Log Entries:**
   - На уровне EVM события хранятся в виде логов.
   - Логи содержат:
     - Адрес контракта.
     - Темы (indexed параметры).
     - Данные (non-indexed параметры).

2. **Gas Costs:**
   - Запись событий дешевле, чем запись в `storage`.
   - Индексированные параметры увеличивают затраты газа.

---

### **Пример отслеживания событий через Web3.js**
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://mainnet.infura.io/v3/YOUR_PROJECT_ID');

const abi = [/* ABI контракта */];
const contractAddress = '0xYourContractAddress';
const contract = new web3.eth.Contract(abi, contractAddress);

contract.events.Minted({
    fromBlock: 0,
    toBlock: 'latest'
}, (error, event) => {
    if (!error) {
        const owner = event.returnValues.owner;
        const tokenId = event.returnValues.tokenId;
        const tokenURI = event.returnValues.tokenURI;
        console.log(`New NFT minted: Owner=${owner}, TokenID=${tokenId}, URI=${tokenURI}`);
    }
});
```

- В этом примере:
  - Приложение подписывается на событие `Minted`.
  - При каждом выпуске NFT выводится информация о владельце, ID токена и его URI.

---

## Связанные темы
- [Вернуться к списку вопросов](5.%20Список%20вопросов.md)
- [[Что такое selector функции? Когда он генерируется, а когда отсутствует? Для чего используется?]]
- [[Каким образом представлено логирование? Особенности и ограничения.]]

---

## Источники
- [Solidity Documentation - Events](https://docs.soliditylang.org/en/latest/contracts.html#events)
- [Web3.js Documentation](https://web3js.readthedocs.io/)
- [Ethers.js Documentation](https://docs.ethers.org/)
---