from bs4 import BeautifulSoup
import requests
import json
import os

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
        #TODO:do we need this? or can we just do find_all for the leftcellspacer etc.
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

def download_forms(form,beg,end):        
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

    soup = BeautifulSoup(response.text, "html.parser")   

    containers = soup.find_all('tr', {"class": ["odd", "even"]})

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
    
    current_dir = os.getcwd() 
    new_dir = f'{current_dir}/downloads'
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    for result in results:
        file_name = f"{result['form_number']} - {result['year']}" + ".pdf"
        file = requests.get(result['form_link'])

        with open(f"{new_dir}/{file_name}", 'wb') as f:
            f.write(file.content)    




