import dns
from .inwx import domrobot
from .configuration import get_account_data

class InwxChallenge:

    def __init__(self, domain):
        self.domain = domain
        self._login()

    def _login(self):
        api_url, username, password, shared_secret = get_account_data(
                print_errors = True, config_file="/etc/manuale.ini",
                config_section="live")
        self.api = domrobot(api_url, debug = False)
        self.api.login({"user", username, "pass", password})

    def deploy_challenge(self, challenge):
        """Creates challenge TXT record"""
        logger.info("Creating TXT record for {}".format(self.domain))
        tld = ".".join(self.domain.rsplit(".")[-2:])
        name = "_acme-challenge." + self.domain
        response = self.api.nameserver.createRecord({"domain": tld,
            "type": "TXT", "content": challenge, "name": name})
        self.recordId = response["resData"]["id"]
        logger.info("TXT record registered...")
        logger.info("Checking if DNS has propagated...")
        while(self._has_dns_propagated() == False):
            logger.info("DNS not propagated, waiting 30s...")
            time.sleep(30)
        logger.info("DNS propagated.")

    def clean_challenge(self):
        """Deletes challenge TXT record"""
        self.api.nameserver.deleteRecord({"id":self.recordId})
        logger.info("Deleted TXT record for {}".format(self.domain))

    def _has_dns_propagated(self):
        """Checks if the TXT record has propagated."""
        txt_records = []
        try:
            dns_response = dns.resolver.query(self.domain, 'TXT')
            for rdata in dns_response:
                for txt_record in rdata.strings:
                    txt_records.append(txt_record)
        except dns.exception.DNSException as error:
            return False

        for txt_record in txt_records:
            if txt_record == self.token:
                return True

        return False
