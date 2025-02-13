[[6. Список вопросов]]

## Короткий ответ

Role-based AccessControl от OpenZeppelin - это система управления доступом на основе ролей, где каждая роль может иметь множество участников и администраторов. Контракт использует `DEFAULT_ADMIN_ROLE` как суперроль, которая может управлять всеми остальными ролями. Система позволяет гибко настраивать права доступа и иерархию ролей через механизм администрирования ролей.

---

## Подробный разбор

### **1. Базовая реализация OpenZeppelin**

```solidity
abstract contract AccessControl {
    struct RoleData {
        mapping(address => bool) members;
        bytes32 adminRole;
    }
    
    mapping(bytes32 => RoleData) private _roles;
    
    bytes32 public constant DEFAULT_ADMIN_ROLE = 0x00;
    
    event RoleAdminChanged(
        bytes32 indexed role,
        bytes32 indexed previousAdminRole,
        bytes32 indexed newAdminRole
    );
    
    event RoleGranted(
        bytes32 indexed role,
        address indexed account,
        address indexed sender
    );
    
    event RoleRevoked(
        bytes32 indexed role,
        address indexed account,
        address indexed sender
    );
    
    modifier onlyRole(bytes32 role) {
        require(
            hasRole(role, msg.sender),
            "AccessControl: account is missing role"
        );
        _;
    }
    
    function hasRole(
        bytes32 role,
        address account
    ) public view virtual returns (bool) {
        return _roles[role].members[account];
    }
    
    function getRoleAdmin(
        bytes32 role
    ) public view virtual returns (bytes32) {
        return _roles[role].adminRole;
    }
    
    function grantRole(
        bytes32 role,
        address account
    ) public virtual onlyRole(getRoleAdmin(role)) {
        _grantRole(role, account);
    }
    
    function revokeRole(
        bytes32 role,
        address account
    ) public virtual onlyRole(getRoleAdmin(role)) {
        _revokeRole(role, account);
    }
    
    function renounceRole(
        bytes32 role,
        address account
    ) public virtual {
        require(
            account == msg.sender,
            "AccessControl: can only renounce roles for self"
        );
        _revokeRole(role, account);
    }
}
```

### **2. Примеры использования**

1. **Управление токеном:**
   ```solidity
   contract ManagedToken is ERC20, AccessControl {
       bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
       bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");
       bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
       
       constructor() ERC20("Managed", "MGD") {
           _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
           _setRoleAdmin(MINTER_ROLE, DEFAULT_ADMIN_ROLE);
           _setRoleAdmin(BURNER_ROLE, DEFAULT_ADMIN_ROLE);
           _setRoleAdmin(PAUSER_ROLE, DEFAULT_ADMIN_ROLE);
       }
       
       function mint(
           address to,
           uint256 amount
       ) external onlyRole(MINTER_ROLE) {
           _mint(to, amount);
       }
       
       function burn(
           address from,
           uint256 amount
       ) external onlyRole(BURNER_ROLE) {
           _burn(from, amount);
       }
       
       function pause() external onlyRole(PAUSER_ROLE) {
           _pause();
       }
   }
   ```

2. **Управление протоколом:**
   ```solidity
   contract DeFiProtocol is AccessControl {
       bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
       bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");
       bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");
       
       constructor() {
           _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
           
           // Настройка администраторов ролей
           _setRoleAdmin(OPERATOR_ROLE, DEFAULT_ADMIN_ROLE);
           _setRoleAdmin(UPGRADER_ROLE, DEFAULT_ADMIN_ROLE);
           _setRoleAdmin(EMERGENCY_ROLE, DEFAULT_ADMIN_ROLE);
       }
       
       function setFees(uint256 newFee) external onlyRole(OPERATOR_ROLE) {
           // Изменение комиссий
       }
       
       function upgrade(address newImpl) external onlyRole(UPGRADER_ROLE) {
           // Обновление контракта
       }
       
       function emergencyWithdraw() external onlyRole(EMERGENCY_ROLE) {
           // Экстренный вывод средств
       }
   }
   ```

### **3. Иерархия ролей**

1. **Настройка иерархии:**
   ```solidity
   contract HierarchicalAccess is AccessControl {
       bytes32 public constant LEVEL1_ROLE = keccak256("LEVEL1_ROLE");
       bytes32 public constant LEVEL2_ROLE = keccak256("LEVEL2_ROLE");
       bytes32 public constant LEVEL3_ROLE = keccak256("LEVEL3_ROLE");
       
       constructor() {
           _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
           
           // Level1 управляется DEFAULT_ADMIN
           _setRoleAdmin(LEVEL1_ROLE, DEFAULT_ADMIN_ROLE);
           
           // Level2 управляется Level1
           _setRoleAdmin(LEVEL2_ROLE, LEVEL1_ROLE);
           
           // Level3 управляется Level2
           _setRoleAdmin(LEVEL3_ROLE, LEVEL2_ROLE);
       }
       
       function level1Action() external onlyRole(LEVEL1_ROLE) {
           // Действия уровня 1
       }
       
       function level2Action() external onlyRole(LEVEL2_ROLE) {
           // Действия уровня 2
       }
       
       function level3Action() external onlyRole(LEVEL3_ROLE) {
           // Действия уровня 3
       }
   }
   ```

2. **Множественные администраторы:**
   ```solidity
   contract MultiAdminAccess is AccessControl {
       bytes32 public constant ROLE_A = keccak256("ROLE_A");
       bytes32 public constant ROLE_B = keccak256("ROLE_B");
       bytes32 public constant ADMIN_GROUP = keccak256("ADMIN_GROUP");
       
       constructor() {
           _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
           
           // ADMIN_GROUP управляется DEFAULT_ADMIN
           _setRoleAdmin(ADMIN_GROUP, DEFAULT_ADMIN_ROLE);
           
           // Роли A и B управляются ADMIN_GROUP
           _setRoleAdmin(ROLE_A, ADMIN_GROUP);
           _setRoleAdmin(ROLE_B, ADMIN_GROUP);
       }
   }
   ```

### **4. DEFAULT_ADMIN_ROLE**

1. **Особенности DEFAULT_ADMIN_ROLE:**
   ```solidity
   contract AdminExample is AccessControl {
       constructor() {
           // DEFAULT_ADMIN_ROLE имеет полный доступ
           _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
           
           // DEFAULT_ADMIN_ROLE может управлять собой
           assert(getRoleAdmin(DEFAULT_ADMIN_ROLE) == DEFAULT_ADMIN_ROLE);
       }
       
       function addAdmin(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
           grantRole(DEFAULT_ADMIN_ROLE, account);
       }
       
       function removeAdmin(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
           revokeRole(DEFAULT_ADMIN_ROLE, account);
       }
   }
   ```

2. **Безопасная передача DEFAULT_ADMIN_ROLE:**
   ```solidity
   contract SafeAdminTransfer is AccessControl {
       function transferAdmin(
           address newAdmin
       ) external onlyRole(DEFAULT_ADMIN_ROLE) {
           require(newAdmin != address(0), "Zero address");
           
           // Сначала выдаем права новому админу
           grantRole(DEFAULT_ADMIN_ROLE, newAdmin);
           
           // Затем отзываем у старого
           renounceRole(DEFAULT_ADMIN_ROLE, msg.sender);
       }
   }
   ```

### **5. Как выдавать и забирать доступ**

1. **Выдача ролей:**
   ```solidity
   // 1. Выдача роли
   function grantOperator(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
       grantRole(OPERATOR_ROLE, account);
   }
   
   // 2. Проверка роли
   require(hasRole(OPERATOR_ROLE, account), "Not operator");
   
   // 3. Массовая выдача ролей
   function grantOperators(
       address[] calldata accounts
   ) external onlyRole(DEFAULT_ADMIN_ROLE) {
       for (uint256 i = 0; i < accounts.length;) {
           grantRole(OPERATOR_ROLE, accounts[i]);
           unchecked { i++; }
       }
   }
   ```

2. **Отзыв ролей:**
   ```solidity
   // 1. Отзыв роли администратором
   function revokeOperator(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
       revokeRole(OPERATOR_ROLE, account);
   }
   
   // 2. Отказ от роли
   function renounceOperator() external {
       renounceRole(OPERATOR_ROLE, msg.sender);
   }
   
   // 3. Массовый отзыв ролей
   function revokeOperators(
       address[] calldata accounts
   ) external onlyRole(DEFAULT_ADMIN_ROLE) {
       for (uint256 i = 0; i < accounts.length;) {
           revokeRole(OPERATOR_ROLE, accounts[i]);
           unchecked { i++; }
       }
   }
   ```

3. **Управление администраторами ролей:**
   ```solidity
   // 1. Изменение администратора роли
   function setRoleAdmin(
       bytes32 role,
       bytes32 adminRole
   ) external onlyRole(DEFAULT_ADMIN_ROLE) {
       _setRoleAdmin(role, adminRole);
   }
   
   // 2. Проверка администратора роли
   bytes32 admin = getRoleAdmin(role);
   require(hasRole(admin, msg.sender), "Not admin of role");
   ```

---

## Связанные темы
- [[Что представляет из себя access control паттерн?]]
- [[Расскажите идею и возможности паттерна Ownable]]
- [[Расскажите идею и возможности паттерна Ownable2Step]]

---

## Источники
- [OpenZeppelin AccessControl](https://docs.openzeppelin.com/contracts/4.x/api/access#AccessControl)
- [OpenZeppelin Access Control Guide](https://docs.openzeppelin.com/contracts/4.x/access-control)
- [Smart Contract Security Best Practices](https://consensys.github.io/smart-contract-best-practices/) 