---
marp: true
theme: uncover
_class: invert lead
class: invert
author: virashu
lang: ru
transition: fade
style: |
  .morph {
    display: inline-block;
    view-transition-name: var(--id);
    contain: layout;
    vertical-align: top;
  }
  img[alt="screenshot"] {
    view-transition-name: screenshot;
    contain: layout;
  }
  .ma {
     margin-left: auto;
     margin-right: auto;
  }
---

<!-- _footer: 2023 Сёмин В. -->

# ♟ Шахматы

##### Проект на Python с использованием Qt

---

# Введение

Цель проекта: Создать приложение, использующее функционал библиотек `PyQt` и `SQLite3`.

В качестве приложения была выбрана игра _"шахматы"_.

---

<div style="display:flex;">
  <style>ul{display:flex;flex-direction:column;align-items:center;}</style>
  <ul>
  <h2>Архитектура</h2>
    Приложение состоит из 3 модулей:
    <div>
      <li><span class="morph" style="--id: hBackend;">Chess</span></li>
      <li><span class="morph" style="--id: hFrontend;">UI</span></li>
      <li><span class="morph" style="--id: hDatabase;">Database</span></li>
    </div>
  </ul>
  <img src="media/arch.png" style="">
</div>

---

## <span class="morph" style="--id: hBackend;">Chess</span>

Содержит определение класса `Board` доски, а также дополнительный модуль `Pieces` с определением классов всех фигур.

---

## <span class="morph" style="--id: hBackend;">Chess</span>

Класс `Board` является основным интерфейсом взаимодействия с игровым полем и содержит
все его свойства (положение фигур, очередь хода, состояния шаха и мата)

---

## <span class="morph" style="--id: hBackend;">Chess</span>

|        Метод        |        Функционал        |
| :-----------------: | :----------------------: |
|   `move_piece()`    |    Перемещение фигуры    |
|    `get_piece()`    |  Прямой доступ к фигуре  |
|  `field_to_text()`  | Дамп поля для сохранения |
| `field_from_text()` |      Загрузка поля       |

---

<!-- header: Chess -->

## Pieces

Классы фигур содержат методы проверки на правильность хода.

Их экземпляры содержат собственный цвет и количество совершенных ходов.

---

<!-- header: "" -->

## <span class="morph" style="--id: hFrontend;">UI</span>

| Для создания интерфейса использовалась библиотека PyQt.<br>Внешний вид приложения: | ![screenshot](media/screenshot.png) |
| ---------------------------------------------------------------------------------- | ----------------------------------- |

---

<!-- header: UI -->
<!-- _footer: Интерфейс -->

<img alt="screenshot" src="media/screenshot.png" style="width: 48%;" class="ma">

---

<span class="morph" style="--id: dText;">При достижении пешкой противоположного края доски появляется диалоговое окно:</span>

<img alt="dialog" src="media/promotion.png" style="width: 30%;" class="ma">

---

<span class="morph" style="--id: dText;">При завершении игры появляется диалог с результатом:</span>

<img alt="dialog" src="media/result.png" class="ma" style="width: 20%;">

---

<!-- header: "" -->

## <span class="morph" style="--id: hDatabase;">Database</span>

Содержит класс для удобного взаимодействия с базой данных, которая в свою очередь
хранит список ходов в следующем формате:

| id  | field (STRING) | turn (STRING) |
| --- | -------------- | ------------- |
| 1   | pW,\_,bK...    | w             |
| 2   | \_,\_,bK...    | b             |

---

<!-- header: "" -->

## <span class="morph" style="--id: hDatabase;">Database</span>

Также класс способен записывать победителей в таблицу лидеров

---

<img src="media/qr.svg" style="width: 50%; background: white; border-radius: 10%;" class="ma">

https://github.com/virashu/pychessqt

---

## Спасибо за внимание!

## Прошу задавать вопросы
