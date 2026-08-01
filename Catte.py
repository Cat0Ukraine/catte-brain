import json
import os
import math

FILE_PATH = "brain.json"


def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "Кіт": ["жива істота", "тварина", "домашня тварина", "нявкає", "має хвіст", "чотири лапи"],
            "Собака": ["жива істота", "тварина", "домашня тварина", "гавкає", "має хвіст", "чотири лапи"],
            "Тигр": ["жива істота", "тварина", "дика тварина", "смугастий", "має хвіст", "чотири лапи"],
            "Смартфон": ["неживий предмет", "електронний пристрій", "має екран", "можна дзвонити", "поміщається в кишеню"],
            "Телевізор": ["неживий предмет", "електронний пристрій", "має екран", "стоїть у вітальні"],
            "Людина": ["жива істота", "розумна істота", "має дві ноги", "вміє розмовляти"],
        }


def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def best_question(candidates, data, asked):
    feature_counts = {}
    total = len(candidates)

    for name in candidates:
        for feature in data[name]:
            if feature in asked:
                continue
            feature_counts[feature] = feature_counts.get(feature, 0) + 1

    if not feature_counts:
        return None

    best_feature = None
    best_score = -1

    for feature, count in feature_counts.items():
        p_yes = count / total
        p_no = 1 - p_yes
        if p_yes == 0 or p_no == 0:
            entropy = 0
        else:
            entropy = -(p_yes * math.log2(p_yes) + p_no * math.log2(p_no))
        score = entropy
        if score > best_score:
            best_score = score
            best_feature = feature

    return best_feature


def filter_candidates(candidates, data, question, answer):
    if answer == "так":
        return [c for c in candidates if question in data[c]]
    else:
        return [c for c in candidates if question not in data[c]]


def play_round(data):
    candidates = list(data.keys())
    asked = []
    questions_path = []

    while True:
        if len(candidates) == 1:
            guess = candidates[0]
            ans = input(f"\nЦе {guess}? (так/ні): ").strip().lower()
            if ans == "так":
                print("Ура! Я переміг! Спробуй загадати когось складнішого.\n")
                return
            else:
                learn_new_character(data, questions_path)
                return

        if not candidates:
            print("\nЯ розгубився — жоден персонаж не підходить під твої відповіді.")
            learn_new_character(data, questions_path)
            return

        question = best_question(candidates, data, asked)

        if question is None:
            guess = candidates[0]
            ans = input(f"\nЦе {guess}? (так/ні): ").strip().lower()
            if ans == "так":
                print("Ура! Я переміг!\n")
                return
            else:
                learn_new_character(data, questions_path)
                return

        answer = input(f"\nВаш персонаж — {question}? (так/ні): ").strip().lower()
        asked.append(question)

        if answer == "так":
            questions_path.append(question)

        candidates = filter_candidates(candidates, data, question, answer)


def learn_new_character(data, questions_path):
    print("\nЕх... Я здаюся. Допоможи мені стати розумнішим!")
    character = input("Кого ти загадав?: ").strip()
    new_feature = input(f"Яка унікальна ознака відрізняє {character} від інших?: ").strip().lower()

    features = list(questions_path)
    if new_feature not in features:
        features.append(new_feature)

    data[character] = features
    save_data(data)
    print("Запам'ятав!")


def main():
    data = load_data()
    print("--- Гра Акінатор: Загадай персонажа! ---")
    while True:
        play_round(data)
        print("--- НОВА ГРА ---")


if __name__ == "__main__":
    main()