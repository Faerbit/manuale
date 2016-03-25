import logging
import time

import dns.resolver
import dns.exception

from .inwx import domrobot
from .configuration import get_account_data

logger = logging.getLogger(__name__)

class InwxChallenge:

    def __init__(self, domain):
        self.domain = domain
        self._login()

    def __del__(self):
        if self.recordId:
            self._clean_challenge()

    def _login(self):
        api_url, username, password, shared_secret = get_account_data(
                print_errors = True, config_file="/etc/manuale.ini",
                config_section="live")
        self.api = domrobot(api_url, debug = False)
        self.api.account.login({"user": username, "pass": password})

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
        for i in range(20):
            if (self._has_dns_propagated(challenge) == False):
                logger.info("Try {:2d}/20 failed: DNS not propagated, waiting 30s...".format(i))
                time.sleep(30)
            else:
                break
        logger.info("DNS propagated.")

    def _clean_challenge(self):
        """Deletes challenge TXT record"""
        self.api.nameserver.deleteRecord({"id":self.recordId})
        logger.info("Deleted TXT record for {}".format(self.domain))

    def _has_dns_propagated(self, challenge):
        """Checks if the TXT record has propagated."""
        txt_records = []
        name = "_acme-challenge." + self.domain
        try:
            resolver = dns.resolver.Resolver()
            # INWX, google and ccc nameservers
            resolver.nameservers = ["217.70.142.66", "8.8.8.8", "213.73.91.35"]
            dns_response = resolver.query(name, 'TXT')
            for rdata in dns_response:
                for txt_record in rdata.strings:
                    txt_records.append(txt_record)
        except dns.exception.DNSException as error:
            return False

        for txt_record in txt_records:
            if txt_record == challenge:
                return True

        return False
