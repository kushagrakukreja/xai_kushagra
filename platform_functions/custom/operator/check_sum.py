from xpms_rules.utils import CustomOperatorParams
from jsonpath_ng import parse


def check_sum(config, input_obj: CustomOperatorParams):
    lval = input_obj.l_val
    rval = input_obj.r_val
    scope = input_obj.json_path
    input_data = input_obj.input_data

    # Assuming scope consists of a list of objects (cardinality - n)
    json_path_expr = parse(scope)
    matches = [match.value for match in json_path_expr.find(input_data)]
    sum_amount = 0
    for match in matches[0]:
        if match.get(lval) is not None:
            sum_amount += match.get(lval)

    if sum_amount >= rval:
        return True
    return False
