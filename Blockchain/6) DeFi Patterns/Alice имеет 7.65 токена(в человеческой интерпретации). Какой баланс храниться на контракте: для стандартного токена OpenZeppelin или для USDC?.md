## Короткий ответ

Для стандартного токена OpenZeppelin (18 decimals) баланс будет храниться как 7650000000000000000 (7.65 * 10^18). Для USDC (6 decimals) баланс будет храниться как 7650000 (7.65 * 10^6). Разница в количестве десятичных знаков связана с разными подходами к точности представления чисел.

---

## Подробный разбор

### **1. Стандартный токен OpenZeppelin**

1. **Базовая реализация:**
   ```solidity
   contract StandardToken is ERC20 {
       // 18 decimals по умолчанию
       constructor() ERC20("Standard Token", "STD") {}
       
       // Пример баланса
       function example() external pure returns (uint256) {
           uint256 humanReadable = 7.65;
           // В контракте хранится:
           return 7650000000000000000; // 7.65 * 10^18
       }
   }
   ```

2. **Конвертация значений:**
   ```solidity
   contract TokenMath {
       uint8 public constant DECIMALS = 18;
       
       function toTokenAmount(uint256 humanReadable) public pure returns (uint256) {
           return humanReadable * 10**DECIMALS;
           // 7.65 * 10^18 = 7650000000000000000
       }
       
       function toHumanReadable(uint256 tokenAmount) public pure returns (string memory) {
           // 7650000000000000000 / 10^18 = 7.65
           uint256 integer = tokenAmount / 10**DECIMALS;
           uint256 fraction = tokenAmount % 10**DECIMALS;
           return string(abi.encodePacked(
               integer.toString(),
               ".",
               fraction.toString()
           ));
       }
   }
   ```

### **2. USDC (6 decimals)**

1. **Специфика реализации:**
   ```solidity
   contract USDC is ERC20 {
       // 6 decimals для USDC
       constructor() ERC20("USD Coin", "USDC") {
           _setupDecimals(6);
       }
       
       // Пример баланса
       function example() external pure returns (uint256) {
           uint256 humanReadable = 7.65;
           // В контракте хранится:
           return 7650000; // 7.65 * 10^6
       }
   }
   ```

2. **Работа с USDC:**
   ```solidity
   contract USDCHandler {
       uint8 public constant USDC_DECIMALS = 6;
       
       function toUSDCAmount(uint256 humanReadable) public pure returns (uint256) {
           return humanReadable * 10**USDC_DECIMALS;
           // 7.65 * 10^6 = 7650000
       }
       
       function fromUSDCAmount(uint256 usdcAmount) public pure returns (string memory) {
           // 7650000 / 10^6 = 7.65
           uint256 integer = usdcAmount / 10**USDC_DECIMALS;
           uint256 fraction = usdcAmount % 10**USDC_DECIMALS;
           return string(abi.encodePacked(
               integer.toString(),
               ".",
               fraction.toString()
           ));
       }
   }
   ```

### **3. Сравнение и конвертация**

1. **Между разными decimals:**
   ```solidity
   contract TokenConverter {
       function convertDecimals(
           uint256 amount,
           uint8 fromDecimals,
           uint8 toDecimals
       ) public pure returns (uint256) {
           if (fromDecimals == toDecimals) {
               return amount;
           }
           
           if (fromDecimals > toDecimals) {
               return amount / 10**(fromDecimals - toDecimals);
           } else {
               return amount * 10**(toDecimals - fromDecimals);
           }
       }
       
       function example() external pure returns (uint256, uint256) {
           uint256 standardAmount = 7650000000000000000; // 7.65 в 18 decimals
           uint256 usdcAmount = 7650000;                 // 7.65 в 6 decimals
           
           // Конвертация из 18 в 6 decimals
           uint256 toUSDC = convertDecimals(standardAmount, 18, 6);
           // Конвертация из 6 в 18 decimals
           uint256 toStandard = convertDecimals(usdcAmount, 6, 18);
           
           return (toUSDC, toStandard);
       }
   }
   ```

### **4. Работа с дробными числами**

1. **Безопасная математика:**
   ```solidity
   contract SafeTokenMath {
       using SafeMath for uint256;
       
       function multiplyWithDecimals(
           uint256 amount,
           uint256 multiplier,
           uint8 decimals
       ) public pure returns (uint256) {
           // Например, 7.65 * 2.5
           uint256 rawResult = amount.mul(multiplier);
           return rawResult.div(10**decimals);
       }
       
       function divideWithDecimals(
           uint256 amount,
           uint256 divisor,
           uint8 decimals
       ) public pure returns (uint256) {
           // Например, 7.65 / 2
           uint256 scaledAmount = amount.mul(10**decimals);
           return scaledAmount.div(divisor);
       }
   }
   ```

2. **Округление:**
   ```solidity
   contract TokenRounding {
       function roundUp(
           uint256 amount,
           uint8 decimals
       ) public pure returns (uint256) {
           uint256 precision = 10**decimals;
           return (amount + precision - 1) / precision * precision;
       }
       
       function roundDown(
           uint256 amount,
           uint8 decimals
       ) public pure returns (uint256) {
           uint256 precision = 10**decimals;
           return amount / precision * precision;
       }
   }
   ```

### **5. Практические примеры**

1. **DEX расчеты:**
   ```solidity
   contract DEXExample {
       function calculateSwap(
           uint256 amountIn,
           uint8 decimalsIn,
           uint8 decimalsOut,
           uint256 price
       ) external pure returns (uint256) {
           // Нормализация к 18 decimals для расчетов
           uint256 normalizedAmount = convertDecimals(amountIn, decimalsIn, 18);
           
           // Расчет
           uint256 result = normalizedAmount.mul(price).div(10**18);
           
           // Конвертация к нужным decimals
           return convertDecimals(result, 18, decimalsOut);
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое unchecked блоки?]]
- [[Опишите основные функции, события и особенности поведения ERC-20 токенов?]]
- [[Fixed point math in Solidity]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [USDC Implementation](https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48#code)
- [OpenZeppelin ERC20 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol) 