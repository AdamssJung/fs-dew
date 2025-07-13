# Placeholder for process_attendance.py
from utils.db_connection import get_db_connection
from utils.logger import get_logger

logger = get_logger("ProcessAttendance")

def insert_attendance(match_id, player_id, is_present, games_played_count):
    """
    선수의 출석 및 참여 데이터를 `tb_player_attendance` 테이블에 삽입합니다.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO tb_player_attendance (match_id, player_id, is_present, games_played_count, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (match_id, player_id)
        DO UPDATE SET 
            is_present = EXCLUDED.is_present,
            games_played_count = EXCLUDED.games_played_count,
            updated_at = NOW()
        """
        cursor.execute(query, (match_id, player_id, is_present, games_played_count))
        conn.commit()
        logger.info(f"Attendance data inserted/updated for player_id={player_id}, match_id={match_id}")
    except Exception as e:
        logger.error(f"Error inserting/updating attendance data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def process_attendance_data(attendance_records):
    """
    주어진 출석 데이터를 처리합니다.
    :param attendance_records: 출석 데이터 목록. 각 데이터는 딕셔너리 형식으로 제공됩니다.
        예: [{"match_id": 1, "player_id": 2, "is_present": True, "games_played_count": 2}, ...]
    """
    for record in attendance_records:
        try:
            insert_attendance(
                match_id=record["match_id"],
                player_id=record["player_id"],
                is_present=record["is_present"],
                games_played_count=record["games_played_count"],
            )
        except KeyError as e:
            logger.error(f"Missing required field in attendance record: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    # Replace this with actual data from a Google Sheet or other data source
    example_data = [
        {"match_id": 1, "player_id": 2, "is_present": True, "games_played_count": 2},
        {"match_id": 1, "player_id": 3, "is_present": False, "games_played_count": 0},
        {"match_id": 2, "player_id": 4, "is_present": True, "games_played_count": 3},
    ]
    process_attendance_data(example_data)
