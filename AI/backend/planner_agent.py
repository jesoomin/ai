from search_agent import search
from booking_agent import book_trip

def plan_trip(query: str):
    results = search(query)
    if not results:
        return {"error": "검색 결과가 없습니다."}

    top = results[0]
    destination = top["metadata"]["location"]
    summary = top["page_content"]
    booking = book_trip(destination, "2025-12-01")

    return {
        "summary": summary,
        "destination": destination,
        "booking": booking
    }
