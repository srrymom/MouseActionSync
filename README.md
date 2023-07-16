# MouseActionSync

MouseActionSync - это программное решение, которое позволяет записывать и синхронизировать действия мыши на разных компьютерах.

## Описание

MouseActionSync состоит из трех компонентов:
- **mouse_recorder**: программа, которая записывает действия мыши на экране и отправляет их на сервер.
- **server**: серверная программа, которая принимает записанные события мыши и сохраняет их для последующего использования.
- **mouse_replayer**: программа, которая обращается к серверу и воспроизводит записанные действия мыши на других компьютерах..

## Требования

- Python 3.7 или выше.
- Установленные библиотеки: pynput, requests, bottle.