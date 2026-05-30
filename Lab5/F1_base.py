import json
import os

# Клас документа

class Document:
    def __init__(self, data: dict):
        if "id" not in data:
            raise ValueError("Документ обов'язково повинен містити ID.")
        self.data = data
        if "_history" not in self.data:
            self.data["_history"] = []

    def get_id(self):
        return self.data["id"]

    def add_history(self, field, old_val, new_val):
        self.data["_history"].append({
            "field": field,
            "old": old_val,
            "new": new_val
        })

    def __repr__(self):
        return json.dumps(self.data, indent=2, ensure_ascii=False)

# Клас колекції

class Collection:
    def __init__(self):
        self.documents = []

    def add(self, json_str: str):
        try:
            data = json.loads(json_str)
            if "id" in data and any(d.get_id() == data["id"] for d in self.documents):
                doc_id = data["id"]
                raise ValueError(f"Документ з ID {doc_id} вже існує.")

            doc = Document(data)
            self.documents.append(doc)
            return True
        except json.JSONDecodeError:
            raise ValueError("Некоректний формат JSON.")

    def delete(self, doc_id):
        initial_len = len(self.documents)
        self.documents = [d for d in self.documents if d.get_id() != doc_id]
        return len(self.documents) < initial_len

    def upd(self, doc_id, field, value):
        for doc in self.documents:
            if doc.get_id() == doc_id:
                keys = field.split(".")
                target = doc.data

                for k in keys[:-1]:
                    if k not in target or not isinstance(target[k], dict):
                        target[k] = {}
                    target = target[k]

                old_val = target.get(keys[-1], None)
                target[keys[-1]] = value

                doc.add_history(field, old_val, value)
                return True
        return False

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([doc.data for doc in self.documents], f, indent=2, ensure_ascii=False)

    def load(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError("Файл не знайдено.")
        with open(filename, "r", encoding="utf-8") as f:
            data_list = json.load(f)
            self.documents = [Document(d) for d in data_list]

# Клас запитів

class SearchTools:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_val(self, doc_data: dict, field_path: str):
        if field_path == "_history":
            return doc_data.get("_history", [])

        keys = field_path.split(".")
        value = doc_data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value

    def check_doc(self, doc: Document, field: str, op: str, value) -> bool:
        actual_val = self.get_val(doc.data, field)

        if op == "exists":
            val_bool = str(value).lower() == "true"
            return (actual_val is not None) == val_bool

        if actual_val is None:
            return False

        try:
            if op == "=":
                return actual_val == value
            elif op == ">":
                return actual_val > value
            elif op == "<":
                return actual_val < value
            elif op == ">=":
                return actual_val >= value
            elif op == "<=":
                return actual_val <= value
            elif op == "in":
                if isinstance(actual_val, list):
                    return value in actual_val
                return False
        except TypeError:
            return False

        return False

    def find(self, conditions: list, logic="and", sort_by=None, reverse=False):
        results = []
        for doc in self.collection.documents:
            if not conditions:
                results.append(doc)
                continue

            matches = [self.check_doc(doc, f, op, v) for f, op, v in conditions]

            if logic == "and" and all(matches):
                results.append(doc)
            elif logic == "or" and any(matches):
                results.append(doc)

        if sort_by:
            def get_sort_key(doc):
                val = self.get_val(doc.data, sort_by)
                if val is None:
                    return (1, "")
                return (0, val)

            try:
                results.sort(key=get_sort_key, reverse=reverse)
            except TypeError:
                results.sort(key=lambda d: (0, str(self.get_val(d.data, sort_by))), reverse=reverse)

        return results

    def aggregate(self, operation, field):
        values = []
        for doc in self.collection.documents:
            val = self.get_val(doc.data, field)
            if val is not None:
                if not isinstance(val, (int, float)):
                    raise TypeError(
                        f"Дія можлива лише для числових полів. Поле \"{field}\" має нечислове значення.")
                values.append(val)

        if not values:
            return 0

        if operation == "count":
            return len(values)
        elif operation == "sum":
            return sum(values)
        elif operation == "avg":
            return sum(values) / len(values)
        elif operation == "min":
            return min(values)
        elif operation == "max":
            return max(values)
        else:
            raise ValueError(f"Невідома операція агрегації: {operation}.")

    def group(self, field):
        groups = {}
        for doc in self.collection.documents:
            val = self.get_val(doc.data, field)
            val_key = str(val) if val is not None else "None"
            if val_key not in groups:
                groups[val_key] = 0
            groups[val_key] += 1
        return groups

# Консольне меню

def parse_value(val_str):
    if val_str.isdigit(): return int(val_str)
    try:
        return float(val_str)
    except ValueError:
        pass
    if val_str.lower() == "true": return True
    if val_str.lower() == "false": return False
    return val_str


def main():
    base = Collection()
    searcher = SearchTools(base)

    while True:
        print("\nКонсольне меню")
        print("1. Додати документ")
        print("2. Видалити документ")
        print("3. Оновити поле в документі")
        print("4. Знайти документи")
        print("5. Агрегація (count, sum, avg, min, max)")
        print("6. Групування")
        print("7. Зберегти базу у файл")
        print("8. Завантажити базу з файлу")
        print("0. Вийти")

        choice = input("Оберіть дію (0-8): ").strip()

        try:
            if choice == "0":
                print("Завершення роботи.")
                break

            elif choice == "1":
                json_str = input("Введіть JSON документа: ").strip()
                base.add(json_str)
                print("Документ успішно додано.")

            elif choice == "2":
                doc_id = parse_value(input("Введіть ID документа для видалення: ").strip())
                if base.delete(doc_id):
                    print(f"Документ з ID {doc_id} видалено.")
                else:
                    print("Документ не знайдено.")

            elif choice == "3":
                doc_id = parse_value(input("Введіть ID документа: ").strip())
                field = input("Введіть поле для оновлення: ").strip()
                value = parse_value(input("Введіть нове значення: ").strip())
                if base.upd(doc_id, field, value):
                    print("Оновлено.")
                else:
                    print("Документ не знайдено.")


            elif choice == "4":
                print("Вводьте умови по одній. Формат: поле оператор значення (наприклад, age > 20).")
                print("Щоб завершити введення умов, залиште порожнім і натисніть Enter.")
                conditions = []
                while True:
                    cond = input("Умова: ").strip()
                    if not cond:
                        break
                    parts = cond.split(maxsplit=2)
                    if len(parts) < 3:
                        print("Помилка формату. Спробуйте ще раз.")
                        continue
                    conditions.append((parts[0], parts[1], parse_value(parts[2])))

                logic = "and"
                if len(conditions) > 1:
                    while True:
                        logic = input("Умови виконуються водночас чи хоча б одна з?: ").strip().lower()
                        if logic in ["and", "or"]:
                            break
                        print("Некоректний ввід. Будь ласка, введіть and або or.")

                sort_by = input("Сортувати за полем (Enter щоб пропустити): ").strip()
                reverse = False
                if sort_by:
                    rev_input = input("Сортувати за спаданням(true) чи зростанням(false))?): ").strip().lower()
                    if rev_input == "true":
                        reverse = True

                results = searcher.find(conditions, logic, sort_by if sort_by else None, reverse)
                print(f"Знайдено документів: {len(results)}")
                for r in results:
                    print(r)

            elif choice == "5":
                op = input("Оберіть операцію (count, sum, avg, min, max): ").strip()
                field = input("Введіть поле для агрегації: ").strip()
                res = searcher.aggregate(op, field)
                print(f"Результат: {res}")

            elif choice == "6":
                field = input("Введіть поле для групування: ").strip()
                groups = searcher.group(field)
                print(f"Групування за \"{field}\":")
                for k, v in groups.items():
                    print(f"  {k}: {v} док.")

            elif choice == "7":
                filename = input("Введіть ім'я файлу: ").strip()
                base.save(filename)
                print(f"Базу збережено у {filename}.")

            elif choice == "8":
                filename = input("Введіть ім'я файлу для завантаження: ").strip()
                base.load(filename)
                print(f"Базу завантажено. Документів: {len(base.documents)}")

            else:
                print("Невідомий пункт меню. Спробуйте ще раз.")

        except Exception as e:
            print(f"Помилка: {e}")


if __name__ == "__main__":
    main()