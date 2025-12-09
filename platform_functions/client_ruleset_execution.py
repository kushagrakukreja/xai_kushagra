import os
import requests

from xpms_rules.models.rules import Ruleset


def client_ruleset_execution(**kwargs):
    client_name = kwargs.get("Client_Name")
    if not client_name:
        msg = "Please provide key Client_Name in payload"
        raise Exception(msg)

    agent_id = kwargs.get("config").get("context").get("agent_id")
    solution_id = kwargs.get("config").get("context").get("solution_id")

    ruleset_filter = {
        "agent_id": agent_id,
        "solution_id": solution_id
    }
    all_rulesets = Ruleset().get_ruleset(ruleset_filter=ruleset_filter)
    ruleset_list = [ruleset for ruleset in all_rulesets
                    if client_name in ruleset.get("ruleset_metadata", {}).get("Clients", "")]

    ruleset_ids = [ruleset_json.get("ruleset_id") for ruleset_json in ruleset_list]
    run_all_exclusions = kwargs.get("run_all_exclusions", False)
    execution_method = kwargs.get("execution_method", "Sequential")

    kwargs.pop("Client_Name")
    kwargs.pop("config")
    kwargs.update({
        "run_all_exclusions": run_all_exclusions,
        "ruleset_ids": ruleset_ids,
        "execution_method": execution_method,
    })
    inp_payload = {
        "data": {
            **kwargs
        },
        "solution_id": "sol31"
    }

    requests.post(f"http://{os.getenv('API_GATEWAY_URL')}/execute_ruleset", json=inp_payload)  # noqa: S113
