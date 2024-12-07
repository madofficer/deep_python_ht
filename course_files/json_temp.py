import json
from datetime import datetime

def generate_crm_template(operation, entity, data):
    """
    CRM JSON-temp.

    :param operation: (create, read, update, delete).
    :param entity: (client, service, admin, visit, request_status).
    :param data: dict.
    :return: JSON-str.
    """
    template = {
        "operation": operation,
        "entity": entity,
        "data": data
    }
    return json.dumps(template, indent=4, ensure_ascii=False)


client_data = {
    "id": 12345,
    "name": "NameName",
    "phone": "+1234567890",
    "email": "ivan@example.com",
    "notes": "vip",
    "services": [
        {
            "service_id": 1,
            "name": "product",
            "status": "active",
        }
    ]
}

client_json = generate_crm_template("create", "client", client_data)
print(client_json)


status_data = {
    "client_id": 12345,
    "service_id": 1,
    "status": "completed"
}

status_json = generate_crm_template("update", "request_status", status_data)
print(status_json)
