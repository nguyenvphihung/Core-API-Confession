from logging.config import fileConfig
import os
import sys

# Thêm thư mục gốc của backend vào sys.path để import được database và models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import Base và tất cả các models để autogenerate hoạt động
from database import Base
import models  # noqa: F401 — import này cần thiết để Alembic "nhìn thấy" tất cả models

# Alembic Config object — cung cấp giá trị từ file alembic.ini
config = context.config

# Ghi đè sqlalchemy.url bằng DATABASE_URL từ .env (ưu tiên hơn giá trị trong .ini)
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Cấu hình logging từ alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata của tất cả models — cần thiết cho --autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Chạy migrations ở chế độ offline (không cần kết nối DB trực tiếp).
    
    Hữu ích khi muốn xem SQL sẽ được chạy mà không cần DB thực sự.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Phát hiện thay đổi kiểu dữ liệu cột
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Chạy migrations ở chế độ online (kết nối trực tiếp đến DB).
    
    Đây là chế độ mặc định khi chạy alembic upgrade/downgrade.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Phát hiện thay đổi kiểu dữ liệu cột
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
