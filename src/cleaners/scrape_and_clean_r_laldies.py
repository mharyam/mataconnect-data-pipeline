import requests
import json
from bs4 import BeautifulSoup
import datetime


def fetch_rladies_chapters():
    # Read from local file instead of URL
    with open("../test.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Try multiple methods to get all rows
    # table = soup.find("table", class_="chp-table")
    table = soup.find("tbody")
    if not table:
        raise ValueError("Could not find table in the HTML")

    # Get ALL rows directly using CSS selector
    rows = table.select("tr")
    print(f"Found {len(rows)} total rows")

    chapters = []
    current_country = ""

    for row in rows:
        cells = row.find_all("td")
        print(f"Processing row with {len(cells)} cells")

        # Handle different row types
        if len(cells) == 3:
            country_cell, city_cell, social_cell = cells
            current_country = country_cell.get_text(strip=True)
            print(f"Found country row: {current_country}")
        elif len(cells) == 2:
            city_cell, social_cell = cells
            print(f"Found city row in {current_country}")
        else:
            print(f"Found row with {len(cells)} cells - skipping")
            continue

        # Extract data from the row
        city_name = city_cell.get_text(strip=True) if city_cell else ""
        link = city_cell.find("a") if city_cell else None
        meetup_url = link["href"] if link and link.has_attr("href") else None

        # Extract social links
        social_links = []
        if social_cell:
            for a in social_cell.find_all("a"):
                if a.has_attr("href"):
                    social_links.append(a["href"])

        chapter = {
            "country": current_country,
            "city": city_name,
            "meetup_url": meetup_url,
            "social_links": social_links,
        }
        chapters.append(chapter)
        print(f"Added chapter: {chapter}")  # Debug print

    print(f"Total chapters processed: {len(chapters)}")
    return chapters


def extract_contact_email(links):
    for link in links:
        if link.startswith("mailto:"):
            return link.replace("mailto:", "")
    return ""


def extract_social_links(links):
    social = {}
    for link in links:
        if "facebook.com" in link:
            social["facebook"] = link
        elif "twitter.com" in link:
            social["twitter"] = link
        elif "instagram.com" in link:
            social["instagram"] = link
        elif "github.com" in link:
            social["github"] = link
        elif "youtube.com" in link:
            social["youtube"] = link
        elif "meetup.com" in link:
            social["meetup"] = link
        elif "netlify.app" in link or "rladies" in link:
            social["website"] = link
    return social


def clean_chapter_data(chapter):
    """Clean and format chapter data."""
    now = datetime.datetime.utcnow().isoformat()
    city_name = chapter["city"].replace("R-Ladies ", "")
    schema = {
        "name": chapter["city"],
        "description": "A local chapter of R-Ladies Global, supporting and promoting gender diversity in the R programming community.",
        "website": chapter.get("meetup_url", ""),
        "tags": ["tech", "R", "data science", "gender diversity", "community"],
        "focus_areas": ["STEM", "Career Support", "Leadership", "Mentorship"],
        "country": chapter.get("country", ""),
        "city": city_name,
        "language": ["English"],  # default assumption
        "contact_email": extract_contact_email(chapter.get("social_links", [])),
        "is_virtual": True,
        "social_links": extract_social_links(chapter.get("social_links", [])),
        "community_info": {},
        "pricing_model": "free",
        "topics_supported": ["R Programming", "Data Science", "Machine Learning"],
        "audience_type": ["Students", "Professionals", "Researchers"],
        "event_types": ["Meetup", "Workshop", "Webinar"],
        "year_founded": None,
        "verified": False,
        "embedding": [],
        "data_source": "https://rladies.org/",
        "created_at": now,
        "updated_at": now,
        "last_verified_at": None,
    }
    return schema


# Example usage
if __name__ == "__main__":
    chapters = fetch_rladies_chapters()
    print(f"\nTotal chapters fetched: {len(chapters)}")

    cleaned_chapters = [clean_chapter_data(chap) for chap in chapters]
    with open("../../data/rladies_chapters.json", "w") as f:
        json.dump(cleaned_chapters, f, indent=4)

    print("Cleaned data saved to rladies_chapters_cleaned.json")
