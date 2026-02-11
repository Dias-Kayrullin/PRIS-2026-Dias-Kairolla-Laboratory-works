import json
import os

# Определяем путь к rules.json относительно проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'rules.json')

def load_rules():
    if not os.path.exists(RULES_PATH):
        raise FileNotFoundError(f"Файл правил не найден: {RULES_PATH}")
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_receipt_rules(receipt_data):
    """
    Проверяет данные чека по правилам из JSON.
    Возвращает строку-вердикт.
    """
    rules = load_rules()
    
    # 1. Критические (HARD) проверки — сразу отказ
    if rules["critical_rules"]["block_alcohol"] and receipt_data["has_alcohol"]:
        return "⛔️ Критический отказ: Обнаружен алкоголь — покупка заблокирована"
    
    if rules["critical_rules"]["require_total_amount"] and receipt_data["total_amount"] <= 0:
        return "⛔️ Критический отказ: Сумма чека некорректна (≤ 0)"

    # 2. Проверка числовых порогов
    if receipt_data["total_amount"] < rules["thresholds"]["min_total_amount"]:
        return f"❌ Отказ: Сумма слишком маленькая ({receipt_data['total_amount']} < {rules['thresholds']['min_total_amount']})"
    
    if receipt_data["total_amount"] > rules["thresholds"]["max_total_amount_daily"]:
        return f"⚠️ Предупреждение: Сумма превышает дневной лимит ({receipt_data['total_amount']} > {rules['thresholds']['max_total_amount_daily']})"

    # 3. Проверка тегов (blacklist)
    for tag in receipt_data["tags"]:
        if tag.lower() in [t.lower() for t in rules["lists"]["prohibited_tags"]]:
            return f"⚠️ Предупреждение: Обнаружен запрещённый тег — {tag}"

    # 4. Всё прошло — успех
    return f"✅ Чек принят. Категория: {receipt_data['category_text']}, Сумма: {receipt_data['total_amount']}"
