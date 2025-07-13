import os

# 프로젝트 루트 폴더
ROOT_FOLDER = "Migration"

# 폴더 및 파일 구조 정의
STRUCTURE = {
    "config": ["db_config.py"],  # Google API JSON 파일은 제외
    "scripts": [
        "load_data.py",
        "process_attendance.py",
        "process_mom_votes.py",
        "process_goals.py",
        "generate_reports.py",
    ],
    "models": ["__init__.py", "db_models.py"],
    "utils": ["__init__.py", "db_connection.py", "data_validation.py", "logger.py"],
    "tests": [
        "test_db_connection.py",
        "test_data_processing.py",
        "test_models.py",
    ],
    "": ["requirements.txt"],  # Root-level files
}

# 스크립트 실행
def create_project_structure(root_folder, structure):
    os.makedirs(root_folder, exist_ok=True)
    for folder, files in structure.items():
        folder_path = os.path.join(root_folder, folder)
        if folder:  # If folder is not the root folder
            os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as f:
                if file_name == "db_config.py":
                    f.write(
                        f"""# Database connection settings
DATABASE_CONFIG = {{
    "host": "localhost",
    "user": "app_fs",
    "password": "pok1234",
    "database": "db_fs",
    "port": 5432
}}
"""
                    )
                else:
                    f.write("# Placeholder for {}\n".format(file_name))

# 실행
if __name__ == "__main__":
    create_project_structure(ROOT_FOLDER, STRUCTURE)
    print(f"Project structure created under '{ROOT_FOLDER}'")
