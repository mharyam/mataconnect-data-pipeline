import json
from datetime import datetime


def clean_organization_data(data):
    # Map field names directly
    output = {
        "name": data.get("organizationname"),
        "description": data.get("description"),
        "website": data.get("url"),
        "tags": [],
        "focus_areas": [],
        "country": "US",
        "city": data.get("city", ""),
        "language": ["English"],
        "contact_email": "",
        "is_virtual": False,
        "social_links": {},
        "community_info": {},
        "pricing_model": "free",
        "topics_supported": [],
        "audience_type": [],
        "event_types": [],
        "year_founded": None,
        "verified": False,
        "embedding": [],
        "data_source": "https://data.cityofnewyork.us/resource/pqg4-dm6b.json",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "last_verified_at": None,
    }

    # Tags: convert fields with value 'Y' to readable tag names
    tag_fields = {
        "aging": "aging",
        "anti_discrimination_human_rights": "human rights",
        "arts_culture": "arts & culture",
        "business": "business",
        "child_care_parent_information": "child care",
        "community_service_volunteerism": "community service",
        "counseling_support_groups": "counseling",
        "disabilities": "disabilities",
        "domestic_violence": "domestic violence",
        "education": "education",
        "employment_job_training": "job training",
        "health": "health",
        "homelessness": "homelessness",
        "housing": "housing",
        "immigration": "immigration",
        "legal_services": "legal services",
        "lesbian_gay_bisexual_and_or_transgender": "LGBTQ+",
        "personal_finance_financial_education": "financial education",
        "professional_association": "professional association",
        "veterans_military_families": "veterans",
        "victim_services": "victim services",
        "youth_services": "youth services",
        "faith_based_organization": "faith-based",
        "foundation": "foundation",
    }

    for field, tag_name in tag_fields.items():
        if data.get(field, "").upper() == "Y":
            output["tags"].append(tag_name)

    return output


with open("../dirty_data/NYC_Women_s_Resource_Network_Database.json", "r") as f:
    raw_data_list = json.load(f)

cleaned = [clean_organization_data(raw_data) for raw_data in raw_data_list]


with open("../data/NYC_Women_Resource_Network_Database.json", "w") as f:
    json.dump(cleaned, f, indent=4)
print(f"Cleaned {len(cleaned)} organizations.")
# Save the cleaned data to a new file
