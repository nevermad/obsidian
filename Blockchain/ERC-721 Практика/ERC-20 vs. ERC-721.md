# Сравнение ERC-20 и ERC-721

В этом документе рассматриваются основные различия между стандартами ERC-20 (взаимозаменяемые токены) и ERC-721 (невзаимозаменяемые токены).

[[Основы ERC-20]] · [[Основы ERC-721]]

---

## Основные характеристики

### ERC-20
- Взаимозаменяемые токены
- Все токены идентичны и равноценны
- Делимые (могут быть дробными)
- Единый баланс для всех токенов
- Общее количество токенов (totalSupply)

### ERC-721
- Невзаимозаменяемые токены (NFT)
- Каждый токен уникален
- Неделимые (только целые единицы)
- Отдельный владелец для каждого tokenId
- Метаданные для каждого токена

---

## Основные функции

### ERC-20
```solidity
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}
```

### ERC-721
```solidity
interface IERC721 {
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function setApprovalForAll(address operator, bool approved) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

---

## Ключевые различия

1. **Идентификация токенов**
   - ERC-20: Не требует идентификации отдельных токенов
   - ERC-721: Каждый токен имеет уникальный tokenId

2. **Передача токенов**
   - ERC-20: Передача определенного количества токенов
   - ERC-721: Передача конкретного токена по его ID

3. **Одобрения (Approvals)**
   - ERC-20: Одобрение на определенное количество токенов
   - ERC-721: Одобрение на конкретный токен или все токены (setApprovalForAll)

4. **Метаданные**
   - ERC-20: Обычно только название и символ
   - ERC-721: Расширенные метаданные через tokenURI

5. **Применение**
   - ERC-20: Криптовалюты, utility токены, стейблкоины
   - ERC-721: Цифровое искусство, игровые предметы, виртуальная недвижимость

---

## Взаимодействие стандартов

### Фракционирование NFT
NFT (ERC-721) может быть фракционирован в ERC-20 токены, что позволяет:
- Разделить владение дорогим NFT
- Повысить ликвидность
- Создать рынок долей NFT

### Объединение токенов
ERC-20 токены могут быть объединены обратно в NFT при условии:
- Сбора достаточного количества фракций (обычно 95-100%)
- Соблюдения условий смарт-контракта
- Сжигания ERC-20 токенов

---

## Связанные темы
- [[Примеры фракционирования NFT]]
- [[Безопасность ERC-20]]
- [[Безопасность ERC-721]]
- [[Метаданные NFT]]
