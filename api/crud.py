# crud.py

from sqlalchemy.orm import Session
from sqlalchemy import text, func
from . import models


def get_top_products(db: Session, limit: int = 10):
    """
    Finds the most frequently mentioned products by looking for capitalized words,
    while excluding a comprehensive list of common non-product words.
    """
    # A more extensive list of words to exclude
    stop_words = [
        # Days & Months
        'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY',
        'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY',
        'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER',
        # Common English Words
        'PRICE', 'CONTACT', 'PHONE', 'HELLO', 'ADDRESS', 'AVAILABLE', 'INFRONT',
        'TELEGRAM', 'CHANNEL', 'HTTPS', 'GROUP', 'LIMITED', 'MESSAGE', 'LOBELIA',
        # Locations & Common Names
        'MEDHANIALEM', 'ADDIS', 'ABABA', 'ETHIOPIA',
        # Other
        'TABLE', 'MACHINE', 'ROUND'
    ]

    # The query is updated to use UPPER() for case-insensitive filtering
    query = text(f"""
        SELECT
            word AS product,
            COUNT(*) AS mention_count
        FROM marts.fct_messages, unnest(regexp_split_to_array(message_text, '\\s+')) AS word
        WHERE 
            length(word) > 3 
            AND word ~ '^[A-Z]' 
            AND UPPER(word) NOT IN ({", ".join(f"'{w}'" for w in stop_words)})
        GROUP BY word
        ORDER BY mention_count DESC
        LIMIT :limit;
    """)

    result = db.execute(query, {'limit': limit}).fetchall()
    return result


def search_messages(db: Session, query: str):
    """
    Searches for messages containing a specific keyword (case-insensitive).
    """
    return db.query(models.Message)\
             .filter(models.Message.message_text.ilike(f"%{query}%"))\
             .order_by(models.Message.message_datetime.desc())\
             .limit(100)\
             .all()
