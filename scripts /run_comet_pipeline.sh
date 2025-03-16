#!/bin/bash

COMET_API_KEY="YOUR_API_KEY"
export COMET_API_KEY  # Экспортируем переменную

# Проверка значения переменной
echo "COMET_API_KEY в bash-скрипте: $COMET_API_KEY"

check_gpu_free() {
  GPU_USAGE=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | awk '{sum+=$1} END {print sum}')
  GPU_MEMORY_FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | awk '{sum+=$1} END {print sum}')
  
  echo "Текущая загрузка GPU: $GPU_USAGE%"
  echo "Свободная память GPU: $GPU_MEMORY_FREE MiB"
  
  # Проверяем, если GPU-Util < 95% и свободно более 10GB памяти
  if [ "$GPU_USAGE" -lt 95 ] && [ "$GPU_MEMORY_FREE" -gt 10240 ]; then
    return 0
  else
    return 1
  fi
}

check_gpu_processes() {
  GPU_PROCESSES=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits | wc -l)
  if [ "$GPU_PROCESSES" -gt 0 ]; then
    echo "Обнаружены активные процессы на GPU:"
    nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader,nounits
    return 1
  fi
  echo "На GPU нет активных процессов."
  return 0
}

check_gpu_ready() {
  if check_gpu_free; then
    echo "Выполняется вторичная проверка через 10 секунд..."
    sleep 10
    if check_gpu_free; then
      echo "GPU готов к запуску."
      return 0
    fi
  fi
  echo "GPU занят."
  return 1
}

generate_log_name() {
  TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
  echo "/mldata/wait_output/wait_output_${TIMESTAMP}.log"
}

echo "Ожидание освобождения GPU..."
while ! check_gpu_ready; do
  echo "GPU занят, повторная проверка через 45 секунд..."
  sleep 45
done

LOG_FILE=$(generate_log_name)
echo "GPU свободен. Запускаю скрипт..."

sudo COMET_API_KEY="$COMET_API_KEY" nohup /path/to/venv/bin/python /path/to/run_comet_pipeline.py > "$LOG_FILE" 2>&1 &
PROCESS_PID=$!  # Сохраняем PID запущенного процесса
echo "Скрипт запущен в фоне с PID=$PROCESS_PID. Лог записывается в $LOG_FILE."

echo "Отправляю уведомление о запуске..."
sudo nohup /path/to/venv/bin/python /path/to/notify_bot.py "Обучение началось. Лог: $LOG_FILE" &

wait $PROCESS_PID
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  sudo nohup /path/to/venv/bin/python /path/to/notify_bot.py "Обучение завершено успешно! Логи сохранены в $LOG_FILE"
  echo "Запускаю обработку логов..."
  sudo nohup /path/to/venv/bin/python /path/to/parse_log_to_excel.py "$LOG_FILE"
  sudo nohup /path/to/venv/bin/python /path/to/notify_bot.py "Логи успешно обработаны и добавлены в Excel."
else
  sudo nohup /path/to/venv/bin/python /path/to/notify_bot.py "Обучение завершено с ошибкой (код $EXIT_CODE). Логи: $LOG_FILE"
fi
