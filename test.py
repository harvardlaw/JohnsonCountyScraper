import unittest
import hashlib
import json
from scrape import *
from sql import testConnection

class TestParse(unittest.TestCase):
    def test_caseinfo(self):
        self.individual_parsers('charges.html','3b9d382ab012de42c57793748cbfba7f',parseCaseHeaderInformation)
    def test_chargeinfo(self):
        self.individual_parsers('charges.html','813df4651e6a23a76f0fdccbe4de842c',parseChargeInformation)
    def test_sentenceinfo(self):
        self.individual_parsers('charges.html','5cc54d0da74c27c72fc3c2709bb8d7bc',parseSentenceInfo)
    def test_casehistory(self):
        self.individual_parsers('casehistory.html','4ae929a183c3cbc97f68d20063ba1030',parseCaseHistory)
    def test_caledar(self):
        self.individual_parsers('calendar.html','224dd19f6ac1c85e8b6d48388e3783b9',parseCalendarHTML)
    def test_othercaes(self):
        self.individual_parsers('othercases.html','85d2eaf1420875aaf334dbdca131c0af',parseOtherCasesHTML)
    def test_accounting(self):
        self.individual_parsers('accounting.html','2a7af3585d28c29739b8e12db5ae9f74',parseAccountingHTML)
    def individual_parsers(self,htmlfile,hash,func):
        with open(htmlfile, 'r') as file:
            html = file.read().replace('\n', '')
        jsonresults = json.dumps(func(html))
        result = hashlib.md5(jsonresults.encode('utf-8'))
        self.assertEqual(result.hexdigest(),hash)

class TestScraper(unittest.TestCase):
    # Tests where the HTML hashes the same or they have changed the layout of their page
    # TODO: Need to add tests for the other pages. Right now we just look at the homepage and the first charge page.
    def test_homepage(self):
        # Test if the homepage is the same as development
        livehash = hashlib.md5(getCookiesandHTML()['HTML'].encode('utf-8')).hexdigest()
        self.assertEqual(livehash,'dcf7fc1d142c88c58a246cc448c39935')
    def test_chargepage(self):
        # Test if the homepage charge page for case 97CR00090 is the same
        cookiesandhtml = getCookiesandHTML()
        cookies = cookiesandhtml['Cookies']
        baseaspxheaders = parseASPXParameters(cookiesandhtml['HTML'])
        livehash = hashlib.md5(getChargeHTML(cookies,'97CR00090',baseaspxheaders).encode('utf-8')).hexdigest()
        self.assertEqual(livehash,'54ec1c591c0e3749f3e5bdd40d131cb3')

class TestSQL(unittest.TestCase):
    def testSQLCredentials(self):
        self.assertTrue(testConnection())
if __name__ == '__main__':
    unittest.main()