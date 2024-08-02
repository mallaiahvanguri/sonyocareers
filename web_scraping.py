import os

import requests
from bs4 import BeautifulSoup


def save_extracted_html(file_content, file_name):
    folder_path = "html_files"
    file_path = os.path.join(folder_path, file_name)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Write content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)


def get_table_data(base_url, page_number):
    url = f"{base_url}?page_num={page_number}"
    print(f"Scraping page {page_number}: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve. Status code: {response.status_code}")
        return []

    save_extracted_html(response.text, f"{page_number}.html")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table")
    rows = table.find_all("tr", class_="team")

    data = []
    for row in rows:
        ot_losses = row.find("td", class_="ot-losses").text.strip()
        team_data = {
            "Team Name": row.find("td", class_="name").text.strip(),
            "Year": row.find("td", class_="year").text.strip(),
            "Wins": int(row.find("td", class_="wins").text.strip()),
            "Losses": int(row.find("td", class_="losses").text.strip()),
            "OT Losses": int(ot_losses) if ot_losses != "" else 0,
            "Win %": float(row.find("td", class_="pct").text.strip()),
            "Goals For (GF)": int(row.find("td", class_="gf").text.strip()),
            "Goals Against (GA)": int(row.find("td", class_="ga").text.strip()),
            "+ / -": row.find("td", class_="diff").text.strip(),
        }
        data.append(team_data)

    return data


def get_all_tables(number_of_pages, base_url):
    all_data = []

    for page_number in range(1, number_of_pages + 1):
        page_data = get_table_data(base_url, page_number)
        all_data.extend(page_data)

    return all_data
