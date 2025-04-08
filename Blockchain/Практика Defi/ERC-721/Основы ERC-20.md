ERC-20 — это стандарт для взаимозаменяемых токенов в блокчейне Ethereum. Он определяет базовый интерфейс для смарт-контрактов, позволяющих создавать токены, которые могут свободно обмениваться, передаваться и использоваться в различных приложениях.

## Основные элементы ERC-20

- **totalSupply():**  
  Возвращает общее количество токенов, находящихся в обращении.

- **balanceOf(address account):**  
  Возвращает баланс токенов для указанного адреса.

- **transfer(address recipient, uint256 amount):**  
  Переводит указанное количество токенов от отправителя к получателю.

- **allowance(address owner, address spender):**  
  Показывает, сколько токенов разрешено тратить указанному адресу от имени владельца.

- **approve(address spender, uint256 amount):**  
  Разрешает указанному адресу тратить определённое количество токенов от имени владельца.

- **transferFrom(address sender, address recipient, uint256 amount):**  
  Переводит токены от одного адреса к другому с использованием разрешения.

## Пример интерфейса ERC-20

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}