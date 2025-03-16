# Архитектура проекта "Разработка модели ИИ для категоризации рекламных баннеров"

## 1. Общий обзор
Проект предназначен для автоматизированной модерации макетов и видео с использованием ИИ. Основные функции включают:
- Анализ макетов и видео на соответствие юридическим требованиям и техническому заданию.
- Анализ документов с помощью OCR и NLP.
- Поиск похожих изображений.
- Авторазметку данных для обучения моделей.
- Масштабируемость, высокая доступность и интеграция с внешними сервисами.

  >>> Не все компоненты представлены в проекте ввиду коммерческой тайны 

## 2. Основные компоненты

### 2.1 Хранение данных
Данные проекта хранятся в следующей структуре:

```
moderation-ai/
├── README.md
├── requirements.txt
├── scripts/
│   ├── run_comet_pipeline.sh
│   ├── run_comet_pipeline.py
│   ├── notify_bot.py
│   ├── parse_log_to_excel.py
│   ├── qwen_vl_utils.py
│   ├── process_images.py
│   ├── auto_annotation.py
|   ├── README.md
├── data/
│   ├── images/
│   ├── models/
│   ├── logs/
│   ├── results/
|   ├── README.md
├── docs/
│   ├── api_documentation.md
│   ├── user_manual.md
│   ├── training_videos/
|   ├── README.md
├── tests/
│   ├── test_processing.py
│   ├── test_notifications.py
|   ├── README.md
```

### Описание файлов и папок

1. **README.md** - Основной файл с описанием проекта, инструкциями по установке, настройке и запуску.
2. **requirements.txt** - Файл с перечислением всех необходимых Python пакетов для проекта.
3. **scripts/** - Папка с основными исполняемыми скриптами.
   - **run_comet_pipeline.sh** - Bash-скрипт для запуска процесса обучения модели.
   - **run_comet_pipeline.py** - Python скрипт для обучения модели YOLO.
   - **notify_bot.py** - Скрипт для отправки уведомлений через Telegram.
   - **parse_log_to_excel.py** - Скрипт для обработки логов и сохранения их в Excel.
   - **qwen_vl_utils.py** - Вспомогательные функции для работы с моделью Qwen2VL.
   - **process_images.py** - Скрипт для обработки изображений и анализа их содержания.
   - **auto_annotation.py** - Скрипт для автоматической разметки изображений с использованием YOLO.
4. **data/** - Папка для хранения данных.
   - **images/** - Изображения для анализа.
   - **models/** - Обученные модели.
   - **logs/** - Логи выполнения скриптов.
   - **results/** - Результаты анализа изображений.
5. **docs/** - Документация проекта.
   - **api_documentation.md** - Описание API проекта.
   - **user_manual.md** - Руководство пользователя.
   - **training_videos/** - Видео инструкции по использованию системы.
6. **tests/** - Тесты для проверки функциональности проекта.
   - **test_processing.py** - Тесты для проверки обработки изображений.
   - **test_notifications.py** - Тесты для проверки системы уведомлений.

### Пример содержимого некоторых файлов

**README.md**
```markdown
# Moderation AI Project

This project aims to automate the moderation of advertising layouts using AI technologies.

## Установка
Clone the repository and install the required packages:
```bash
git clone https://github.com/yourusername/moderation-ai.git
cd moderation-ai
pip install -r requirements.txt
```

## Использование
To start the model training process:
```bash
bash scripts/run_comet_pipeline.sh
```

For more details, refer to the [user manual](docs/README.md).
```
---

## Поддержка и обратная связь

Если у вас возникли вопросызачечания или предложения, свяжитесь со мной:
- Email: lidushehca188@mail.com
- Telegram: @lidiya_cutie
---
