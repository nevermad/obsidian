## Короткий ответ

ERC-20 определяет стандартный интерфейс для взаимозаменяемых токенов, включая обязательные функции (`totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, `allowance`), опциональные функции (`name`, `symbol`, `decimals`) и события (`Transfer`, `Approval`). Стандарт обеспечивает совместимость токенов с DeFi протоколами и кошельками.

---

## Подробный разбор

### **1. Обязательные функции**

1. **Базовые запросы:**
   ```solidity
   interface IERC20 {
       // Общее количество токенов
       function totalSupply() external view returns (uint256);
       
       // Баланс конкретного адреса
       function balanceOf(address account) external view returns (uint256);
   }
   ```

2. **Функции передачи:**
   ```solidity
   interface IERC20 {
       // Прямая передача токенов
       function transfer(address to, uint256 amount) external returns (bool);
       
       // Передача от имени другого адреса
       function transferFrom(
           address from,
           address to,
           uint256 amount
       ) external returns (bool);
   }
   ```

3. **Функции одобрения:**
   ```solidity
   interface IERC20 {
       // Одобрение на списание токенов
       function approve(address spender, uint256 amount) external returns (bool);
       
       // Проверка одобренной суммы
       function allowance(
           address owner,
           address spender
       ) external view returns (uint256);
   }
   ```

### **2. Опциональные функции**

1. **Метаданные токена:**
   ```solidity
   interface IERC20Metadata {
       // Название токена (например, "Ethereum")
       function name() external view returns (string memory);
       
       // Символ токена (например, "ETH")
       function symbol() external view returns (string memory);
       
       // Количество десятичных знаков (обычно 18)
       function decimals() external view returns (uint8);
   }
   ```

### **3. События**

1. **Обязательные события:**
   ```solidity
   interface IERC20 {
       // Событие передачи токенов
       event Transfer(address indexed from, address indexed to, uint256 value);
       
       // Событие одобрения списания
       event Approval(
           address indexed owner,
           address indexed spender,
           uint256 value
       );
   }
   ```

### **4. Стандартная имплементация**

```solidity
contract ERC20 is IERC20, IERC20Metadata {
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    uint256 private _totalSupply;
    string private _name;
    string private _symbol;
    
    constructor(string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
    }
    
    function transfer(address to, uint256 amount) external returns (bool) {
        address owner = msg.sender;
        _transfer(owner, to, amount);
        return true;
    }
    
    function _transfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual {
        require(from != address(0), "ERC20: transfer from zero");
        require(to != address(0), "ERC20: transfer to zero");
        
        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: insufficient");
        
        unchecked {
            _balances[from] = fromBalance - amount;
            _balances[to] += amount;
        }
        
        emit Transfer(from, to, amount);
    }
    
    function approve(address spender, uint256 amount) external returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }
    
    function _approve(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {
        require(owner != address(0), "ERC20: approve from zero");
        require(spender != address(0), "ERC20: approve to zero");
        
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}
```

### **5. Особенности и ограничения**

1. **Безопасность:**
   ```solidity
   contract SafeERC20 {
       // Защита от race condition в approve
       function safeApprove(IERC20 token, address spender, uint256 value) internal {
           require(
               (value == 0) || (token.allowance(address(this), spender) == 0),
               "SafeERC20: approve from non-zero to non-zero allowance"
           );
           token.approve(spender, value);
       }
       
       // Безопасный трансфер с проверкой возврата
       function safeTransfer(IERC20 token, address to, uint256 value) internal {
           bool success = token.transfer(to, value);
           require(success, "SafeERC20: transfer failed");
       }
   }
   ```

2. **Расширения:**
   ```solidity
   contract ERC20Extended is ERC20 {
       // Минтинг новых токенов
       function mint(address account, uint256 amount) external {
           _mint(account, amount);
       }
       
       // Сжигание токенов
       function burn(uint256 amount) external {
           _burn(msg.sender, amount);
       }
       
       // Пауза транзакций
       bool private _paused;
       modifier whenNotPaused() {
           require(!_paused, "Paused");
           _;
       }
   }
   ```

### **6. Лучшие практики**

1. **Проверки безопасности:**
   ```solidity
   contract SecureERC20 is ERC20 {
       // Проверка переполнения
       using SafeMath for uint256;
       
       // Защита от reentrancy
       uint256 private _locked;
       modifier nonReentrant() {
           require(_locked == 0, "Reentrant call");
           _locked = 1;
           _;
           _locked = 0;
       }
       
       // Проверка нулевого адреса
       modifier validAddress(address account) {
           require(account != address(0), "Zero address");
           _;
       }
   }
   ```

2. **Оптимизация газа:**
   ```solidity
   contract GasOptimizedERC20 is ERC20 {
       // Использование unchecked для экономии газа
       function transfer(address to, uint256 amount) external returns (bool) {
           uint256 balance = _balances[msg.sender];
           require(balance >= amount, "Insufficient");
           
           unchecked {
               _balances[msg.sender] = balance - amount;
               _balances[to] += amount;
           }
           
           emit Transfer(msg.sender, to, amount);
           return true;
       }
   }
   ```

---

## Связанные темы
- [[6. Список вопросов]]
- [[Какие проблемы есть у современной реализации функции transfer?]]
- [[Что такое SafeERC?]]
- [[С помощью каких функций израсходовать выданный approve ERC-20?]]

---

## Источники
- [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin ERC20 Implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol)
- [ConsenSys Best Practices](https://consensys.github.io/smart-contract-best-practices/) 