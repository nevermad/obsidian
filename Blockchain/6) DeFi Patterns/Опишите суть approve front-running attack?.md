## Короткий ответ

Approve front-running attack происходит, когда злоумышленник отслеживает транзакции на изменение allowance и успевает потратить старый allowance до того, как новое значение будет установлено. Это возможно из-за того, что approve просто перезаписывает значение allowance, а не увеличивает или уменьшает его.

---

## Подробный разбор

### **1. Механизм атаки**

1. **Исходный сценарий:**
   ```solidity
   // Текущее состояние
   allowance[owner][spender] = 100 tokens
   
   // Владелец хочет изменить allowance на 50 токенов
   token.approve(spender, 50);
   ```

2. **Последовательность атаки:**
   ```solidity
   // 1. Владелец отправляет транзакцию на approve(spender, 50)
   
   // 2. Злоумышленник видит транзакцию в mempool и быстро отправляет:
   token.transferFrom(owner, attacker, 100); // Использует старый allowance
   
   // 3. Транзакция владельца выполняется
   allowance[owner][spender] = 50; // Новый allowance установлен
   
   // 4. Злоумышленник может снова использовать новый allowance
   token.transferFrom(owner, attacker, 50); // Использует новый allowance
   ```

### **2. Защитные механизмы**

1. **Проверка текущего allowance:**
   ```solidity
   contract SafeApprove {
       function safeApprove(
           IERC20 token,
           address spender,
           uint256 value
       ) external {
           require(
               token.allowance(msg.sender, spender) == 0 ||
               value == 0,
               "SafeApprove: approve from non-zero to non-zero"
           );
           
           token.approve(spender, value);
       }
   }
   ```

2. **Incremental Approve Pattern:**
   ```solidity
   contract IncrementalApprove {
       function increaseAllowance(
           IERC20 token,
           address spender,
           uint256 addedValue
       ) external returns (bool) {
           uint256 currentAllowance = token.allowance(
               msg.sender,
               spender
           );
           token.approve(spender, currentAllowance + addedValue);
           return true;
       }
       
       function decreaseAllowance(
           IERC20 token,
           address spender,
           uint256 subtractedValue
       ) external returns (bool) {
           uint256 currentAllowance = token.allowance(
               msg.sender,
               spender
           );
           require(
               currentAllowance >= subtractedValue,
               "Decreased below zero"
           );
           token.approve(spender, currentAllowance - subtractedValue);
           return true;
       }
   }
   ```

### **3. Современные решения**

1. **Permit Pattern:**
   ```solidity
   interface IERC20Permit {
       function permit(
           address owner,
           address spender,
           uint256 value,
           uint256 deadline,
           uint8 v,
           bytes32 r,
           bytes32 s
       ) external;
   }
   
   contract PermitExample {
       function depositWithPermit(
           IERC20Permit token,
           uint256 amount,
           uint256 deadline,
           uint8 v,
           bytes32 r,
           bytes32 s
       ) external {
           // Атомарное одобрение и трансфер
           token.permit(
               msg.sender,
               address(this),
               amount,
               deadline,
               v,
               r,
               s
           );
           token.transferFrom(msg.sender, address(this), amount);
       }
   }
   ```

2. **Meta-транзакции:**
   ```solidity
   contract MetaTransactionReceiver {
       struct MetaTransaction {
           address owner;
           address spender;
           uint256 value;
           uint256 nonce;
           uint256 deadline;
       }
       
       mapping(address => uint256) public nonces;
       
       function executeMetaTransaction(
           MetaTransaction calldata metaTx,
           bytes calldata signature
       ) external {
           require(block.timestamp <= metaTx.deadline, "Expired");
           require(nonces[metaTx.owner]++ == metaTx.nonce, "Invalid nonce");
           
           bytes32 hash = keccak256(abi.encode(metaTx));
           address signer = ECDSA.recover(hash, signature);
           require(signer == metaTx.owner, "Invalid signature");
           
           IERC20(token).transferFrom(
               metaTx.owner,
               metaTx.spender,
               metaTx.value
           );
       }
   }
   ```

### **4. Мониторинг и предотвращение**

1. **Мониторинг mempool:**
   ```javascript
   // Web3 код для мониторинга
   web3.eth.subscribe('pendingTransactions')
       .on('data', async (txHash) => {
           const tx = await web3.eth.getTransaction(txHash);
           if (isApproveTransaction(tx)) {
               // Анализ транзакции approve
               const decoded = decodeApproveData(tx.input);
               checkForFrontRunning(decoded);
           }
       });
   ```

2. **Защита на уровне контракта:**
   ```solidity
   contract ProtectedToken is ERC20 {
       mapping(address => uint256) public lastApproveTimestamp;
       uint256 public constant APPROVE_DELAY = 1 minutes;
       
       function approve(
           address spender,
           uint256 amount
       ) public virtual override returns (bool) {
           require(
               block.timestamp >= lastApproveTimestamp[msg.sender] + APPROVE_DELAY,
               "Must wait before next approve"
           );
           lastApproveTimestamp[msg.sender] = block.timestamp;
           return super.approve(spender, amount);
       }
   }
   ```

### **5. Лучшие практики**

1. **Двухшаговый approve:**
   ```solidity
   contract TwoStepApprove {
       mapping(address => mapping(address => uint256)) public pendingApprovals;
       mapping(address => mapping(address => uint256)) public approvalTimestamps;
       
       function initiateApprove(
           address spender,
           uint256 amount
       ) external {
           pendingApprovals[msg.sender][spender] = amount;
           approvalTimestamps[msg.sender][spender] = block.timestamp;
       }
       
       function confirmApprove(address spender) external {
           require(
               block.timestamp >= approvalTimestamps[msg.sender][spender] + 1 minutes,
               "Wait required"
           );
           uint256 amount = pendingApprovals[msg.sender][spender];
           delete pendingApprovals[msg.sender][spender];
           super.approve(spender, amount);
       }
   }
   ```

---

## Связанные темы
- [[Что такое SafeERC?]]
- [[С помощью каких функций израсходовать выданный approve ERC-20?]]
- [[Опишите суть, преимущества и недостатки паттерна unlimited amount approval.]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [EIP-2612: Permit Extension for ERC-20](https://eips.ethereum.org/EIPS/eip-2612)
- [OpenZeppelin Security Advisory](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories) 