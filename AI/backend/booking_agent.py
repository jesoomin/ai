def book_trip(destination: str, date: str):
    """더미 예약 정보 생성"""
    return {
        "destination": destination,
        "date": date,
        "hotel": f"{destination} 호텔 3박 예약 완료",
        "flight": f"{destination}행 항공권 예약 완료",
        "status": "예약 완료"
    }
