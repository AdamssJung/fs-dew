# Placeholder for data_validation.py
import re
from datetime import datetime

def validate_presence(fields, record):
    """
    필수 필드가 모두 존재하는지 검증.
    :param fields: 필수 필드 리스트 (예: ["match_id", "player_id"])
    :param record: 검증할 데이터 딕셔너리
    :return: 모든 필드가 존재하면 True, 아니면 False
    """
    missing_fields = [field for field in fields if field not in record or record[field] is None]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")
    return True

def validate_date_format(date_string, date_format="%Y-%m-%d"):
    """
    날짜 형식을 검증.
    :param date_string: 검증할 날짜 문자열
    :param date_format: 기대되는 날짜 형식 (기본값: "YYYY-MM-DD")
    :return: 변환된 datetime 객체 또는 ValueError
    """
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Expected format: {date_format}")

def validate_integer(value, field_name):
    """
    값이 정수인지 검증.
    :param value: 검증할 값
    :param field_name: 필드 이름 (오류 메시지에 사용)
    :return: 정수 변환된 값 또는 ValueError
    """
    if not isinstance(value, int):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Field '{field_name}' must be an integer. Found: {value}")
    return value

def clean_string(value):
    """
    문자열 정리: 공백 제거, 소문자 변환.
    :param value: 검증할 문자열
    :return: 정리된 문자열
    """
    if isinstance(value, str):
        return value.strip().lower()
    return value
