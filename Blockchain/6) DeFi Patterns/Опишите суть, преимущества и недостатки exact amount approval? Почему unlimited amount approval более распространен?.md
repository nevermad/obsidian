## Короткий ответ

Exact amount approval - это паттерн, при котором одобряется точное количество токенов, необходимое для конкретной операции. Это более безопасно, чем unlimited approval, но требует дополнительных транзакций и газа для каждой операции. Unlimited amount approval более распространен из-за лучшего UX и экономии газа, несмотря на повышенные риски безопасности.

---

## Подробный разбор

### **1. Механизм работы**

1. **Базовая реализация:**
   ```solidity
   contract ExactApproval {
       IERC20 public token;
       
       function exactApprove(
           address spender,
           uint256 exactAmount
       ) external {
           // Одобрение точного количества
           require(
               token.approve(spender, exactAmount),
               "Approve failed"
           );
       }
       
       function spendExact(
           address from,
           uint256 amount
       ) external {
           // Проверка точного allowance
           require(
               token.allowance(from, address(this)) == amount,
               "Incorrect allowance"
           );
           
           // Использование токенов
           token.transferFrom(from, address(this), amount);
       }
   }
   ```

2. **Сравнение с unlimited approval:**
   ```solidity
   contract ApprovalComparison {
       // Exact amount подход
       function exactApproachFlow(uint256 amount) external {
           // 1. Approve exact amount
           token.approve(spender, amount);        // Gas: ~45,000
           // 2. Transfer
           token.transferFrom(msg.sender, to, amount); // Gas: ~35,000
           // Общий газ на операцию: ~80,000
       }
       
       // Unlimited подход
       function unlimitedApproachFlow(uint256 amount) external {
           // 1. Approve unlimited (делается один раз)
           token.approve(spender, type(uint256).max); // Gas: ~45,000
           // 2. Transfer (все последующие операции)
           token.transferFrom(msg.sender, to, amount); // Gas: ~35,000
           // Газ на первую операцию: ~80,000
           // Газ на последующие операции: ~35,000
       }
   }
   ```

### **2. Преимущества**

1. **Безопасность:**
   ```solidity
   contract SecureExactApproval {
       using SafeERC20 for IERC20;
       
       function safeExactApprove(
           IERC20 token,
           address spender,
           uint256 amount
       ) external {
           // Сначала сбрасываем allowance
           token.safeApprove(spender, 0);
           
           // Затем устанавливаем точное значение
           token.safeApprove(spender, amount);
           
           // Проверяем установленное значение
           require(
               token.allowance(msg.sender, spender) == amount,
               "Approval mismatch"
           );
       }
   }
   ```

2. **Аудит и мониторинг:**
   ```solidity
   contract ExactApprovalAuditor {
       event ExactApproval(
           address indexed token,
           address indexed owner,
           address indexed spender,
           uint256 amount,
           uint256 timestamp
       );
       
       function auditExactApproval(
           IERC20 token,
           address owner,
           address spender
       ) external view returns (bool) {
           uint256 allowance = token.allowance(owner, spender);
           // Проверка на точное соответствие ожидаемой сумме
           return allowance == expectedAmount;
       }
   }
   ```

### **3. Недостатки**

1. **Газовые затраты:**
   ```solidity
   contract GasAnalysis {
       struct Operation {
           uint256 approveGas;
           uint256 transferGas;
           uint256 totalGas;
       }
       
       function compareGasCosts(
           uint256 operationsCount
       ) external pure returns (
           Operation memory exactApproval,
           Operation memory unlimitedApproval
       ) {
           // Exact approval
           exactApproval.approveGas = 45000 * operationsCount;
           exactApproval.transferGas = 35000 * operationsCount;
           exactApproval.totalGas = exactApproval.approveGas + 
               exactApproval.transferGas;
           
           // Unlimited approval
           unlimitedApproval.approveGas = 45000; // Только один раз
           unlimitedApproval.transferGas = 35000 * operationsCount;
           unlimitedApproval.totalGas = unlimitedApproval.approveGas + 
               unlimitedApproval.transferGas;
       }
   }
   ```

2. **UX проблемы:**
   ```solidity
   contract UXComparison {
       // Exact amount - требует двух транзакций каждый раз
       function exactAmountFlow() external {
           // 1. Пользователь должен подписать approve
           // 2. Ждать подтверждения
           // 3. Подписать основную транзакцию
           // 4. Снова ждать подтверждения
       }
       
       // Unlimited - требует одну транзакцию после первого approve
       function unlimitedFlow() external {
           // 1. Проверить наличие unlimited approval
           // 2. Если есть - сразу выполнить операцию
           // 3. Если нет - запросить unlimited approval один раз
       }
   }
   ```

### **4. Почему unlimited более распространен**

1. **Экономические факторы:**
   ```solidity
   contract EconomicAnalysis {
       struct CostAnalysis {
           uint256 gasPrice;
           uint256 operationsPerMonth;
           uint256 exactApprovalCost;
           uint256 unlimitedApprovalCost;
       }
       
       function analyzeCosts(
           uint256 gasPrice,
           uint256 operationsCount
       ) external pure returns (CostAnalysis memory) {
           // Exact approval
           uint256 exactCost = (45000 + 35000) * 
               operationsCount * gasPrice;
           
           // Unlimited approval
           uint256 unlimitedCost = 45000 * gasPrice + 
               (35000 * operationsCount * gasPrice);
           
           return CostAnalysis({
               gasPrice: gasPrice,
               operationsPerMonth: operationsCount,
               exactApprovalCost: exactCost,
               unlimitedApprovalCost: unlimitedCost
           });
       }
   }
   ```

2. **UX оптимизации:**
   ```solidity
   contract ModernDEX {
       mapping(address => bool) public hasUnlimitedApproval;
       
       function optimizedSwap(
           IERC20 tokenIn,
           IERC20 tokenOut,
           uint256 amountIn
       ) external {
           if (!hasUnlimitedApproval[msg.sender]) {
               // Запрос unlimited approval только один раз
               tokenIn.approve(address(this), type(uint256).max);
               hasUnlimitedApproval[msg.sender] = true;
           }
           
           // Выполнение свопа без дополнительных approve
           _executeSwap(tokenIn, tokenOut, amountIn);
       }
   }
   ```

### **5. Гибридные подходы**

1. **Умный approval:**
   ```solidity
   contract SmartApproval {
       uint256 public constant THRESHOLD = 1000 * 10**18; // 1000 токенов
       
       function smartApprove(
           IERC20 token,
           address spender,
           uint256 amount
       ) external {
           if (amount > THRESHOLD) {
               // Для больших сумм используем exact approval
               token.approve(spender, amount);
           } else {
               // Для малых сумм используем unlimited
               token.approve(spender, type(uint256).max);
           }
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Опишите суть, преимущества и недостатки паттерна unlimited amount approval.]]
- [[Что такое SafeERC?]]
- [[Опишите суть approve front-running attack?]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol)
- [DeFi Security Best Practices](https://consensys.github.io/smart-contract-best-practices/development-recommendations/token-specific/token-approval/) 