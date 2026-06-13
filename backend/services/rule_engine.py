import json


class RuleEngine:
    def __init__(self, rule_file):
        with open(rule_file) as f:
            self.rules = json.load(f)

    def evaluate(self, event):
        alerts = []

        for rule in self.rules:
            if self._evaluate_rule(rule, event):
                alerts.append({
                    "rule_id": rule["id"],
                    "risk": rule["risk"],
                    "message": rule["message"]
                })

        return alerts

    def _evaluate_rule(self, rule, event):
        """
        Evaluates rule conditions safely without eval()
        """

        conditions = rule.get("conditions", [])
        logic = rule.get("logic", "AND")

        results = []

        for cond in conditions:
            field = cond["field"]
            op = cond["operator"]
            value = cond["value"]

            event_value = event.get(field)

            result = self._compare(event_value, op, value)
            results.append(result)

        if logic == "AND":
            return all(results)
        else:
            return any(results)

    def _compare(self, event_value, operator, value):
        """
        Safe comparison handler
        """

        try:
            if operator == ">":
                return event_value > value
            elif operator == "<":
                return event_value < value
            elif operator == ">=":
                return event_value >= value
            elif operator == "<=":
                return event_value <= value
            elif operator == "==":
                return event_value == value
            elif operator == "!=":
                return event_value != value
            elif operator == "in":
                return event_value in value
            elif operator == "not_in":
                return event_value not in value
            else:
                return False
        except:
            return False