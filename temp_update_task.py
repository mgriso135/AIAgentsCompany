
from backend.unified_api_client import UnifiedAPIClient
import json
from datetime import datetime

client = UnifiedAPIClient()
task_data = {
    'status': 'Done',
    'ai_notes': 'Analyzed the competitive landscape of AI-powered chatbots for customer service in the SME sector, focusing on competitors not in the `competitors.txt` list. Identified key players, their value propositions, pricing models, and target audiences. The report is saved in the task directory.',
    'real_end_date': datetime.now().isoformat()
}
response = client.update_task(task_id='47', task_data=task_data)
print(json.dumps(response, indent=2))
