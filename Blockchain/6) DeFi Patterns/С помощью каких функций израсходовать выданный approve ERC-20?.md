## Короткий ответ

После получения approve от владельца токенов, можно использовать функцию `transferFrom` для перемещения одобренных токенов. Также существуют специализированные функции в DeFi протоколах, такие как `deposit`, `stake`, `addLiquidity`, которые внутри используют `transferFrom` для перемещения одобренных токенов.

---

## Подробный разбор

### **1. Базовое использование transferFrom**

1. **Стандартный интерфейс:**
   ```solidity
   interface IERC20 {
       function transferFrom(
           address from,
           address to,
           uint256 amount
       ) external returns (bool);
       
       function allowance(
           address owner,
           address spender
       ) external view returns (uint256);
   }
   ```

2. **Пример использования:**
   ```solidity
   contract TokenSpender {
       IERC20 public token;
       
       function spendAllowance(
           address from,
           uint256 amount
       ) external returns (bool) {
           // Проверка доступного allowance
           require(
               token.allowance(from, address(this)) >= amount,
               "Insufficient allowance"
           );
           
           // Использование одобренных токенов
           return token.transferFrom(from, address(this), amount);
       }
   }
   ```

### **2. DeFi протоколы**

1. **Пример DEX:**
   ```solidity
   contract DEXExample {
       using SafeERC20 for IERC20;
       
       function swap(
           IERC20 tokenIn,
           IERC20 tokenOut,
           uint256 amountIn,
           uint256 minAmountOut,
           address recipient
       ) external returns (uint256 amountOut) {
           // Перемещение входящих токенов
           tokenIn.safeTransferFrom(msg.sender, address(this), amountIn);
           
           // Расчет выходящего количества
           amountOut = _calculateAmountOut(amountIn);
           require(amountOut >= minAmountOut, "Insufficient output");
           
           // Отправка выходящих токенов
           tokenOut.safeTransfer(recipient, amountOut);
       }
   }
   ```

2. **Пример Lending Protocol:**
   ```solidity
   contract LendingProtocol {
       using SafeERC20 for IERC20;
       
       struct UserAccount {
           uint256 deposited;
           uint256 borrowed;
           uint256 lastUpdate;
       }
       
       mapping(address => UserAccount) public accounts;
       
       function deposit(
           IERC20 token,
           uint256 amount
       ) external {
           // Перемещение токенов пользователя
           token.safeTransferFrom(msg.sender, address(this), amount);
           
           // Обновление состояния
           accounts[msg.sender].deposited += amount;
           accounts[msg.sender].lastUpdate = block.timestamp;
       }
   }
   ```

### **3. Стейкинг контракты**

1. **Базовый стейкинг:**
   ```solidity
   contract Staking {
       using SafeERC20 for IERC20;
       
       IERC20 public stakingToken;
       mapping(address => uint256) public stakes;
       mapping(address => uint256) public lastUpdateTime;
       
       function stake(uint256 amount) external {
           // Перемещение токенов
           stakingToken.safeTransferFrom(msg.sender, address(this), amount);
           
           // Обновление стейка
           stakes[msg.sender] += amount;
           lastUpdateTime[msg.sender] = block.timestamp;
           
           emit Staked(msg.sender, amount);
       }
   }
   ```

2. **Liquidity Mining:**
   ```solidity
   contract LiquidityMining {
       using SafeERC20 for IERC20;
       
       struct Pool {
           IERC20 lpToken;
           uint256 allocPoint;
           uint256 lastRewardBlock;
           uint256 accRewardPerShare;
       }
       
       function deposit(uint256 pid, uint256 amount) external {
           Pool storage pool = pools[pid];
           UserInfo storage user = userInfo[pid][msg.sender];
           
           // Обновление наград
           updatePool(pid);
           
           // Перемещение LP токенов
           if (amount > 0) {
               pool.lpToken.safeTransferFrom(
                   msg.sender,
                   address(this),
                   amount
               );
               user.amount += amount;
           }
           
           user.rewardDebt = user.amount * pool.accRewardPerShare / 1e12;
           emit Deposit(msg.sender, pid, amount);
       }
   }
   ```

### **4. Специализированные паттерны**

1. **Permit Pattern:**
   ```solidity
   contract PermitSpender {
       function depositWithPermit(
           IERC20Permit token,
           uint256 amount,
           uint256 deadline,
           uint8 v,
           bytes32 r,
           bytes32 s
       ) external {
           // Выполнение permit
           token.permit(
               msg.sender,
               address(this),
               amount,
               deadline,
               v,
               r,
               s
           );
           
           // Использование одобренных токенов
           token.transferFrom(msg.sender, address(this), amount);
       }
   }
   ```

2. **Batch Operations:**
   ```solidity
   contract BatchProcessor {
       using SafeERC20 for IERC20;
       
       function batchTransferFrom(
           IERC20[] calldata tokens,
           address[] calldata froms,
           uint256[] calldata amounts
       ) external {
           require(
               tokens.length == froms.length &&
               froms.length == amounts.length,
               "Length mismatch"
           );
           
           for (uint256 i = 0; i < tokens.length; i++) {
               tokens[i].safeTransferFrom(
                   froms[i],
                   address(this),
                   amounts[i]
               );
           }
       }
   }
   ```

### **5. Безопасное использование**

1. **Проверки безопасности:**
   ```solidity
   contract SafeSpender {
       using SafeERC20 for IERC20;
       
       function safeSpend(
           IERC20 token,
           address from,
           uint256 amount
       ) external {
           // Проверка баланса
           require(
               token.balanceOf(from) >= amount,
               "Insufficient balance"
           );
           
           // Проверка allowance
           require(
               token.allowance(from, address(this)) >= amount,
               "Insufficient allowance"
           );
           
           // Безопасное перемещение
           token.safeTransferFrom(from, address(this), amount);
       }
   }
   ```

---

## Связанные темы
- [[Что такое SafeERC?]]
- [[Опишите суть approve front-running attack?]]
- [[Опишите суть, преимущества и недостатки паттерна unlimited amount approval.]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin ERC20 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol)
- [Uniswap V2 Core](https://github.com/Uniswap/v2-core) 