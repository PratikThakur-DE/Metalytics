import os
import sys
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from models import Base
from src.log_info import setup_logging

# Load environment variables
load_dotenv()
setup_logging()


def create_db_engine():
    """
    Sets up the database engine using environment variables.
    """
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        logging.critical(
            "Missing required database credentials in environment variables."
        )
        sys.exit("Missing required database credentials in environment variables.")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    logging.info(f"Connecting to database at: {DATABASE_URL}")

    try:
        engine = create_engine(DATABASE_URL, echo=True)
        engine.connect()
        logging.info("Database connection successful.")
        return engine
    except OperationalError as e:
        logging.critical(f"Database connection failed: {e}")
        sys.exit(f"Database connection failed: {e}")


def create_session(engine):
    """
    Creates a new SQLAlchemy session.
    """
    logging.info("Creating a new database session.")
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


def init_db(engine):
    """
    Initializes the database by creating all tables.
    """
    logging.info("Creating database tables.")
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully.")

    # Create the view after creating the tables
    create_view(engine)


def create_view(engine):
    """Creates a view in the database if it doesn't already exist."""
    with engine.connect() as connection:
        create_view_sql = """
            CREATE OR REPLACE VIEW precious_metals_prices_view AS
            SELECT metal, price, timestamp
            FROM precious_metals_prices;
        """
        try:
            connection.execute(text(create_view_sql))
            connection.commit()
            logging.info("View 'precious_metals_prices_view' created successfully.")
        except Exception as e:
            logging.error(f"Failed to create view: {e}")
            connection.rollback()
            raise  # Raise exception to stop execution
