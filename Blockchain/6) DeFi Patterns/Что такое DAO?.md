[[6. Список вопросов]]

## Короткий ответ

DAO (Decentralized Autonomous Organization) - это организация, управляемая смарт-контрактами и правилами, закодированными в блокчейне, где решения принимаются путем голосования участников. Основные компоненты DAO включают: токены управления (governance tokens), систему предложений и голосований, механизмы исполнения решений и прозрачные правила управления.

---

## Подробный разбор

### **1. Базовая структура DAO**

```solidity
contract SimpleDAO {
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        mapping(address => bool) hasVoted;
    }
    
    IERC20 public governanceToken;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    
    uint256 public constant VOTING_PERIOD = 3 days;
    uint256 public constant PROPOSAL_THRESHOLD = 100e18; // 100 токенов
    uint256 public constant QUORUM = 1000e18; // 1000 токенов
    
    event ProposalCreated(
        uint256 indexed id,
        address indexed proposer,
        string description,
        uint256 startTime,
        uint256 endTime
    );
    
    event VoteCast(
        address indexed voter,
        uint256 indexed proposalId,
        bool support,
        uint256 weight
    );
    
    event ProposalExecuted(uint256 indexed id);
    
    constructor(address _token) {
        governanceToken = IERC20(_token);
    }
}
```

### **2. Механизм предложений**

```solidity
contract ProposalSystem {
    struct Action {
        address target;
        uint256 value;
        bytes data;
    }
    
    function propose(
        Action[] memory actions,
        string memory description
    ) external returns (uint256) {
        require(
            governanceToken.balanceOf(msg.sender) >= PROPOSAL_THRESHOLD,
            "Insufficient tokens to propose"
        );
        
        uint256 proposalId = proposalCount++;
        Proposal storage proposal = proposals[proposalId];
        
        proposal.id = proposalId;
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + VOTING_PERIOD;
        
        emit ProposalCreated(
            proposalId,
            msg.sender,
            description,
            proposal.startTime,
            proposal.endTime
        );
        
        return proposalId;
    }
    
    function executeProposal(
        uint256 proposalId,
        Action[] memory actions
    ) external {
        Proposal storage proposal = proposals[proposalId];
        require(
            block.timestamp > proposal.endTime,
            "Voting period not ended"
        );
        require(!proposal.executed, "Already executed");
        require(
            proposal.forVotes > proposal.againstVotes &&
            proposal.forVotes >= QUORUM,
            "Proposal not passed"
        );
        
        proposal.executed = true;
        
        for (uint256 i = 0; i < actions.length;) {
            (bool success, ) = actions[i].target.call{
                value: actions[i].value
            }(actions[i].data);
            require(success, "Action execution failed");
            unchecked { i++; }
        }
        
        emit ProposalExecuted(proposalId);
    }
}
```

### **3. Система голосования**

```solidity
contract VotingSystem {
    function castVote(
        uint256 proposalId,
        bool support
    ) external {
        Proposal storage proposal = proposals[proposalId];
        require(
            block.timestamp <= proposal.endTime,
            "Voting ended"
        );
        require(
            !proposal.hasVoted[msg.sender],
            "Already voted"
        );
        
        uint256 votes = governanceToken.balanceOf(msg.sender);
        require(votes > 0, "No voting power");
        
        proposal.hasVoted[msg.sender] = true;
        
        if (support) {
            proposal.forVotes += votes;
        } else {
            proposal.againstVotes += votes;
        }
        
        emit VoteCast(msg.sender, proposalId, support, votes);
    }
    
    function getVotingPower(
        address account
    ) public view returns (uint256) {
        return governanceToken.balanceOf(account);
    }
}
```

### **4. Делегирование голосов**

```solidity
contract DelegatedVoting {
    mapping(address => address) public delegates;
    mapping(address => uint256) public delegatedPower;
    
    event DelegateChanged(
        address indexed delegator,
        address indexed fromDelegate,
        address indexed toDelegate
    );
    
    function delegate(address delegatee) external {
        require(delegatee != msg.sender, "Self delegation not allowed");
        
        address currentDelegate = delegates[msg.sender];
        uint256 votes = governanceToken.balanceOf(msg.sender);
        
        if (currentDelegate != address(0)) {
            delegatedPower[currentDelegate] -= votes;
        }
        
        if (delegatee != address(0)) {
            delegatedPower[delegatee] += votes;
        }
        
        delegates[msg.sender] = delegatee;
        
        emit DelegateChanged(
            msg.sender,
            currentDelegate,
            delegatee
        );
    }
    
    function getVotes(address account) public view returns (uint256) {
        return governanceToken.balanceOf(account) + delegatedPower[account];
    }
}
```

### **5. Timelock и исполнение**

```solidity
contract TimelockGovernance {
    uint256 public constant DELAY = 2 days;
    
    struct QueuedTransaction {
        address target;
        uint256 value;
        bytes data;
        uint256 eta;
        bool executed;
    }
    
    mapping(bytes32 => QueuedTransaction) public queuedTransactions;
    
    event TransactionQueued(
        bytes32 indexed txHash,
        address indexed target,
        uint256 value,
        bytes data,
        uint256 eta
    );
    
    event TransactionExecuted(
        bytes32 indexed txHash,
        address indexed target,
        uint256 value,
        bytes data
    );
    
    function queueTransaction(
        address target,
        uint256 value,
        bytes memory data
    ) external returns (bytes32) {
        require(
            msg.sender == address(this),
            "Only through governance"
        );
        
        uint256 eta = block.timestamp + DELAY;
        bytes32 txHash = keccak256(
            abi.encode(target, value, data, eta)
        );
        
        queuedTransactions[txHash] = QueuedTransaction({
            target: target,
            value: value,
            data: data,
            eta: eta,
            executed: false
        });
        
        emit TransactionQueued(txHash, target, value, data, eta);
        return txHash;
    }
    
    function executeTransaction(
        bytes32 txHash
    ) external {
        QueuedTransaction storage transaction = queuedTransactions[txHash];
        require(!transaction.executed, "Already executed");
        require(
            block.timestamp >= transaction.eta,
            "Time lock not expired"
        );
        
        transaction.executed = true;
        
        (bool success, ) = transaction.target.call{
            value: transaction.value
        }(transaction.data);
        require(success, "Transaction execution failed");
        
        emit TransactionExecuted(
            txHash,
            transaction.target,
            transaction.value,
            transaction.data
        );
    }
}
```

### **6. Примеры использования**

1. **Управление протоколом DeFi:**
   ```solidity
   contract DeFiGovernance is SimpleDAO {
       function updateFees(uint256 newFee) external {
           require(msg.sender == address(this), "Only through governance");
           // Обновление комиссий
       }
       
       function updatePools(address[] memory pools) external {
           require(msg.sender == address(this), "Only through governance");
           // Обновление пулов
       }
       
       function emergencyAction() external {
           require(msg.sender == address(this), "Only through governance");
           // Экстренные действия
       }
   }
   ```

2. **Управление казначейством:**
   ```solidity
   contract TreasuryGovernance is SimpleDAO {
       function allocateFunds(
           address recipient,
           uint256 amount
       ) external {
           require(msg.sender == address(this), "Only through governance");
           // Выделение средств
       }
       
       function investFunds(
           address investment,
           uint256 amount
       ) external {
           require(msg.sender == address(this), "Only through governance");
           // Инвестирование средств
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Что такое и для чего необходим Governance Token?]]
- [[Как происходит процесс голосования в DAO?]]
- [[Что такое Multisig?]]
- [[Что такое и для чего необходим Governance Token?]]

## Источники
- [Compound DAO](https://compound.finance/docs/governance)
- [Uniswap Governance](https://docs.uniswap.org/protocol/concepts/governance/overview)
- [MakerDAO Documentation](https://docs.makerdao.com/) 