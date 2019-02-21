import json

from core.models import TokenRuleChainModel, TokenRuleModel


class TokenRuleChain(TokenRuleChainModel):
    class Meta:
        proxy = True

    def add_rule(self, rule):
        self.token_rules.add(rule)

    def validate_chain(self):
        token_rules_list = list(self.token_rules.all().order_by('from_scrapes_count'))

        if len(token_rules_list) == 0:
            rule = TokenRuleModel()
            rule.save()
            self.token_rules.add(rule)
            return True

        first = token_rules_list[0]
        last = token_rules_list[-1]

        if first.from_scrapes_count != 0:
            return False
        if last.to_scrapes_count != -1:
            return False

        end = first.to_scrapes_count
        for rule in token_rules_list[1:]:
            if rule.from_scrapes_count != end + 1:
                return False
            end = rule.to_scrapes_count
        return True

    def receive_token(self, total_scrapes):
        rule = self.get_rule(total_scrapes)
        scrapes_num = total_scrapes - rule.from_scrapes_count
        return scrapes_num % rule.scrapes_per_token == 0

    def get_rule(self, scrapes_count):
        rules_query = self.get_rules_chain().filter(from_scrapes_count__lte=scrapes_count,
                                              to_scrapes_count__gte=scrapes_count)
        if not rules_query.exists():
            rule = list(self.token_rules.all().order_by('from_scrapes_count'))[-1]
        else:
            rule = rules_query[0]

        return rule

    def get_rules_chain(self):
        if self.token_rules.all().count() == 0:
            rule = TokenRuleModel(from_scrapes_count=0, to_scrapes_count=-1, scrapes_per_token=10)
            rule.save()
            self.token_rules.add(rule)
        return self.token_rules.all().order_by('from_scrapes_count')

    def __str__(self):
        token_rules_list = []
        for rule in self.get_rules_chain():
            rule_json = {}
            rule_json['from'] = rule.from_scrapes_count
            if rule.to_scrapes_count == -1:
                rule_json['to'] = 'infinite'
            else:
                rule_json['to'] = rule.to_scrapes_count

            rule_json['rate'] = rule.scrapes_per_token

            token_rules_list.append(rule_json)

        return json.dumps(token_rules_list)
