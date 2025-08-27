# Turkish Weather Data Scraper 🌤️

A Python script to fetch 2 years of historical weather data for all cities in Turkey using the Open-Meteo Historical Weather API.

## Features 📊

- **Comprehensive Data**: Fetches 15 weather variables for each city
- **2 Years Historical Data**: From August 2023 to August 2025
- **All Turkish Cities**: 81 provinces + major districts (~81 locations)
- **Multiple Formats**: Outputs both CSV and JSON files
- **Robust Error Handling**: Rate limit protection, timeout retry, JSON validation
- **Regional Analysis**: Groups data by Turkish geographical regions

## Weather Variables 🌡️

The script collects the following daily weather data:

- **Temperature**: Max/min temperature, apparent temperature
- **Precipitation**: Total precipitation, rain sum, snowfall sum, precipitation hours
- **Solar**: Sunshine duration, daylight duration, solar radiation
- **Wind**: Max wind speed, wind gusts, dominant wind direction  
- **Agriculture**: ET₀ evapotranspiration

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/turkish-weather-scraper.git
   cd turkish-weather-scraper
   ```

2. **Install required packages**
   ```bash
   pip install requests pandas
   ```

3. **Run the script**
   ```bash
   python weather_scraper.py
   ```

## Configuration ⚙️

The script uses a `cities_config.json` file to define which cities to fetch data for. The configuration file should have this structure:

```json
{
  "turkish_cities": [
    {
      "name": "Istanbul",
      "lat": 41.0082,
      "lon": 28.9784,
      "region": "Marmara",
      "population": 15462452
    },
    {
      "name": "Ankara", 
      "lat": 39.9334,
      "lon": 32.8597,
      "region": "Central Anatolia",
      "population": 5663322
    }
  ]
}
```

## Output Files 📁

The script generates two output files:

1. **CSV Format**: `turkey_weather_data_YYYY-MM-DD_YYYY-MM-DD.csv`
2. **JSON Format**: `turkey_weather_data_YYYY-MM-DD_YYYY-MM-DD.json`

### CSV Structure

| Column | Description |
|--------|-------------|
| date | Date (YYYY-MM-DD) |
| city | City name |
| latitude, longitude | GPS coordinates |
| region | Turkish geographical region |
| population | City population |
| temperature_2m_max | Maximum temperature (°C) |
| temperature_2m_min | Minimum temperature (°C) |
| apparent_temperature_max | Max apparent temperature (°C) |
| apparent_temperature_min | Min apparent temperature (°C) |
| precipitation_sum | Total precipitation (mm) |
| rain_sum | Rain amount (mm) |
| snowfall_sum | Snowfall amount (cm) |
| precipitation_hours | Hours of precipitation |
| sunshine_duration | Sunshine duration (seconds) |
| daylight_duration | Daylight duration (seconds) |
| wind_speed_10m_max | Max wind speed (km/h) |
| wind_gusts_10m_max | Max wind gusts (km/h) |
| wind_direction_10m_dominant | Dominant wind direction (°) |
| shortwave_radiation_sum | Solar radiation (MJ/m²) |
| et0_fao_evapotranspiration | Evapotranspiration (mm) |

## Rate Limiting ⚡

The script is designed to respect Open-Meteo's free tier limits:

- **Daily limit**: 10,000 API calls
- **Hourly limit**: 5,000 API calls  
- **Per minute**: 600 API calls

Our script uses only ~81 API calls total, well within limits.

## Error Handling 🛡️

The script includes robust error handling for:

- **Rate limits**: Automatic retry with exponential backoff
- **Timeouts**: Progressive timeout increases (60s → 90s → 120s)
- **JSON errors**: Validates response content
- **Network issues**: Multiple retry attempts
- **Empty responses**: Detects and reports server issues

## Performance ⏱️

- **Typical runtime**: 10-15 minutes for all 81 cities
- **Data size**: ~59,000 records (81 cities × 730 days)
- **File size**: ~15-20 MB (CSV), ~25-30 MB (JSON)

## Data Source 📡

This project uses the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), which provides:

- **Free access** for non-commercial use
- **No API key required**
- **High-quality reanalysis data** from ECMWF ERA5
- **Global coverage** with 9km spatial resolution

## License 📄

This project is open source. The weather data is provided under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license from Open-Meteo.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments 🙏

- [Open-Meteo](https://open-meteo.com) for providing free weather data
- ECMWF for the ERA5 reanalysis dataset
- National weather services for observational data

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

**⚠️ Important**: This script is for non-commercial use only. For commercial usage, please consider [Open-Meteo's commercial plans](https://open-meteo.com/en/pricing).
