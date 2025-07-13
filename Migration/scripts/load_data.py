import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils.db_connection import get_db_connection
from utils.logger import get_logger

logger = get_logger("LoadData")

def load_google_sheet(sheet_id):
    """
    Google 스프레드시트에서 데이터를 읽어옵니다.
    첫 번째 시트의 4행부터 데이터를 반환합니다.
    :param sheet_id: Google 스프레드시트 ID
    :return: 스프레드시트의 데이터 (리스트)
    """
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'config/quiet-amp-275114-083a1f3b2f00.json', 
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id).sheet1  # 첫 번째 시트
        all_data = sheet.get_all_values()
        # 4행부터 데이터 검토
        return all_data[3:]
    except Exception as e:
        logger.error(f"Error loading Google Sheet: {e}")
        raise

def process_sheet_data(data):
    """
    Google 스프레드시트 데이터를 처리합니다.
    :param data: 스프레드시트 데이터 (리스트 형식)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for row in data:
            # 예제: 행에서 필요한 데이터를 추출하여 처리
            match_id = row[0]  # match_id 예시 (필요에 맞게 수정)
            player_id = row[1]  # player_id 예시
            goals = int(row[2])  # 골 예시
            assists = int(row[3])  # 어시스트 예시

            # 데이터베이스 작업 예시
            query = """
            INSERT INTO tb_player_stats (game_id, player_id, goals, assists, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            """
            cursor.execute(query, (match_id, player_id, goals, assists))
        conn.commit()
        logger.info("Sheet data processed successfully")
    except Exception as e:
        logger.error(f"Error processing sheet data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    sheet_id = "your_google_sheet_id"  # Google Sheet ID를 여기에 입력
    data = load_google_sheet(sheet_id)
    process_sheet_data(data)
