[[6. Список вопросов]]

## Короткий ответ

Governance Token может как блокироваться, так и не блокироваться при голосовании - это зависит от дизайна протокола. Блокировка предотвращает двойное голосование и манипуляции, но снижает ликвидность. Не блокирующий механизм обычно использует снапшоты балансов на момент создания предложения или другие механизмы учета голосов без блокировки токенов.

---

## Подробный разбор

### **1. Блокирующий механизм**

```solidity
contract LockingGovernance {
    struct Vote {
        uint256 proposalId;
        uint256 amount;
        bool support;
        uint256 unlockTime;
    }
    
    mapping(address => Vote[]) public votes;
    mapping(address => uint256) public lockedAmount;
    
    uint256 public constant LOCK_DURATION = 3 days;
    
    event TokensLocked(
        address indexed voter,
        uint256 amount,
        uint256 unlockTime
    );
    
    event TokensUnlocked(
        address indexed voter,
        uint256 amount
    );
    
    function castVote(
        uint256 proposalId,
        uint256 amount,
        bool support
    ) external {
        require(amount > 0, "Amount must be > 0");
        require(
            token.balanceOf(msg.sender) >= amount + lockedAmount[msg.sender],
            "Insufficient balance"
        );
        
        // Блокировка токенов
        token.transferFrom(msg.sender, address(this), amount);
        lockedAmount[msg.sender] += amount;
        
        uint256 unlockTime = block.timestamp + LOCK_DURATION;
        votes[msg.sender].push(Vote({
            proposalId: proposalId,
            amount: amount,
            support: support,
            unlockTime: unlockTime
        }));
        
        emit TokensLocked(msg.sender, amount, unlockTime);
    }
    
    function unlock(uint256 voteIndex) external {
        Vote storage vote = votes[msg.sender][voteIndex];
        require(
            block.timestamp >= vote.unlockTime,
            "Still locked"
        );
        
        uint256 amount = vote.amount;
        lockedAmount[msg.sender] -= amount;
        token.transfer(msg.sender, amount);
        
        emit TokensUnlocked(msg.sender, amount);
    }
}
```

### **2. Не блокирующий механизм**

1. **Снапшот балансов:**
   ```solidity
   contract SnapshotGovernance {
       struct Proposal {
           uint256 id;
           uint256 snapshotBlock;
           mapping(address => bool) hasVoted;
       }
       
       mapping(uint256 => Proposal) public proposals;
       mapping(uint256 => mapping(address => uint256)) public snapshots;
       
       function createProposal() external returns (uint256) {
           uint256 proposalId = proposalCount++;
           Proposal storage proposal = proposals[proposalId];
           proposal.id = proposalId;
           proposal.snapshotBlock = block.number;
           
           // Создание снапшота балансов
           address[] memory voters = getVoters();
           for (uint256 i = 0; i < voters.length;) {
               snapshots[proposalId][voters[i]] = token.balanceOf(voters[i]);
               unchecked { i++; }
           }
           
           return proposalId;
       }
       
       function castVote(
           uint256 proposalId,
           bool support
       ) external {
           Proposal storage proposal = proposals[proposalId];
           require(!proposal.hasVoted[msg.sender], "Already voted");
           
           uint256 votingPower = snapshots[proposalId][msg.sender];
           require(votingPower > 0, "No voting power");
           
           proposal.hasVoted[msg.sender] = true;
           // Учет голоса
       }
   }
   ```

2. **Checkpointing:**
   ```solidity
   contract CheckpointGovernance {
       struct Checkpoint {
           uint256 fromBlock;
           uint256 votes;
       }
       
       mapping(address => Checkpoint[]) private _checkpoints;
       
       function writeCheckpoint(
           address account,
           uint256 newVotes
       ) internal {
           uint256 pos = _checkpoints[account].length;
           
           if (pos > 0 &&
               _checkpoints[account][pos - 1].fromBlock == block.number) {
               _checkpoints[account][pos - 1].votes = newVotes;
           } else {
               _checkpoints[account].push(Checkpoint({
                   fromBlock: block.number,
                   votes: newVotes
               }));
           }
       }
       
       function getPriorVotes(
           address account,
           uint256 blockNumber
       ) public view returns (uint256) {
           require(blockNumber < block.number, "Not determined");
           
           Checkpoint[] storage checkpoints = _checkpoints[account];
           if (checkpoints.length == 0) return 0;
           
           // Бинарный поиск чекпоинта
           uint256 low = 0;
           uint256 high = checkpoints.length - 1;
           
           while (low < high) {
               uint256 mid = (low + high + 1) / 2;
               if (checkpoints[mid].fromBlock <= blockNumber) {
                   low = mid;
               } else {
                   high = mid - 1;
               }
           }
           
           return checkpoints[low].votes;
       }
   }
   ```

### **3. Гибридные решения**

1. **Частичная блокировка:**
   ```solidity
   contract HybridGovernance {
       struct VotingPower {
           uint256 locked;
           uint256 unlocked;
       }
       
       mapping(address => VotingPower) public votingPower;
       
       function lockTokens(uint256 amount) external {
           require(amount > 0, "Amount must be > 0");
           
           token.transferFrom(msg.sender, address(this), amount);
           votingPower[msg.sender].locked += amount;
       }
       
       function castVote(
           uint256 proposalId,
           bool support,
           bool useLocked
       ) external {
           VotingPower storage power = votingPower[msg.sender];
           uint256 votes;
           
           if (useLocked) {
               votes = power.locked;
           } else {
               votes = token.balanceOf(msg.sender);
               require(votes > 0, "No voting power");
               power.unlocked = votes;
           }
           
           // Учет голоса
       }
   }
   ```

2. **Временная блокировка:**
   ```solidity
   contract TimedLockGovernance {
       struct Lock {
           uint256 amount;
           uint256 duration;
           uint256 multiplier;
       }
       
       mapping(address => Lock) public locks;
       
       function lockWithMultiplier(
           uint256 amount,
           uint256 duration
       ) external {
           require(duration >= 1 weeks, "Min 1 week");
           require(duration <= 52 weeks, "Max 52 weeks");
           
           uint256 multiplier = duration / 1 weeks;
           token.transferFrom(msg.sender, address(this), amount);
           
           locks[msg.sender] = Lock(
               amount,
               block.timestamp + duration,
               multiplier
           );
       }
       
       function getVotingPower(
           address account
       ) public view returns (uint256) {
           Lock memory lock = locks[account];
           if (block.timestamp >= lock.duration) return 0;
           return lock.amount * lock.multiplier;
       }
   }
   ```

### **4. Безопасность**

1. **Защита от атак:**
   ```solidity
   contract SecureGovernance {
       mapping(address => uint256) public lastVoteBlock;
       uint256 public constant VOTE_DELAY = 10; // блоков
       
       modifier preventFlashLoan() {
           require(
               lastVoteBlock[msg.sender] == 0 ||
               block.number >= lastVoteBlock[msg.sender] + VOTE_DELAY,
               "Recent vote"
           );
           _;
           lastVoteBlock[msg.sender] = block.number;
       }
       
       function castVote(
           uint256 proposalId,
           bool support
       ) external preventFlashLoan {
           // Голосование
       }
   }
   ```

2. **Аудит голосования:**
   ```solidity
   contract AuditedGovernance {
       event VoteCast(
           address indexed voter,
           uint256 indexed proposalId,
           bool support,
           uint256 votes,
           string reason
       );
       
       event VotingPowerChanged(
           address indexed account,
           uint256 previousBalance,
           uint256 newBalance
       );
       
       function castVoteWithReason(
           uint256 proposalId,
           bool support,
           string calldata reason
       ) external {
           uint256 votes = getVotingPower(msg.sender);
           require(votes > 0, "No voting power");
           
           emit VoteCast(
               msg.sender,
               proposalId,
               support,
               votes,
               reason
           );
           
           // Голосование
       }
   }
   ```

### **5. Примеры использования**

1. **DeFi протокол:**
   ```solidity
   contract DeFiGovernance {
       function proposeUpgrade(
           address newImplementation
       ) external {
           uint256 votingPower = getVotingPower(msg.sender);
           require(
               votingPower >= PROPOSAL_THRESHOLD,
               "Insufficient voting power"
           );
           
           // Создание предложения
       }
       
       function executeUpgrade(
           uint256 proposalId
       ) external {
           require(isProposalPassed(proposalId), "Not passed");
           require(
               getVotingPower(msg.sender) >= EXECUTION_THRESHOLD,
               "Insufficient power to execute"
           );
           
           // Выполнение обновления
       }
   }
   ```

2. **Казначейство DAO:**
   ```solidity
   contract TreasuryGovernance {
       function proposeFunding(
           address recipient,
           uint256 amount
       ) external {
           uint256 votingPower = getVotingPower(msg.sender);
           require(
               votingPower >= amount * PROPOSAL_RATIO,
               "Insufficient stake"
           );
           
           // Создание предложения
       }
   }
   ```

---

## Связанные темы
- [[Что такое и для чего необходим Governance Token?]]
- [[Voting power и баланс Governance Token это одинаковые понятия?]]
- [[Что такое DAO?]]

---

## Источники
- [Compound Governance](https://compound.finance/docs/governance)
- [Aave Governance V2](https://docs.aave.com/developers/protocol-governance/governance)
- [OpenZeppelin Governor](https://docs.openzeppelin.com/contracts/4.x/api/governance) 