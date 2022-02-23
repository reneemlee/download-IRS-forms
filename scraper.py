import json
import os
import re
import requests

from bs4 import BeautifulSoup

YEAR_RE = re.compile(r".*([1-3][0-9]{3})")

def return_response_from_irs(form):
    """Request from IRS"""

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?"

    params = { 'value': form,
                'criteria': 'formNumber',
                'submitSearch': 'Find',
                'resultsPerPage': 200,
                'indexOfFirstRow': 0,
                'sortColumn': 'sortOrder',
                'isDescending':'false'
            }

    response = requests.get(url, params=params)

    response_txt = BeautifulSoup(response.text, "html.parser")   

    return response_txt

def get_product_info(forms):
    """Return information on list of forms
    
    >>> print(get_product_info(["Form W-4"]))
    [
        {
            "form_number": "Form W-4",
            "form_title": "Employee's Withholding Certificate",
            "min_year": 1990,
            "max_year": 2022
        }
    ]

    >>> print(get_product_info(["Form XYZ", "Form W-2"]))
    Form XYZ does not exist. Please enter valid search
    [
        {
            "form_number": "Form W-2",
            "form_title": "Wage and Tax Statement (Info Copy Only)",
            "min_year": 1954,
            "max_year": 2022
        }
    ]
    """
    
    results_list = []
    
    for form in forms:
        search_results = return_response_from_irs(form)

        containers = search_results.find_all('tr', {"class": ["odd", "even"]})

        matches = []
        
        for container in containers:
            form_number = container.find('td', class_='LeftCellSpacer').text.strip()
            form_title = container.find('td', class_='MiddleCellSpacer').text.strip()
            year = container.find('td', class_='EndCellSpacer').text.strip()

            data = {'form_number': form_number,
                    'form_title' : form_title,
                    'year': int(year),
                    }
            #if form number matches search value, append dict to results
            if form == data['form_number']:
                matches.append(data)
            
        #returns the min and max year of a form
        try:
            min_year = min(matches, key=lambda k : k['year'])
            max_year = max(matches, key=lambda k : k['year'])
            
            results = {'form_number': max_year['form_number'],
                        'form_title' : max_year['form_title'],
                        'min_year': min_year['year'],
                        'max_year': max_year['year']
                        }
            
            results_list.append(results)
        except:
            print(f'{form} does not exist. Please enter valid search')
        
    if results_list != []:
        results_json = json.dumps(results_list, indent=4)
        return results_json

def download_forms(form,beg,end):
    """Download available forms within a given range""" 

    check_beg = re.search(YEAR_RE,str(beg))
    check_end = re.search(YEAR_RE,str(end))

    if not check_beg and check_end:
         print("Please enter valid year range")
         quit()
         
    search_results = return_response_from_irs(form)       

    containers = search_results.find_all('tr', {"class": ["odd", "even"]})

    results = []
    
    for container in containers:
        form_number = container.find('td', class_='LeftCellSpacer').text.strip()
        form_link = container.find('a').get('href')
        form_title = container.find('td', class_='MiddleCellSpacer').text.strip()
        year = container.find('td', class_='EndCellSpacer').text.strip()

        data = {'form_number': form_number,
                'form_link': form_link,
                'form_title' : form_title,
                'year': int(year),
                }
    
        if form == data['form_number'] and data['year'] in range(beg,end+1):
            results.append(data)
    
    if results == []:
        print("Please enter valid form number")
    
    #create subdirectory
    current_dir = os.getcwd() 
    new_dir = f'{current_dir}/downloads'
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    for result in results:
        file_name = f"{result['form_number']} - {result['year']}" + ".pdf"
        file = requests.get(result['form_link'])

        with open(f"{new_dir}/{file_name}", 'wb') as f:
            f.write(file.content) 






