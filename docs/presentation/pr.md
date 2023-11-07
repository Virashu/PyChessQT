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

В качестве приложения были выбрана игра *"шахматы"*.

---

## Архитектура

Приложение состоит из 3 частей:
- <span class="morph" style="--id: hBackend;">Backend</span>
- <span class="morph" style="--id: hFrontend;">Frontend</span>
- Database

---

## <span class="morph" style="--id: hBackend;">Backend</span>

Содержит определение класса `Board` доски, а также классов всех фигур.

Класс `Board` является основным интерфейсом взаимодействия с игровым полем и содержит
все его свойства (положение фигур, очередь хода, состояния шаха и мата)

---
<!-- header: Backend -->

Классы фигур содержат методы проверки на правильность хода.

Их экземпляры содержат собственный цвет.

---
<!-- header: "" -->
## <span class="morph" style="--id: hFrontend;">Frontend</span>



| Для создания интерфейса использовалась библиотека PyQt.<br>Внешний вид приложения: | ![screenshot](media/screenshot.png) |
|-|-|

---

<!-- header: Frontend -->
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
## Database

Содержит класс для удобного взаимодействия с базой данных, которая в свою очередь
хранит список ходов в следующем формате:

|id|field (STRING)|turn (STRING)|
|-|-|-|
|1|pW,_,bK...|w|
|2|\_,_,bK...|b|

---

<img src="media/qr.svg" style="width: 50%; background: white; border-radius: 10%;" class="ma">

https://github.com/virashu/pychessqt

---

## Спасибо за внимание!

## Прошу задавать вопросы
