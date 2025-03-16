# Установка comet_ml (если не установлен)
#!pip install -q comet_ml

import os
from comet_ml import Experiment
from ultralytics import YOLO

# Базовый путь к проекту
base_path = "/path/to/runs" # необходимо указать путь до места, где хранится проект
data_path = "/path/to/data.yaml" # необходимо указать путь до места

# Списки гиперпараметров
optimizers = ['SGD', 'SGD']
learning_rates = [0.001]  # 0.05, , 0.01, 0.001
weight_decays = [0.0001]
conf_thresholds = [0.2]  #, 0.2 , 0.4
batches = [24]

# Начальный путь к весам
weights_path = "/path/to/best.pt" # необходимо указать путь до места, где лежат веса

# Номер итерации
iteration = 1

# Функция для обучения с заданными параметрами
def train_model(weights, optimizer, lr, weight_decay, conf, batch, iteration, experiment):
    print(f"Запуск обучения с параметрами: optimizer={optimizer}, lr={lr}, weight_decay={weight_decay}, conf={conf}, batch={batch}, iteration={iteration}")
    
    model = YOLO(weights)

    # Путь для сохранения результатов текущей итерации
    run_name = f"yolo_apteka_{iteration}"
    run_path = os.path.join(base_path, run_name)

    # Запуск обучения
    results = model.train(
        data=data_path,
        epochs=750,
        save=True,
        save_period=-1,
        imgsz=640,
        optimizer=optimizer,
        lr0=lr,
        weight_decay=weight_decay,
        conf=conf,
        batch=batch,
        patience=200,
        augment=True,
        scale=True,
        mosaic=True,
        device=0,
        project=base_path,
        name=run_name
    )

    # Логируем метрики в Comet ML
    experiment.log_metrics({
        "mAP50": results.results_dict["metrics/mAP50(B)"],
        "mAP50-95": results.results_dict["metrics/mAP50-95(B)"],
        "precision": results.results_dict["metrics/precision(B)"],
        "recall": results.results_dict["metrics/recall(B)"]
    })

    # Логируем графики
    for plot_name in ["results.png", "confusion_matrix.png", "F1_curve.png", "P_curve.png", "R_curve.png"]:
        plot_path = os.path.join(run_path, plot_name)
        if os.path.exists(plot_path):
            experiment.log_image(plot_path, name=plot_name)

    # Логируем модель (веса)
    model_weights_path = os.path.join(run_path, "weights/best.pt")
    if os.path.exists(model_weights_path):
        experiment.log_model("YOLOv8_weights", model_weights_path)

    # Логируем результаты (например, текстовые файлы или логи)
    results_files = ["results.txt", "opt.yaml"]
    for file_name in results_files:
        file_path = os.path.join(run_path, file_name)
        if os.path.exists(file_path):
            experiment.log_asset(file_path, file_name)

    # Возврат пути к новым весам
    return model_weights_path

# Основной цикл для перебора параметров
for optimizer in optimizers:
    for lr in learning_rates:
        for weight_decay in weight_decays:
            for conf in conf_thresholds:
                for batch in batches:
                    # Создаем новый объект эксперимента Comet ML для каждой итерации
                    run_name = f"yolo_apteka_{iteration}"
                    experiment = Experiment(
                        api_key=os.getenv("COMET_API_KEY"),  # Используем переменную окружения
                        project_name=run_name,
                        workspace="lidiya-cutie" 
                    )

                    # Устанавливаем имя эксперимента
                    experiment.set_name(run_name)

                    # Логируем гиперпараметры
                    experiment.log_parameters({
                        "optimizer": optimizer,
                        "learning_rate": lr,
                        "weight_decay": weight_decay,
                        "conf_threshold": conf,
                        "batch_size": batch,
                        "iteration": iteration
                    })

                    # Обучение с текущими параметрами
                    weights_path = train_model(weights_path, optimizer, lr, weight_decay, conf, batch, iteration, experiment)
                    
                    # Завершаем текущий эксперимент
                    experiment.end()

                    iteration += 1  # Увеличиваем номер итерации
