from xpms_rules.rule_service.utils import CustomActionParams
from jsonpath_ng import parse

def add_sum(config, action_obj: CustomActionParams):
    input_data = action_obj.input_object
    json_path = action_obj.scope.get("scope")
    lval = action_obj.scope.get("sub-scope")
    rval = action_obj.rval

    json_path_expr = parse(json_path)
    matches = [match.value for match in json_path_expr.find(input_data)]
    sum_amount = 0
    for match in matches[0]:
        if match.get(lval) is not None:
            sum_amount += match.get(lval)

    path_parts = rval.split('.')[1:]
    current = input_data

    for part in path_parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]

    current[path_parts[-1]] = sum_amount
