import os

db_config = {
    "mysql": {
        "host": "localhost",
        "name": "tennis_match_db",
        "user": "root",
        "password": "root"
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths_list = {
    "index": r"index.html",
    "new_match": r"new-match.html",
    "matches": r"matches.html",
    "match_score": r"match-score.html",
    "error": r"not_found.html",
    "static_files": os.path.join(BASE_DIR, "view", "static", "css"),
    "templates_files": os.path.join(BASE_DIR, "view", "templates"),

}
