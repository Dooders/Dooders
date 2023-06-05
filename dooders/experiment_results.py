import pandas as pd


def total_accuracy(inference_record):
    results = [a['accurate']
               for a in inference_record.values() if a['accurate'] is not None]
    true_count = sum(results)
    total_count = len(results)
    percentage = (true_count / total_count) * 100 if total_count > 0 else 0.0
    return percentage, total_count


def running_accuracy(inference_record):
    count_true = 0
    total = 0
    accuracies = []

    for value in inference_record.values():
        total += 1
        if value['accurate']:
            count_true += 1
        accuracies.append(count_true / total)

    return accuracies


def n_running_accuracy(inference_record, n=200):
    count_true = 0
    total = 0
    accuracies = []
    record_items = list(inference_record.items())

    for i, (_, value) in enumerate(record_items):
        total += 1
        if value['accurate']:
            count_true += 1
        if i >= n:
            oldest_item = record_items[i - n]
            if oldest_item[1]['accurate']:
                count_true -= 1
            total -= 1
        accuracies.append(count_true / total)

    return accuracies
