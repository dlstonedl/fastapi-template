import json
from datetime import datetime

from app.domain.entity.gender import Gender


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Gender):
            return obj.name
        return super().default(obj)