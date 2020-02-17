import json


class Actions:
    def __init__(self, type, ):
        self.json_representation = {
            "type": type
        }

    def execute(self):
        pass

    def from_json(self):
        self.json_representation = json.loads(self.json_representation)
        return self.json_representation

    def to_json(self):
        self.json_representation = json.dumps(self.json_representation)
        return self.json_representation


"""
{
    "type": "Buy/Click/DoDmgOrWhatever",
    "buy" : item_id
}
"""
