from bs4 import BeautifulSoup
import requests
import json

def get_product_info(forms):

    url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?"

    results_list = []
    
    for item in forms:
        params = { 'value': {item},
                    'criteria': 'formNumber',
                    'submitSearch': 'Find',
                    'resultsPerPage': 200,
                    'indexOfFirstRow': 0,
                    'sortColumn': 'sortOrder',
                    'isDescending':'false'
                }
        response = requests.get(url, params=params)

        soup = BeautifulSoup(response.text, "html.parser")   

        #html tag for the results
        containers = soup.find_all('tr', {"class": ["odd", "even"]})

        lst = []
        
        for container in containers:
            form_number = container.find('td', class_='LeftCellSpacer').text.strip()
            form_title = container.find('td', class_='MiddleCellSpacer').text.strip()
            year = container.find('td', class_='EndCellSpacer').text.strip()

            data = {'form_number': form_number,
                    'form_title' : form_title,
                    'year': int(year),
                    }
            #if form number matches search value, append the dic to results
            if item == data['form_number']:
                lst.append(data)
            
        #returns the min and max year of a form
        try:
            min_year = min(lst, key=lambda k : k['year'])
            max_year = max(lst, key=lambda k : k['year'])
            
            results = {'form_number': max_year['form_number'],
                        'form_title' : max_year['form_title'],
                        'min_year': min_year['year'],
                        'max_year': max_year['year']
                        }
            
            results_list.append(results)
        except:
            print(f'{item} does not exist. Please enter valid search')

    with open('results.json', 'w') as f:
        json.dump(results_list, f, indent=8, ensure_ascii=False)
    
    print("JSON file created")
        
        
        


    
    