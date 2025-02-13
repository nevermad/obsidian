[[6. Список вопросов]]

## Короткий ответ

К аккаунтам участников Multisig предъявляются строгие требования безопасности: использование холодных кошельков или hardware wallets, надежное хранение приватных ключей, регулярная ротация ключей, разделение ключей между разными физическими локациями и лицами, использование различных устройств для подписи транзакций и обязательное резервное копирование.

---

## Подробный разбор

### **1. Базовые требования безопасности**

1. **Типы кошельков:**
   ```solidity
   contract MultisigRequirements {
       enum WalletType {
           HOT,      // Онлайн кошельки (не рекомендуется)
           COLD,     // Оффлайн хранение
           HARDWARE  // Аппаратные кошельки
       }
       
       struct OwnerWallet {
           address wallet;
           WalletType walletType;
           uint256 lastActivity;
           bool isActive;
       }
       
       mapping(address => OwnerWallet) public ownerWallets;
       
       modifier onlyHardwareWallet(address wallet) {
           require(
               ownerWallets[wallet].walletType == WalletType.HARDWARE,
               "Only hardware wallets allowed"
           );
           _;
       }
   }
   ```

2. **Проверки активности:**
   ```solidity
   contract ActivityMonitoring {
       uint256 public constant MAX_INACTIVITY_PERIOD = 90 days;
       
       function checkActivity(address owner) public view returns (bool) {
           return block.timestamp - lastActivity[owner] <= MAX_INACTIVITY_PERIOD;
       }
       
       function updateActivity(address owner) internal {
           lastActivity[owner] = block.timestamp;
           emit OwnerActivity(owner);
       }
       
       function requireActiveOwners() internal view {
           for (uint256 i = 0; i < owners.length;) {
               require(
                   checkActivity(owners[i]),
                   "Inactive owner detected"
               );
               unchecked { i++; }
           }
       }
   }
   ```

### **2. Управление ключами**

1. **Ротация ключей:**
   ```solidity
   contract KeyRotation {
       uint256 public constant KEY_ROTATION_PERIOD = 180 days;
       mapping(address => uint256) public lastKeyRotation;
       
       event KeyRotated(
           address indexed oldKey,
           address indexed newKey,
           uint256 timestamp
       );
       
       function rotateKey(
           address oldKey,
           address newKey
       ) external onlyOwner {
           require(
               block.timestamp >= lastKeyRotation[oldKey] + KEY_ROTATION_PERIOD,
               "Too early for rotation"
           );
           
           require(newKey != address(0), "Invalid new key");
           require(!isOwner[newKey], "Key already used");
           
           isOwner[oldKey] = false;
           isOwner[newKey] = true;
           lastKeyRotation[newKey] = block.timestamp;
           
           emit KeyRotated(oldKey, newKey, block.timestamp);
       }
   }
   ```

2. **Резервное копирование:**
   ```solidity
   contract BackupSystem {
       struct BackupInfo {
           bytes32 backupHash;
           uint256 lastUpdate;
           bool exists;
       }
       
       mapping(address => BackupInfo) public backups;
       
       event BackupUpdated(
           address indexed owner,
           bytes32 indexed backupHash
       );
       
       function updateBackup(bytes32 backupHash) external onlyOwner {
           require(backupHash != bytes32(0), "Invalid backup");
           
           backups[msg.sender] = BackupInfo({
               backupHash: backupHash,
               lastUpdate: block.timestamp,
               exists: true
           });
           
           emit BackupUpdated(msg.sender, backupHash);
       }
       
       function verifyBackup(
           address owner,
           bytes32 backupHash
       ) external view returns (bool) {
           return backups[owner].backupHash == backupHash;
       }
   }
   ```

### **3. Физическая безопасность**

1. **Географическое разделение:**
   ```solidity
   contract GeographicDistribution {
       struct Location {
           bytes32 region;
           uint256 lastUpdate;
           bool active;
       }
       
       mapping(address => Location) public ownerLocations;
       mapping(bytes32 => uint256) public regionCount;
       
       uint256 public constant MAX_OWNERS_PER_REGION = 2;
       
       function updateLocation(
           bytes32 region
       ) external onlyOwner {
           bytes32 oldRegion = ownerLocations[msg.sender].region;
           if (oldRegion != bytes32(0)) {
               regionCount[oldRegion]--;
           }
           
           require(
               regionCount[region] < MAX_OWNERS_PER_REGION,
               "Too many owners in region"
           );
           
           ownerLocations[msg.sender] = Location({
               region: region,
               lastUpdate: block.timestamp,
               active: true
           });
           regionCount[region]++;
       }
   }
   ```

2. **Устройства для подписи:**
   ```solidity
   contract DeviceManagement {
       struct Device {
           bytes32 deviceId;
           uint256 lastUsed;
           bool isActive;
       }
       
       mapping(address => Device[]) public ownerDevices;
       uint256 public constant MIN_DEVICES = 2;
       
       function addDevice(
           bytes32 deviceId
       ) external onlyOwner {
           require(deviceId != bytes32(0), "Invalid device");
           
           Device[] storage devices = ownerDevices[msg.sender];
           devices.push(Device({
               deviceId: deviceId,
               lastUsed: block.timestamp,
               isActive: true
           }));
       }
       
       function validateDevices(address owner) internal view {
           Device[] storage devices = ownerDevices[owner];
           uint256 activeDevices;
           
           for (uint256 i = 0; i < devices.length;) {
               if (devices[i].isActive) {
                   activeDevices++;
               }
               unchecked { i++; }
           }
           
           require(
               activeDevices >= MIN_DEVICES,
               "Insufficient active devices"
           );
       }
   }
   ```

### **4. Мониторинг и аудит**

1. **Система мониторинга:**
   ```solidity
   contract SecurityMonitoring {
       event UnusualActivity(
           address indexed owner,
           string activityType,
           uint256 timestamp
       );
       
       mapping(address => uint256) public lastLoginTime;
       mapping(address => string) public lastLoginLocation;
       
       function recordLogin(
           string calldata location
       ) external onlyOwner {
           if (
               lastLoginTime[msg.sender] > 0 &&
               !compareLocations(
                   location,
                   lastLoginLocation[msg.sender]
               )
           ) {
               emit UnusualActivity(
                   msg.sender,
                   "Location change",
                   block.timestamp
               );
           }
           
           lastLoginTime[msg.sender] = block.timestamp;
           lastLoginLocation[msg.sender] = location;
       }
   }
   ```

2. **Аудит действий:**
   ```solidity
   contract ActionAudit {
       struct AuditRecord {
           address owner;
           bytes32 action;
           uint256 timestamp;
           bytes data;
       }
       
       AuditRecord[] public auditLog;
       
       event ActionRecorded(
           address indexed owner,
           bytes32 indexed action,
           uint256 timestamp
       );
       
       function recordAction(
           bytes32 action,
           bytes memory data
       ) internal {
           auditLog.push(AuditRecord({
               owner: msg.sender,
               action: action,
               timestamp: block.timestamp,
               data: data
           }));
           
           emit ActionRecorded(msg.sender, action, block.timestamp);
       }
   }
   ```

### **5. Лучшие практики**

1. **Проверки безопасности:**
   ```solidity
   contract SecurityChecks {
       // 1. Проверка сложности пароля/фразы
       function validateSecurityPhrase(
           string memory phrase
       ) internal pure returns (bool) {
           require(bytes(phrase).length >= 12, "Phrase too short");
           // Дополнительные проверки сложности
           return true;
       }
       
       // 2. Проверка устройства
       function validateDevice(
           bytes32 deviceId,
           bytes memory signature
       ) internal view returns (bool) {
           // Проверка подписи и характеристик устройства
           return true;
       }
       
       // 3. Проверка времени и локации
       function validateLoginAttempt(
           address owner,
           string memory location
       ) internal view returns (bool) {
           // Проверка подозрительной активности
           return true;
       }
   }
   ```

2. **Процедуры восстановления:**
   ```solidity
   contract RecoveryProcedures {
       struct Recovery {
           address[] approvers;
           uint256 threshold;
           uint256 delay;
           bool active;
       }
       
       mapping(address => Recovery) public recoveryPlans;
       
       function initiateRecovery(
           address owner
       ) external {
           require(
               recoveryPlans[owner].active,
               "No recovery plan"
           );
           
           // Начало процедуры восстановления
       }
       
       function approveRecovery(
           address owner
       ) external {
           require(
               isApprover[msg.sender],
               "Not an approver"
           );
           
           // Подтверждение восстановления
       }
   }
   ```

---

## Связанные темы
- [[Что такое и как работает Multisig?]]
- [[Multisig 1:2 какие могут быть проблемы?]]
- [[Что такое DAO?]]

---

## Источники
- [Gnosis Safe Security Guidelines](https://docs.gnosis-safe.io/security)
- [Hardware Wallet Security Best Practices](https://blog.trezor.io/security-best-practices)
- [ConsenSys Security Best Practices](https://consensys.github.io/smart-contract-best-practices/) 