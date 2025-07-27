import os

# 创建 env_config 目录如果不存在
env_config_dir = "env_config"
if not os.path.exists(env_config_dir):
    os.makedirs(env_config_dir)


def get_xhs_profile_base_url():
    return 'https://www.xiaohongshu.com/user/profile/'


def get_cookie():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read().strip()
            if content.startswith("COOKIES="):
                return content.split("=", 1)[1].strip("'")
    return ""


def set_cookie(value):
    with open(".env", "w") as f:
        f.write(f"COOKIES='{value}'")


def get_user_profile():
    path = os.path.join(env_config_dir, "user_profile")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return ""


def set_user_profile(value):
    path = os.path.join(env_config_dir, "user_profile")
    with open(path, "w") as f:
        f.write(value)


def get_notion_token():
    path = os.path.join(env_config_dir, "notion_token")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return ""


def set_notion_token(value):
    path = os.path.join(env_config_dir, "notion_token")
    with open(path, "w") as f:
        f.write(value)


def get_notion_database_id():
    path = os.path.join(env_config_dir, "notion_database_id")
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return ""


def set_notion_database_id(value):
    path = os.path.join(env_config_dir, "notion_database_id")
    with open(path, "w") as f:
        f.write(value)
