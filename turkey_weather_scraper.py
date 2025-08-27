import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import os

def load_cities_config(config_file="cities_config.json"):
    """Load cities list from configuration file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config['turkish_cities']
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        print("Please create cities_config.json file.")
        return []
    except Exception as e:
        print(f"Config file read error: {e}")
        return []

def fetch_weather_data(config_file="cities_config.json"):
    """Fetch 2 years of historical weather data"""
    
    # Load cities list
    turkish_cities = load_cities_config(config_file)
    if not turkish_cities:
        return None
    
    print("Turkish Weather Data Scraper")
    print(f"Fetching 2 years of data for {len(turkish_cities)} locations")
    print("-" * 60)
    
    # Date range (last 2 years, historical data only)
    today = datetime.now().date()
    end_date = today - timedelta(days=1)  # Yesterday (2025-08-26)
    start_date = end_date - timedelta(days=729)  # 2 years ago (2023-08-27)
    
    print(f"Date range: {start_date} to {end_date}")
    print("-" * 60)
    
    all_data = []
    success_count = 0
    error_count = 0
    
    for i, city in enumerate(turkish_cities, 1):
        try:
            print(f"[{i}/{len(turkish_cities)}] Fetching {city['name']}...", end=" ")
            
            # Open-Meteo Historical Weather API call
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": city["lat"],
                "longitude": city["lon"],
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "daily": "temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,sunshine_duration,daylight_duration,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration",
                "timezone": "Europe/Istanbul"
            }
            
            response = requests.get(url, params=params, timeout=60)  # 60 seconds timeout
            response.raise_for_status()
            
            # Validate response content
            if not response.text.strip():
                print("Empty response!")
                error_count += 1
            else:
                try:
                    data = response.json()
                except ValueError as json_error:
                    print(f"JSON parse error. Response first 200 chars:")
                    print(f"'{response.text[:200]}...'")
                    error_count += 1
                    data = None
            
            # Convert data to pandas DataFrame
            if data and 'daily' in data:
                df = pd.DataFrame(data['daily'])
                df['city'] = city["name"]
                df['latitude'] = city["lat"]
                df['longitude'] = city["lon"]
                
                # Add additional info if available
                if 'region' in city:
                    df['region'] = city["region"]
                if 'population' in city:
                    df['population'] = city["population"]
                
                # Convert time column to datetime
                df['date'] = pd.to_datetime(df['time'])
                df = df.drop('time', axis=1)
                
                all_data.append(df)
                success_count += 1
                print("✅")
            else:
                print("No data found")
                error_count += 1
                
        except requests.exceptions.Timeout:
            print(f"Timeout! Waiting 10 seconds...")
            time.sleep(10)
            # Retry for timeout
            try:
                response = requests.get(url, params=params, timeout=90)  # Longer timeout
                response.raise_for_status()
                
                if not response.text.strip():
                    print("Empty response! (timeout retry)")
                    error_count += 1
                else:
                    try:
                        data = response.json()
                    except ValueError:
                        print(f"JSON parse error (timeout retry): '{response.text[:100]}...'")
                        error_count += 1
                        continue
                
                if data and 'daily' in data:
                    df = pd.DataFrame(data['daily'])
                    df['city'] = city["name"]
                    df['latitude'] = city["lat"]
                    df['longitude'] = city["lon"]
                    
                    # Add additional info if available
                    if 'region' in city:
                        df['region'] = city["region"]
                    if 'population' in city:
                        df['population'] = city["population"]
                    
                    # Convert time column to datetime
                    df['date'] = pd.to_datetime(df['time'])
                    df = df.drop('time', axis=1)
                    
                    all_data.append(df)
                    success_count += 1
                    print("✅ (timeout retry)")
                else:
                    print("No data found (timeout retry)")
                    error_count += 1
            except Exception as timeout_retry_e:
                print(f"Timeout retry failed: {timeout_retry_e}")
                error_count += 1
        except requests.exceptions.RequestException as e:
            if "429" in str(e):
                print(f"Rate limit! Waiting 10 seconds...")
                time.sleep(10)
                # Retry for rate limit
                try:
                        try:
                            response = requests.get(url, params=params, timeout=90)  # Long timeout
                            response.raise_for_status()
                            
                            if not response.text.strip():
                                print("Empty response! (2nd attempt)")
                                error_count += 1
                            else:
                                try:
                                    data = response.json()
                                except ValueError:
                                    print(f"JSON parse error (2nd attempt): '{response.text[:100]}...'")
                                    error_count += 1
                                    continue
                            
                            if data and 'daily' in data:
                                df = pd.DataFrame(data['daily'])
                                df['city'] = city["name"]
                                df['latitude'] = city["lat"]
                                df['longitude'] = city["lon"]
                                
                                if 'region' in city:
                                    df['region'] = city["region"]
                                if 'population' in city:
                                    df['population'] = city["population"]
                                
                                df['date'] = pd.to_datetime(df['time'])
                                df = df.drop('time', axis=1)
                                
                                all_data.append(df)
                                success_count += 1
                                print("✅ (2nd attempt)")
                            else:
                                print("No data found (2nd attempt)")
                                error_count += 1
                        except Exception as retry_e:
                            if "429" in str(retry_e):
                                print(f"Rate limit again! Waiting 30 seconds...")
                                time.sleep(30)
                                # 3rd attempt
                                try:
                                    response = requests.get(url, params=params, timeout=120)  # Longest timeout
                                    response.raise_for_status()
                                    
                                    if not response.text.strip():
                                        print("Empty response! (3rd attempt)")
                                        error_count += 1
                                    else:
                                        try:
                                            data = response.json()
                                        except ValueError:
                                            print(f"JSON parse error (3rd attempt): '{response.text[:100]}...'")
                                            error_count += 1
                                            continue
                                    
                                    if data and 'daily' in data:
                                        df = pd.DataFrame(data['daily'])
                                        df['city'] = city["name"]
                                        df['latitude'] = city["lat"]
                                        df['longitude'] = city["lon"]
                                        
                                        if 'region' in city:
                                            df['region'] = city["region"]
                                        if 'population' in city:
                                            df['population'] = city["population"]
                                        
                                        df['date'] = pd.to_datetime(df['time'])
                                        df = df.drop('time', axis=1)
                                        
                                        all_data.append(df)
                                        success_count += 1
                                        print("✅ (3rd attempt)")
                                    else:
                                        print("No data found (3rd attempt)")
                                        error_count += 1
                                except Exception as final_e:
                                    print(f"3rd attempt failed, skipping: {final_e}")
                                    error_count += 1
                            else:
                                print(f"2nd attempt failed: {retry_e}")
                                error_count += 1
                except:
                    pass
            else:
                print(f"Network error: {e}")
                error_count += 1
        except Exception as e:
            print(f"Error: {e}")
            error_count += 1
        
        # Be gentle with the API (rate limit protection)
        time.sleep(8.0)  # 8 seconds = 7.5 requests per minute (very safe)
    
    print("-" * 60)
    print(f"✅ Successful: {success_count}")
    print(f"Failed: {error_count}")
    
    if all_data:
        # Combine all data
        print("\nCombining data...")
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Data summary
        print(f"Total records: {len(final_df):,}")
        print(f"Date range: {final_df['date'].min().date()} to {final_df['date'].max().date()}")
        print(f"Number of cities: {final_df['city'].nunique()}")
        
        # Save as CSV
        filename = f"turkey_weather_data_{start_date}_{end_date}.csv"
        final_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nData saved: {filename}")
        
        # Also save as JSON (optional)
        json_filename = f"turkey_weather_data_{start_date}_{end_date}.json"
        final_df.to_json(json_filename, orient='records', date_format='iso', indent=2)
        print(f"Also saved in JSON format: {json_filename}")
        
        # Summary statistics
        print("\nSummary Statistics:")
        print(f"Average maximum temperature: {final_df['temperature_2m_max'].mean():.1f}°C")
        print(f"Average minimum temperature: {final_df['temperature_2m_min'].mean():.1f}°C")
        print(f"Average precipitation: {final_df['precipitation_sum'].mean():.1f} mm")
        
        return final_df
    else:
        print("No data could be fetched!")
        return None

def main():
    """Main function"""
    # Check if config file exists
    config_file = "cities_config.json"
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        print("Please create cities_config.json file.")
        return
    
    # Start data fetching
    df = fetch_weather_data(config_file)
    
    if df is not None:
        print(f"\nProcess completed! {len(df):,} records successfully fetched.")
        print("\nFirst 5 records:")
        print(df.head())
        
        # Region-based summary
        if 'region' in df.columns:
            print(f"\nRegional Distribution:")
            region_counts = df.groupby('region')['city'].nunique().sort_values(ascending=False)
            for region, count in region_counts.items():
                print(f"  {region}: {count} cities")
    else:
        print("\nProcess failed.")

if __name__ == "__main__":
    main()
