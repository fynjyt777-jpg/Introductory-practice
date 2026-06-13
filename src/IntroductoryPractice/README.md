# Инструкция по запуску приложения из исходного кода

## 1. Системные требования

**Перед началом убедитесь, что у вас установлены:**

- Python версии 3.10 или выше (в коде использовались современные библиотеки).

- Git (для клонирования репозитория).

- Веб-камера (требуется для функций работы с видео через OpenCV).

## 2. Клонирование проекта и переход в папку

Откройте терминал/консоль и выполните:

```
git clone https://github.com/fynjyt777-ipg/Introductory-practice/tree/master/src/IntroductoryPractice
cd PythonProject 
```
(Если вы передаете проект архивом, просто распакуйте его и откройте терминал в корневой папке проекта).

## 3. Настройка виртуального окружения

Чтобы изолировать зависимости приложения от вашей системы, создайте и активируйте виртуальное окружение:

**- Для Windows (PowerShell):**

```commandline
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**- Для Linux / macOS:**

```
python3 -m venv .venv
source .venv/bin/activate
```
После активации в начале строки терминала появится префикс (.venv).

## 4. Установка зависимостей

Установите все необходимые для работы библиотеки (включая numpy и Pillow),
которые зафиксированы в файле конфигурации:

```commandline
pip install --upgrade pip
pip install -r src/IntroductoryPractice/requirements.txt
```

## 5. Запуск приложения

Запустите главный файл приложения:

```commandline
python src/IntroductoryPractice/PracticaProject.py
```