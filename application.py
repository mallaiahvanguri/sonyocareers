from collections import defaultdict

from openpyxl import Workbook

from web_scraping import get_all_tables


def calculate_winner_looser(data):
    # Group teams by year
    teams_by_year = defaultdict(list)
    for team in data:
        teams_by_year[team["Year"]].append(team)

    # Find teams with max and min wins for each year
    results = []
    for year, teams in teams_by_year.items():
        max_team = max(teams, key=lambda x: x["Wins"])
        min_team = min(teams, key=lambda x: x["Wins"])
        results.append(
            {
                "Year": year,
                "Winner": max_team["Team Name"],
                "Winner Num. of Wins": max_team["Wins"],
                "Loser": min_team["Team Name"],
                "Loser Num. of Wins": min_team["Wins"],
            }
        )

    return results


if __name__ == "__main__":
    # Fetch the data from the website
    total_pages = 24
    base_url = "https://www.scrapethissite.com/pages/forms/"

    records = get_all_tables(total_pages, base_url)

    results = calculate_winner_looser(records)

    # Create a workbook and select the active worksheet
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "NHL Stats 1990-2011"

    # Write the first sheet data
    headers1 = list(records[0].keys())
    ws1.append(headers1)
    for entry in records:
        ws1.append(list(entry.values()))

    # Create a second worksheet
    ws2 = wb.create_sheet(title="Winner and Loser per Year")

    # Write the second sheet data
    headers2 = list(results[0].keys())
    ws2.append(headers2)
    for entry in results:
        ws2.append(list(entry.values()))

    # Save the workbook
    wb.save("output.xlsx")
