[[6. Список вопросов]]

## Короткий ответ

Governance Token - это токен, предоставляющий право участия в управлении DAO или протоколом. Количество токенов определяет вес голоса участника при принятии решений. Процесс голосования включает создание предложений, обсуждение, голосование и исполнение решений. Токены могут использоваться для прямого голосования или делегирования голосов другим участникам.

---

## Подробный разбор

### **1. Базовая реализация Governance Token**

```solidity
contract GovernanceToken is ERC20, ERC20Permit {
    // Базовая функциональность токена
    constructor() ERC20("Governance", "GOV") ERC20Permit("Governance") {
        _mint(msg.sender, 1000000 * 10**decimals());
    }
    
    // Делегирование голосов
    mapping(address => address) private _delegates;
    mapping(address => uint256) private _delegatedPower;
    
    event DelegateChanged(
        address indexed delegator,
        address indexed fromDelegate,
        address indexed toDelegate
    );
    
    function delegates(address account) external view returns (address) {
        return _delegates[account];
    }
    
    function delegate(address delegatee) external {
        _delegate(msg.sender, delegatee);
    }
    
    function _delegate(address delegator, address delegatee) internal {
        address currentDelegate = _delegates[delegator];
        uint256 delegatorBalance = balanceOf(delegator);
        _delegates[delegator] = delegatee;
        
        if (currentDelegate != address(0)) {
            _delegatedPower[currentDelegate] -= delegatorBalance;
        }
        if (delegatee != address(0)) {
            _delegatedPower[delegatee] += delegatorBalance;
        }
        
        emit DelegateChanged(delegator, currentDelegate, delegatee);
    }
    
    function getVotes(address account) public view returns (uint256) {
        return balanceOf(account) + _delegatedPower[account];
    }
}
```

### **2. Процесс голосования**

```solidity
contract GovernanceVoting {
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 startBlock;
        uint256 endBlock;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
        mapping(address => Receipt) receipts;
    }
    
    struct Receipt {
        bool hasVoted;
        bool support;
        uint256 votes;
    }
    
    IGovernanceToken public token;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    
    uint256 public constant VOTING_DELAY = 1 days;
    uint256 public constant VOTING_PERIOD = 3 days;
    uint256 public constant PROPOSAL_THRESHOLD = 100e18; // 100 токенов
    
    event ProposalCreated(
        uint256 indexed id,
        address indexed proposer,
        string description,
        uint256 startBlock,
        uint256 endBlock
    );
    
    event VoteCast(
        address indexed voter,
        uint256 indexed proposalId,
        bool support,
        uint256 votes
    );
    
    constructor(address _token) {
        token = IGovernanceToken(_token);
    }
    
    function propose(
        string memory description
    ) external returns (uint256) {
        require(
            token.getVotes(msg.sender) >= PROPOSAL_THRESHOLD,
            "GovernanceVoting: below proposal threshold"
        );
        
        uint256 proposalId = proposalCount++;
        Proposal storage proposal = proposals[proposalId];
        
        proposal.id = proposalId;
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.startBlock = block.timestamp + VOTING_DELAY;
        proposal.endBlock = proposal.startBlock + VOTING_PERIOD;
        
        emit ProposalCreated(
            proposalId,
            msg.sender,
            description,
            proposal.startBlock,
            proposal.endBlock
        );
        
        return proposalId;
    }
    
    function castVote(
        uint256 proposalId,
        bool support
    ) external {
        require(
            block.timestamp >= proposals[proposalId].startBlock,
            "Voting not started"
        );
        require(
            block.timestamp <= proposals[proposalId].endBlock,
            "Voting ended"
        );
        
        Proposal storage proposal = proposals[proposalId];
        Receipt storage receipt = proposal.receipts[msg.sender];
        require(!receipt.hasVoted, "Already voted");
        
        uint256 votes = token.getVotes(msg.sender);
        require(votes > 0, "No voting power");
        
        receipt.hasVoted = true;
        receipt.support = support;
        receipt.votes = votes;
        
        if (support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }
        
        emit VoteCast(msg.sender, proposalId, support, votes);
    }
}
```

### **3. Влияние токена на голосование**

1. **Квадратичное голосование:**
   ```solidity
   contract QuadraticVoting {
       function getVotingPower(
           uint256 tokenAmount
       ) public pure returns (uint256) {
           // Квадратный корень из количества токенов
           return sqrt(tokenAmount);
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

2. **Взвешенное голосование:**
   ```solidity
   contract WeightedVoting {
       struct Vote {
           uint256 weight;
           bool support;
       }
       
       mapping(uint256 => mapping(address => Vote)) public votes;
       
       function castWeightedVote(
           uint256 proposalId,
           uint256 weight,
           bool support
       ) external {
           require(weight <= 100, "Weight must be <= 100");
           
           uint256 votingPower = token.getVotes(msg.sender);
           uint256 weightedVotes = (votingPower * weight) / 100;
           
           votes[proposalId][msg.sender] = Vote(weightedVotes, support);
       }
   }
   ```

### **4. Механизмы защиты**

1. **Временная блокировка:**
   ```solidity
   contract TimeLockVoting {
       mapping(address => uint256) public lockEndTime;
       
       function lockTokens(uint256 duration) external {
           uint256 amount = token.balanceOf(msg.sender);
           require(amount > 0, "No tokens to lock");
           
           uint256 endTime = block.timestamp + duration;
           lockEndTime[msg.sender] = endTime;
           
           token.transferFrom(msg.sender, address(this), amount);
       }
       
       function getVotingPower(
           address account
       ) public view returns (uint256) {
           if (block.timestamp < lockEndTime[account]) {
               return token.balanceOf(address(this));
           }
           return 0;
       }
   }
   ```

2. **Защита от флэш-займов:**
   ```solidity
   contract FlashLoanProtection {
       mapping(address => uint256) public votingSnapshots;
       
       function takeSnapshot() external {
           votingSnapshots[msg.sender] = block.number;
       }
       
       function getVotingPower(
           address account
       ) public view returns (uint256) {
           require(
               votingSnapshots[account] < block.number - 1,
               "Recent snapshot"
           );
           return token.balanceOf(account);
       }
   }
   ```

### **5. Примеры использования**

1. **Управление параметрами протокола:**
   ```solidity
   contract ProtocolGovernance {
       uint256 public fee;
       address public treasury;
       
       function updateFee(
           uint256 newFee
       ) external onlyGovernance {
           require(newFee <= 1000, "Fee too high"); // max 10%
           fee = newFee;
       }
       
       function updateTreasury(
           address newTreasury
       ) external onlyGovernance {
           require(newTreasury != address(0), "Zero address");
           treasury = newTreasury;
       }
   }
   ```

2. **Управление пулами ликвидности:**
   ```solidity
   contract LiquidityGovernance {
       struct Pool {
           address token;
           uint256 weight;
           bool active;
       }
       
       mapping(address => Pool) public pools;
       
       function addPool(
           address token,
           uint256 weight
       ) external onlyGovernance {
           require(weight <= 100, "Weight too high");
           pools[token] = Pool(token, weight, true);
       }
       
       function updatePoolWeight(
           address token,
           uint256 newWeight
       ) external onlyGovernance {
           require(pools[token].active, "Pool not active");
           pools[token].weight = newWeight;
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое DAO?]]
- [[Voting power и баланс Governance Token это одинаковые понятия?]]
- [[При голосовании Governance Token блокируется?]]

---

## Источники
- [Compound Governance](https://compound.finance/docs/governance)
- [Uniswap Governance](https://docs.uniswap.org/protocol/concepts/governance/overview)
- [OpenZeppelin Governor](https://docs.openzeppelin.com/contracts/4.x/api/governance) 