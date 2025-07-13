# Placeholder for test_data_processing.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils.db_connection import get_db_connection
from utils.logger import get_logger

logger = get_logger("TestDataProcessing")

def get_sheet_url(match_id):
    """
    tb_sheeturls 테이블에서 주어진 match_id에 해당하는 기록지 URL을 조회합니다.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT sheet_url FROM tb_sheeturls WHERE match_id = %s"
        cursor.execute(query, (match_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            logger.error(f"No sheet URL found for match_id={match_id}")
            return None
    except Exception as e:
        logger.error(f"Error fetching sheet URL: {e}")
    finally:
        cursor.close()
        conn.close()

def load_google_sheet(sheet_url):
    """
    Google Sheets 데이터를 가져옵니다.
    """
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'config/quiet-amp-275114-083a1f3b2f00.json',
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url).sheet1  # 첫 번째 시트
        all_data = sheet.get_all_values()
        return all_data[3:]  # 4행부터 데이터 반환
    except Exception as e:
        logger.error(f"Error loading Google Sheet: {e}")
        raise

def process_attendance_data(data, match_id):
    """
    출석 데이터를 tb_team_players에 저장합니다.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 기존 데이터 삭제
        delete_query = "DELETE FROM tb_team_players WHERE match_id = %s"
        cursor.execute(delete_query, (match_id,))
        conn.commit()

        for row in data:
            team_name = row[20].strip()  # U열
            player_name = row[21].strip()  # V열

            if not team_name:  # U열(팀명)이 빈 값인 경우 종료
                logger.warning("Team name is empty. Stopping attendance processing.")
                break

            if not player_name:  # Player 이름이 빈 값인 경우 건너뛰기
                logger.warning("Player name is empty. Skipping...")
                continue

            query_player_id = "SELECT id FROM tb_players WHERE name = %s"
            cursor.execute(query_player_id, (player_name,))
            player_id = cursor.fetchone()

            if player_id:
                query = """
                INSERT INTO tb_team_players (match_id, team_name, player_id, created_at, updated_at)
                VALUES (%s, %s, %s, NOW(), NOW())
                """
                cursor.execute(query, (match_id, team_name, player_id[0]))
            else:
                logger.error(f"Player '{player_name}' not found in tb_players. Skipping...")
        conn.commit()
        logger.info("Attendance data processed successfully.")
    except Exception as e:
        logger.error(f"Error processing attendance data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def process_game_data(data, match_id):
    """
    게임 데이터를 tb_games에 저장합니다.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 기존 데이터 삭제
        delete_query = "DELETE FROM tb_games WHERE match_id = %s"
        cursor.execute(delete_query, (match_id,))
        conn.commit()

        for row in data:
            if not row[2] or row[2] == "-":  # C열이 Null or '-'
                break
            gameno = int(row[0])  # A열
            home_team_name = row[1]  # B열
            home_score = int(row[2])  # C열
            home_keeper_name = row[4]  # E열
            away_team_name = row[5]  # F열
            away_score = int(row[6])  # G열
            away_keeper_name = row[8]  # I열

            # Keeper player_id 조회
            def get_player_id(name):
                query_player_id = "SELECT id FROM tb_players WHERE name = %s"
                cursor.execute(query_player_id, (name,))
                result = cursor.fetchone()
                return result[0] if result else None

            home_keeper = get_player_id(home_keeper_name)
            away_keeper = get_player_id(away_keeper_name)

            query = """
            INSERT INTO tb_games (match_id, gameno, home_team_name, home_score, home_keeper,
                                  away_team_name, away_score, away_keeper, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            cursor.execute(query, (match_id, gameno, home_team_name, home_score, home_keeper,
                                   away_team_name, away_score, away_keeper))
        conn.commit()
        logger.info("Game data processed successfully.")
    except Exception as e:
        logger.error(f"Error processing game data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def process_goal_details(data, match_id):
    """
    골/어시스트 데이터를 tb_goal_details에 저장합니다.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for row in data:
            if not row[2] or row[2] == "-":  # C열이 Null or '-'
                break
            gameno = int(row[0])  # A열
            query_game_id = "SELECT id FROM tb_games WHERE match_id = %s AND gameno = %s"
            cursor.execute(query_game_id, (match_id, gameno))
            game_id_result = cursor.fetchone()

            if not game_id_result:
                logger.error(f"Game not found for match_id={match_id}, gameno={gameno}. Skipping...")
                continue

            game_id = game_id_result[0]

            # K-P 열 골/어시스트 데이터 처리 (2열씩 반복)
            for col in range(10, 16, 2):  # K(10), M(12), O(14)
                scorer_name = row[col].strip() if row[col] else None  # 골을 기록한 선수 이름
                assist_name = row[col + 1].strip() if row[col + 1] else None  # 어시스트 선수 이름 (없을 수도 있음)
                own_goal = False

                # 공백 선수 이름 처리 (정상적인 경우)
                if not scorer_name:
                    logger.info("Scorer name is empty. Skipping...")
                    continue

                # 자살골 여부 처리
                if scorer_name.endswith("(ㅇ)") or scorer_name.endswith("(0)"):
                    scorer_name = scorer_name[:-3]  # "(ㅇ)" 또는 "(0)" 제거
                    own_goal = True

                # 선수 ID 조회
                def get_player_id(name):
                    query_player_id = "SELECT id FROM tb_players WHERE name = %s"
                    cursor.execute(query_player_id, (name,))
                    result = cursor.fetchone()
                    return result[0] if result else None

                scorer_id = get_player_id(scorer_name)
                assist_id = get_player_id(assist_name) if assist_name else None

                if not scorer_id:
                    logger.error(f"Scorer '{scorer_name}' not found in tb_players. Skipping...")
                    continue

                # 데이터 삽입
                query = """
                INSERT INTO tb_goal_details (game_id, scorer_id, assist_id, own_goal, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """
                cursor.execute(query, (game_id, scorer_id, assist_id, own_goal))
        conn.commit()
        logger.info("Goal details processed successfully.")
    except Exception as e:
        logger.error(f"Error processing goal details: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def process_matches_in_batches(start_id, end_id, batch_size=10):
    """
    match_id를 10개씩 묶어 데이터를 처리.
    :param start_id: 시작 match_id
    :param end_id: 끝 match_id
    :param batch_size: 한 번에 처리할 match_id의 개수
    """
    current_id = start_id
    failed_matches = []  # 에러난 match_id를 기록
    while current_id <= end_id:
        batch_ids = list(range(current_id, min(current_id + batch_size, end_id + 1)))
        logger.info(f"Processing batch: {batch_ids}")
        
        for match_id in batch_ids:
            try:
                sheet_url = get_sheet_url(match_id)
                if sheet_url:
                    sheet_data = load_google_sheet(sheet_url)
                    process_attendance_data(sheet_data, match_id)
                    process_game_data(sheet_data, match_id)
                    process_goal_details(sheet_data, match_id)
                else:
                    logger.error(f"No sheet URL found for match_id={match_id}")
                    failed_matches.append(match_id)
            except Exception as e:
                logger.error(f"Error processing match_id={match_id}: {e}")
                failed_matches.append(match_id)
        
        current_id += batch_size

    if failed_matches:
        logger.warning(f"Failed matches: {failed_matches}")
        with open("failed_matches.log", "w") as log_file:
            log_file.write("\n".join(map(str, failed_matches)))
    else:
        logger.info("All matches processed successfully.")

def retry_failed_matches(log_file="failed_matches.log"):
    """
    에러난 match_id를 개별적으로 처리.
    :param log_file: 실패한 match_id가 기록된 로그 파일
    """
    try:
        with open(log_file, "r") as file:
            failed_matches = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        logger.error(f"Log file {log_file} not found. Nothing to retry.")
        return

    for match_id in failed_matches:
        try:
            logger.info(f"Retrying match_id={match_id}")
            sheet_url = get_sheet_url(match_id)
            if sheet_url:
                sheet_data = load_google_sheet(sheet_url)
                process_attendance_data(sheet_data, match_id)
                process_game_data(sheet_data, match_id)
                process_goal_details(sheet_data, match_id)
            else:
                logger.error(f"No sheet URL found for match_id={match_id}")
        except Exception as e:
            logger.error(f"Error retrying match_id={match_id}: {e}")

#if __name__ == "__main__":
#    process_matches_in_batches(start_id=4, end_id=65, batch_size=5)

## 개발 match 재수행
if __name__ == "__main__":
    retry_failed_matches()

# if __name__ == "__main__":
#     match_id = 3  # 테스트를 위한 match_id
#     sheet_url = get_sheet_url(match_id)
#     if sheet_url:
#         sheet_data = load_google_sheet(sheet_url)
#         process_attendance_data(sheet_data, match_id)
#         process_game_data(sheet_data, match_id)
#         process_goal_details(sheet_data, match_id)  # 골/어시스트 데이터 처리 추가
#     else:
#         logger.error("No valid sheet URL found. Exiting...")

