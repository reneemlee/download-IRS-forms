import doctest
from filecmp import cmp
import os
import requests
import unittest

import pinwheel as pw

class DownloadFormsTestCase(unittest.TestCase):

    def setUp(self):
        url = f"https://www.irs.gov/pub/irs-prior/fw2--2000.pdf"
        file = requests.get(url)
        file_name = "Form W-2 - 2000"

        with open(f"{file_name}.pdf", 'wb') as f:
            f.write(file.content) 

    def tearDown(self):
        os.remove("Form W-2 - 2000.pdf")
        os.remove("downloads/Form W-2 - 2000.pdf")
        try:
            os.rmdir("downloads")
        except:
            pass

    def test_download(self):
        pw.download_forms("Form W-2",2000,2000)
        f1 = "downloads/Form W-2 - 2000.pdf"
        f2 = "Form W-2 - 2000.pdf"
        comp = cmp(f1,f2)
        
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pw))
    return tests

if __name__ == "__main__":
    unittest.main()
