from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class PreciousMetalPrice(Base):
    __tablename__ = "precious_metals_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    metal = Column(String(10), nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(
        DateTime,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
        index=True,
    )

    def __repr__(self):
        return f"<PreciousMetalPrice(metal='{self.metal}', price={self.price}, timestamp={self.timestamp})>"


class ModelMetadata(Base):  # Assuming you have a Base class from SQLAlchemy
    __tablename__ = "model_training_metadata"

    id = Column(Integer, primary_key=True)
    metal = Column(String, nullable=False)
    hyperparameters = Column(
        JSON, nullable=False
    )  # Use JSON or TEXT depending on your DB
    parameters = Column(JSON, nullable=False)  # Same as above
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<ModelMetadata(metal='{self.metal}', hyperparameters={self.hyperparameters}, parameters={self.parameters}, timestamp={self.timestamp})>"
