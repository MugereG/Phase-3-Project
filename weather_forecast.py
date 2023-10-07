import os
import random
from datetime import date, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Defining my SQL Database
db_path = "weather_forecast.db"
engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    forecasts = relationship("WeatherForecast", back_populates="location")

class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True)
    temperature = Column(Integer, nullable=False)
    conditions = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location", back_populates="forecasts")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

def add_weather_forecast(city, country, temperature, conditions, date):
    location = Location(city=city, country=country)
    session.add(location)
    session.commit()

    forecast = WeatherForecast(
        temperature=temperature,
        conditions=conditions,
        date=date,
        location=location
    )
    session.add(forecast)
    session.commit()

def list_weather_forecasts():
    forecasts = session.query(WeatherForecast).all()
    for forecast in forecasts:
        print(f"Location: {forecast.location.city}, {forecast.location.country}")
        print(f"Date: {forecast.date}")
        print(f"Temperature: {forecast.temperature}°C")
        print(f"Conditions: {forecast.conditions}")
        print("-" * 30)

def search_weather_forecasts(city):
    forecasts = session.query(WeatherForecast).join(Location).filter(Location.city == city).all()
    if forecasts:
        print(f"Weather forecasts for {city}:")
        for forecast in forecasts:
            print(f"Date: {forecast.date}")
            print(f"Temperature: {forecast.temperature}°C")
            print(f"Conditions: {forecast.conditions}")
            print("-" * 30)
    else:
        print(f"No weather forecasts found for {city}.")

if __name__ == "__main__":
    while True:
        print("\nWeather Forecast CLI")
        print("1. Add Weather Forecast")
        print("2. List Weather Forecasts")
        print("3. Search Weather Forecasts")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            city = input("Enter city: ")
            country = input("Enter country: ")
            temperature = random.randint(0, 40)
            conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Snowy"])
            date = date.today() + timedelta(days=random.randint(1, 7))
            add_weather_forecast(city, country, temperature, conditions, date)
            print("Weather forecast added successfully!")

        elif choice == "2":
            list_weather_forecasts()

        elif choice == "3":
            city = input("Enter city to search: ")
            search_weather_forecasts(city)

        elif choice == "4":
            print("Exiting Weather Forecast CLI. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")
