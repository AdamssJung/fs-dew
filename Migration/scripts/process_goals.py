# Placeholder for process_goals.py
from utils.db_connection import get_db_connection
from utils.logger import get_logger

logger = get_logger("ProcessGoals")

def insert_goal_data(game_id, scorer_id, assist_id, team_id, own_goal):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO tb_goal_details (game_id, scorer_id, assist_id, team_id, own_goal)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (game_id, scorer_id, assist_id, team_id, own_goal))
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting goal data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    insert_goal_data(1, 2, 3, 4, False)
