from xpms_rules.rule_service.utils import CustomOperatorParams

def line_amount_checker(config, input_obj: CustomOperatorParams):
    claim_obj = input_obj.l_val

    try:
        line_items = claim_obj.get("claim", {}).get("LINE_INFO", [])
        total_amount = sum(float(line.get("LINE_AMOUNT", 0)) for line in line_items)
    except Exception:
        return False

    if total_amount > 15000:
        return True
    return False