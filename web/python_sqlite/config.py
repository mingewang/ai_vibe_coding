import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_default_database_path():
    data_dir = os.environ.get(
        "COMRITE_CLOUD_DATA_VOLUME",
        os.path.join(BASE_DIR, "data"),
    )
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "blog.db")
