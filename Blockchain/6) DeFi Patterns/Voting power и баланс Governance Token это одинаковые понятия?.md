[[6. Список вопросов]]

## Короткий ответ

Voting power и баланс Governance Token - это разные понятия. Баланс токенов - это количество токенов на адресе, в то время как voting power может включать делегированные токены, учитывать время блокировки, использовать различные формулы расчета (например, квадратичное голосование) и другие модификаторы. Voting power может быть как больше, так и меньше баланса токенов в зависимости от механизма управления.

---

## Подробный разбор

### **1. Базовые различия**

```solidity
contract VotingPowerExample {
    mapping(address => uint256) private _balances;
    mapping(address => address) private _delegates;
    mapping(address => uint256) private _delegatedPower;
    mapping(address => uint256) private _lockTime;
    
    // Баланс токенов
    function balanceOf(
        address account
    ) public view returns (uint256) {
        return _balances[account];
    }
    
    // Voting power с учетом делегирования
    function getVotes(
        address account
    ) public view returns (uint256) {
        return _balances[account] + _delegatedPower[account];
    }
    
    // Voting power с учетом времени блокировки
    function getTimeWeightedVotes(
        address account
    ) public view returns (uint256) {
        uint256 baseVotes = getVotes(account);
        uint256 lockDuration = _lockTime[account] > block.timestamp ?
            _lockTime[account] - block.timestamp : 0;
        
        // Бонус за длительность блокировки
        uint256 bonus = (baseVotes * lockDuration) / 365 days;
        return baseVotes + bonus;
    }
}
```

### **2. Механизмы модификации Voting Power**

1. **Квадратичное голосование:**
   ```solidity
   contract QuadraticVotingPower {
       function getQuadraticVotingPower(
           uint256 balance
       ) public pure returns (uint256) {
           // Voting power = √balance
           return sqrt(balance);
       }
       
       function sqrt(uint256 x) internal pure returns (uint256 y) {
           uint256 z = (x + 1) / 2;
           y = x;
           while (z < y) {
               y = z;
               z = (x / z + z) / 2;
           }
       }
   }
   ```

2. **Временное взвешивание:**
   ```solidity
   contract TimeWeightedVotingPower {
       struct Lock {
           uint256 amount;
           uint256 endTime;
       }
       
       mapping(address => Lock) public locks;
       
       function lockTokens(uint256 amount, uint256 duration) external {
           require(duration <= 4 years, "Max 4 years");
           require(amount > 0, "Amount > 0");
           
           // Перевод токенов
           token.transferFrom(msg.sender, address(this), amount);
           
           // Сохранение информации о блокировке
           locks[msg.sender] = Lock(
               amount,
               block.timestamp + duration
           );
       }
       
       function getVotingPower(address account) public view returns (uint256) {
           Lock memory lock = locks[account];
           if (block.timestamp >= lock.endTime) return 0;
           
           uint256 remainingTime = lock.endTime - block.timestamp;
           uint256 maxBonus = lock.amount; // 100% бонус максимум
           
           return lock.amount + (maxBonus * remainingTime) / (4 years);
       }
   }
   ```

### **3. Делегирование**

```solidity
contract DelegatedVotingPower {
    struct Delegation {
        address delegate;
        uint256 amount;
        uint256 startTime;
    }
    
    mapping(address => Delegation) public delegations;
    mapping(address => uint256) public receivedDelegations;
    
    event PowerDelegated(
        address indexed from,
        address indexed to,
        uint256 amount
    );
    
    function delegate(address to, uint256 amount) external {
        require(to != msg.sender, "Self delegation");
        require(amount <= token.balanceOf(msg.sender), "Insufficient balance");
        
        // Отзыв предыдущего делегирования
        Delegation storage oldDelegation = delegations[msg.sender];
        if (oldDelegation.delegate != address(0)) {
            receivedDelegations[oldDelegation.delegate] -= oldDelegation.amount;
        }
        
        // Новое делегирование
        delegations[msg.sender] = Delegation(
            to,
            amount,
            block.timestamp
        );
        receivedDelegations[to] += amount;
        
        emit PowerDelegated(msg.sender, to, amount);
    }
    
    function getVotingPower(address account) public view returns (uint256) {
        uint256 ownBalance = token.balanceOf(account);
        uint256 delegatedBalance = receivedDelegations[account];
        uint256 delegatedAway = delegations[account].amount;
        
        return ownBalance - delegatedAway + delegatedBalance;
    }
}
```

### **4. Комплексные системы**

1. **Многофакторный расчет:**
   ```solidity
   contract ComplexVotingPower {
       struct VotingPowerFactors {
           uint256 baseBalance;
           uint256 delegatedPower;
           uint256 lockBonus;
           uint256 stakingBonus;
           uint256 reputationBonus;
       }
       
       function calculateVotingPower(
           address account
       ) public view returns (uint256) {
           VotingPowerFactors memory factors;
           
           // Базовый баланс
           factors.baseBalance = token.balanceOf(account);
           
           // Делегированная мощность
           factors.delegatedPower = getDelegatedPower(account);
           
           // Бонус за время блокировки
           factors.lockBonus = getLockBonus(account);
           
           // Бонус за стейкинг
           factors.stakingBonus = getStakingBonus(account);
           
           // Бонус за репутацию
           factors.reputationBonus = getReputationBonus(account);
           
           return factors.baseBalance +
                  factors.delegatedPower +
                  factors.lockBonus +
                  factors.stakingBonus +
                  factors.reputationBonus;
       }
   }
   ```

2. **Система с ограничениями:**
   ```solidity
   contract CappedVotingPower {
       uint256 public constant MAX_VOTING_POWER = 1000e18;
       uint256 public constant MIN_VOTING_POWER = 1e18;
       
       function getAdjustedVotingPower(
           address account
       ) public view returns (uint256) {
           uint256 rawPower = calculateVotingPower(account);
           
           // Минимальное ограничение
           if (rawPower < MIN_VOTING_POWER) {
               return MIN_VOTING_POWER;
           }
           
           // Максимальное ограничение
           if (rawPower > MAX_VOTING_POWER) {
               return MAX_VOTING_POWER;
           }
           
           return rawPower;
       }
   }
   ```

### **5. Примеры использования**

1. **Протокол DeFi:**
   ```solidity
   contract DeFiGovernance {
       function proposeUpdate(
           bytes memory data
       ) external {
           uint256 balance = token.balanceOf(msg.sender);
           uint256 votingPower = getVotingPower(msg.sender);
           
           // Требуется больше voting power, чем просто баланс
           require(
               votingPower >= PROPOSAL_THRESHOLD &&
               votingPower >= balance * 2,
               "Insufficient voting power"
           );
           
           // Создание предложения
       }
   }
   ```

2. **DAO с репутацией:**
   ```solidity
   contract ReputationDAO {
       mapping(address => uint256) public reputation;
       
       function getEffectiveVotingPower(
           address account
       ) public view returns (uint256) {
           uint256 balance = token.balanceOf(account);
           uint256 rep = reputation[account];
           
           // Voting power увеличивается с репутацией
           return balance * (100 + rep) / 100;
       }
   }
   ```

---

## Связанные темы
- [[Что такое и для чего необходим Governance Token?]]
- [[При голосовании Governance Token блокируется?]]
- [[Что такое DAO?]]

---

## Источники
- [Compound Governance](https://compound.finance/docs/governance)
- [Curve DAO](https://curve.readthedocs.io/dao-voting.html)
- [Aave Governance](https://docs.aave.com/developers/protocol-governance) 