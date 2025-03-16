import os
import re
import pandas as pd
from datetime import datetime
import sys

def parse_training_block(block, log_file_path):
    """Функция для извлечения данных из одного блока лога"""
    date_match = re.search(r"wait_output_(\d+-\d+-\d+_\d+-\d+-\d+)\.log", log_file_path)
    date_time = datetime.strptime(date_match.group(1), "%Y-%m-%d_%H-%M-%S") if date_match else None

    project_path_match = re.search(r"Logging results to (.+?)[\s\n]", block)
    project_path = project_path_match.group(1) if project_path_match else None

    epochs_match = re.search(r"epochs=(\d+)", block)
    epochs = int(epochs_match.group(1)) if epochs_match else None

    patience_match = re.search(r"patience=(\d+)", block)
    patience = int(patience_match.group(1)) if patience_match else None

    batch_match = re.search(r"batch=(-?\d+)", block)
    batch = int(batch_match.group(1)) if batch_match else None
    if batch == -1:  
        autobatch_match = re.search(r"AutoBatch: Using batch-size (\d+)", block)
        batch = int(autobatch_match.group(1)) if autobatch_match else None

    imgsz_match = re.search(r"imgsz=(\d+)", block)
    imgsz = int(imgsz_match.group(1)) if imgsz_match else None

    optimizer_match = re.search(r"optimizer=(\w+)", block)
    optimizer = optimizer_match.group(1) if optimizer_match else None

    lr_match = re.search(r"lr0=([\d.]+)", block)
    lr = float(lr_match.group(1)) if lr_match else None

    conf_match = re.search(r"conf=([\d.]+)", block)
    conf = float(conf_match.group(1)) if conf_match else None

    best_weights_match = re.search(r"Optimizer stripped from (.+/weights/best\.pt)", block)
    best_weights = best_weights_match.group(1) if best_weights_match else None

    metrics_match = re.search(
        r"all\s+\d+\s+\d+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", block
    )
    precision = float(metrics_match.group(1)) if metrics_match else None
    recall = float(metrics_match.group(2)) if metrics_match else None
    map50 = float(metrics_match.group(3)) if metrics_match else None
    map50_95 = float(metrics_match.group(4)) if metrics_match else None

    return {
        "date": date_time,
        "name": project_path, 
        "weights path": best_weights,
        "epochs": epochs,
        "patience": patience,
        "batch": batch,
        "imgsz": imgsz,
        "optimizer": optimizer,
        "learning rate (lr)": lr,
        "confidence (conf)": conf,
        "precision (P)": precision,
        "recall (R)": recall,
        "mAP50": map50,
        "mAP50-95": map50_95,
    }

def parse_log_file(log_file_path):
    with open(log_file_path, "r", encoding="utf-8") as file:
        log_data = file.read()

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    log_data = ansi_escape.sub('', log_data)

    if "Запуск обучения с параметрами:" in log_data:
        training_blocks = log_data.split("Запуск обучения с параметрами:")
        return [parse_training_block(block, log_file_path) for block in training_blocks[1:]]
    else:
        return [parse_training_block(log_data, log_file_path)]

def save_to_excel(data, output_excel_path):
    if os.path.exists(output_excel_path):
        existing_data = pd.read_excel(output_excel_path)
        new_data = pd.DataFrame(data)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True).drop_duplicates(subset=["date", "name", "weights path"])
    else:
        combined_data = pd.DataFrame(data)

    combined_data.to_excel(output_excel_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ошибка: Необходимо указать путь к лог-файлу.")
        sys.exit(1)

    log_file_path = sys.argv[1]
    output_excel_path = "/mldata/results_summary.xlsx" # В вашем случае путь будет отличаться

    training_data = parse_log_file(log_file_path)
    save_to_excel(training_data, output_excel_path)
    print(f"Результаты добавлены в {output_excel_path}.")
