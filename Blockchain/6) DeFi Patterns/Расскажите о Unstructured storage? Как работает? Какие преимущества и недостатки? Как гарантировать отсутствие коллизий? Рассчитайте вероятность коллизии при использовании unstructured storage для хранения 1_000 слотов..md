---
title: Unstructured Storage
tags:
  - proxy
  - storage
  - evm
  - solidity
aliases:
  - неструктурированное хранилище
---

## Краткий ответ

Unstructured storage - это паттерн хранения данных в смарт-контрактах, где вместо последовательного размещения переменных используются псевдослучайные слоты, вычисляемые как keccak256 хеш от уникального идентификатора. Это позволяет избежать коллизий при обновлении контрактов и гарантирует, что переменные не будут перезаписаны.

## Подробное объяснение

### Как работает

```solidity
// Пример использования unstructured storage
contract UnstructuredStorageExample {
    // Вычисление слота для implementation адреса
    bytes32 private constant IMPLEMENTATION_SLOT = 
        bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
        
    // Чтение из unstructured storage
    function _implementation() internal view returns (address impl) {
        assembly {
            impl := sload(IMPLEMENTATION_SLOT)
        }
    }
    
    // Запись в unstructured storage
    function _setImplementation(address newImplementation) internal {
        assembly {
            sstore(IMPLEMENTATION_SLOT, newImplementation)
        }
    }
}
```

### Преимущества

1. Независимость от порядка переменных
2. Устойчивость к коллизиям при обновлении контрактов
3. Возможность добавлять новые переменные без влияния на существующие
4. Безопасное хранение критических данных
5. Совместимость с прокси-паттернами

### Недостатки

1. Повышенное потребление газа при доступе к storage
2. Сложность в отладке и аудите
3. Необходимость использования assembly
4. Риск коллизий при неправильном выборе идентификаторов
5. Отсутствие автоматической проверки типов

### Гарантия отсутствия коллизий

1. Использование уникальных строковых идентификаторов
2. Применение namespace для разных типов данных
3. Добавление версий к идентификаторам
4. Использование стандартизированных слотов (например, как в EIP-1967)

### Расчет вероятности коллизии

Для 1000 слотов в unstructured storage:

1. Размер пространства слотов: 2^256 (размер keccak256 хеша)
2. Количество занятых слотов: 1000
3. Вероятность коллизии по формуле дней рождения:
   P(коллизия) = 1 - e^(-n(n-1)/(2N))
   где n = 1000, N = 2^256

```python
P ≈ 1 - e^(-499500/2^257) ≈ 1.17 * 10^-74
```

Вероятность коллизии практически равна нулю, что делает unstructured storage безопасным для использования.

## Примеры использования

1. OpenZeppelin Proxy контракты
2. EIP-1967 стандарт
3. Beacon прокси
4. UUPS прокси
5. Управление доступом в смарт-контрактах

## Связанные темы
- [[6. Список вопросов]]

- [[Что такое storage collision?]]
- [[Расскажите о стандарте ERC1967?]]
- [[Как работает delegatecall?]]
- [[Расскажите подробно как работает паттерн proxy?]]

## Источники
- [OpenZeppelin Proxy Storage](https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies#storage)
- [EIP-1967](https://eips.ethereum.org/EIPS/eip-1967)
- [Solidity Storage Layout](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)
