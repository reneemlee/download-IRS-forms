FIND THE FORMS CHALLENGE
DESCRIPTION:
This project allows you to look up information on IRS tax forms and download them.

-----

TOOLS USED:
I chose BeautifulSoup for its ease of use working with static websites.

-----

REFLECTION:
In addition to fulfilling the requirements, I added error handling for invalid form numbers and search years. I also incorporated doctests and unittests to verify my outputs.

Given more time, I'd like to add additional tests, including testing for given a range of valid years, my function will download all forms within that range, with the earliest form revision date matching the minimum year and latest matching the max year. I'd also add corresponding error messages if the begin/end years input fall outside of a form's revision dates.

-----

INSTALLATION:
To run FIND THE FORMS on your local machine, follow the instructions below(built using Python 3.9.6):

    Download ZIP and open scraper.py

    Create and activate a virtual environment inside your project directory:

        $ virtualenv env (Mac OS)
        $ virtualenv env --always-copy (Windows OS)
        $ source env/bin/activate
        
    Install the dependencies: 
        $ pip3 install -r requirements.txt

-----

HOW TO RUN:
In the command line:
    
    Run scraper.py interactively: 
        $ python3 -i scraper.py

    To return informational results, use the get_product_info function. It takes in a list of form names as argument and returns the exact match output as json in the same format as the given instructions:

    ** printing results to showcase formatting **
    ex: >>> print(get_product_info(["Form W-9","Form W-2"]))

    output:
        [
            {
                "form_number": "Form W-9",
                "form_title": "Request for Taxpayer Identification Number and Certification",
                "min_year": 1983,
                "max_year": 2018
            },
            {
                "form_number": "Form W-2",
                "form_title": "Wage and Tax Statement (Info Copy Only)",
                "min_year": 1954,
                "max_year": 2022
            }
        ]

    To download a given tax form from range of years, use download_forms function and pass in the form name in a string, the start year, then end year. The returned forms are an exact match and will be downloaded to a subdirectory named "downloads" under the script's main directory with the name of the form as "Form Name - Year":

    ex: >>> download_forms("Form W-2",2000,2005)

    output files:
        downloads/Form W-2 - 2000.pdf
        downloads/Form W-2 - 2001.pdf
        downloads/Form W-2 - 2002.pdf
        downloads/Form W-2 - 2003.pdf
        downloads/Form W-2 - 2004.pdf
        downloads/Form W-2 - 2005.pdf

-----
TESTS:
In command line:

    Run tests using:
        $ python3 test_scraper.py





