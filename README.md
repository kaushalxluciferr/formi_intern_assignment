# BBQ Nation Assignment
# kaushal Kishor Rauniyar
# 22054382
# 22054382@kiit.ac.in

# Explanation
This project is a FastAPI-based backend API that serves information about BBQ Nation branches, menus, offers, and other relevant data. It supports querying by city, branch, and categories like menu, timings, booking instructions, etc.

## Features
-> Get a list of available properties (cities)
-> Fetch branch details by name
-> Fetch all branches in a city (e.g., Delhi, Bangalore)
-> Query knowledge base by category or property
-> Support for normalized city names (e.g., "New Delhi" resolves to "Delhi")
-> Menu data integrated via JSON files
-> Token length management for response trimming

## Project Structure

```
├── app/
│   ├── api/
│   │   └── knowledge\_base.py        # Main API logic
│   ├── core/
│   │   └── config.py                # Configuration settings
│   ├── utils/
│   │   └── token\_manager.py         # Response truncation helper
├── data/
│   ├── delhi.json                   # Branch data for Delhi
│   ├── bangalore.json               # Branch data for Bangalore
│   ├── menu\_list.json              # Food menu items
│   ├── menu\_drink.json             # Drinks menu
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Project dependencies
└── README.md
```

## Setup Instructions

1. Clone the repository:

   bash
   ```
   git clone [https://github.com/gracygulati7/formi_intern_assignment.git](https://github.com/gracygulati7/formi_intern_assignment.git)
   cd formi_intern_assignment
   ```

3. Create a virtual environment:

   bash
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. Install dependencies:

   bash
   ```
   pip install -r requirements.txt
   ```

7. Create your environment config in app/core/config.py or via .env:

   Example:

   python
   KNOWLEDGE\_BASE\_PATH = "./data"

8. Run the FastAPI app:

   bash
   uvicorn main\:app --reload

## API Endpoints

| Endpoint                 | Method | Description                               |
| ------------------------ | ------ | ----------------------------------------- |
| /properties              | GET    | List available cities                     |
| /cities/{city\_name}     | GET    | Get all branch data in a city             |
| /branches/{branch\_name} | GET    | Get detailed info about a specific branch |
| /query                   | POST   | Query menu, booking, or property info     |
| /categories              | GET    | Available query categories                |

## Query Example

POST /query

Request:

json
{
"text": "What's on the menu?",
"category": "menu",
"property": "Delhi"
}

Response:

json
{
"content": "Lunch Buffet: Paneer Tikka, Chicken Wings, ...",
"source": "knowledge\_base",
"confidence": 0.9,
"tokens": 46
}

## Notes

* The API supports normalization of city names like "new delhi" → "Delhi"
* Branch data is loaded from the data directory at startup
* For large content (e.g., menus), responses are automatically truncated if tokens exceed a limit

