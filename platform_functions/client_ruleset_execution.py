import os
import uuid

import requests

from xpms_rules.models.rules import Ruleset
from xpms_rules.triggers.execute_rulesets import ExecuteRuleset
from xpms_common.utils import publish_mq_message


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

    from xpms_common.mq_endpoint import MQMessage

    msg = MQMessage()
    msg.solution_id = solution_id
    msg.agent_id = agent_id
    msg.data = inp_payload.get("data")
    msg.user_id = kwargs.get("config").get("context").get("user_id")
    msg.trigger = "execute_ruleset"
    msg.routing_key = "system.system.run_dag"
    msg.request_id = str(uuid.uuid4())
    msg.context = kwargs.get("config").get("context")

    handler = ExecuteRuleset(context=msg.context, message=msg.to_json())
    return handler.run()

