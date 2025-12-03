import json


def sendemail(
    failed_task_input=None,
    failed_task_output=None,
    failed_execution_details=None,
    execution_variables=None,
    config=None,
    **kwargs,
):
    """
    ENSO failure notification function.

    This function is invoked when a task in the pipeline fails.
    It receives details about the failure and returns a payload
    that can be used by a downstream email / notification task.
    """

    failed_task_input = failed_task_input or {}
    failed_task_output = failed_task_output or {}
    failed_execution_details = failed_execution_details or {}
    execution_variables = execution_variables or {}
    config = config or {}

    # Extract error details
    error_details = failed_task_output.get("error_details", {})
    error_messages = error_details.get("error", [])
    execution_id = error_details.get("execution_id") or failed_execution_details.get(
        "execution_id"
    )

    # Extract basic document info from failed_task_input
    document_id = None
    solution_id = None
    file_name = None

    documents = failed_task_input.get("document") or []
    if documents:
        first_doc = documents[0]
        document_id = first_doc.get("doc_id")
        solution_id = first_doc.get("solution_id")
        file_name = (
            first_doc.get("metadata", {})
            .get("properties", {})
            .get("filename")
        )

    # Extract run metadata from execution_variables
    mq_state_value = execution_variables.get("mq_state", {}).get("value", {})
    run_name = mq_state_value.get("run_name")
    ref_id = mq_state_value.get("ref_id")

    subject = f"[ENSO] Pipeline failure for run {run_name or execution_id}"

    body_dict = {
        "message": "A pipeline execution has failed.",
        "execution_id": execution_id,
        "run_name": run_name,
        "ref_id": ref_id,
        "solution_id": solution_id,
        "document_id": document_id,
        "file_name": file_name,
        "error_messages": error_messages,
        "failed_execution_details": failed_execution_details,
    }

    # For ENSO, returning a JSON-serializable payload is usually enough.
    # A downstream task can pick this up and actually send the email.
    return {
        "subject": subject,
        "body": body_dict,
    }


if __name__ == "__main__":
    """
    Simple local test harness.

    You can pipe a JSON blob (similar to the ENSO failed_task_input structure)
    into this script to see the generated payload, for example:

        python sendemail.py < sample_input.json
    """
    import sys

    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("No input provided on stdin")

        data = json.loads(raw)
        result = sendemail(**data)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))