"""Weather Application of cities

This module includes the WeatherApp class which is a class that creates a weather app GUI
using tkinter where user's will be able to use an entry bar to enter a specified city and
receive information about it including the highest temperature of the current day, most 
recent measured pressure in hPa, and a weather image icon representing the current weather
condition of specified city. Information is pulled from the OpenWeather API.
"""

import requests
import tkinter as tk
import time
from PIL import Image, ImageTk
from urllib.request import urlopen
from dotenv import load_dotenv
import os

load_dotenv(".env")
KEY = os.getenv("WEATHER_API_KEY")

class WeatherApp:
    """An object that creates an user interactive GUI relating to weather conditions
    of user specified cities.
    """
    def __init__(self) -> None:
        """Initaties entire GUI
        """
        self.initiateWindow()
        self.createTextField()
        self.createButtons()
        self.runWindow()

    def initiateWindow(self) -> None:
        """initiates window
        """
        self.window = tk.Tk()
        self.window.geometry("850x650")
        self.window.title("Weather App")
        self.window.configure(bg='#89CFF0')

    def createTextField(self) -> None:
        """Creates text feilds
        """
        textfield_prompt = tk.Label(self.window, text="City: ", font=("MS Sans Serif", 35, "bold"), bg='#89CFF0')
        textfield_prompt.pack()
        self.textfield = tk.Entry(self.window, font=("MS Sans Serif", 35, "bold"))
        self.textfield.pack()
        self.textfield.focus()
        self.textfield.bind('<Return>', self.getWeather)
        self.first_entry = True
    
    def createButtons(self) -> None:
        """Creates buttons
        """
        self.temp_button = tk.Button(self.window, text="Temp", command=self.temp_options, bg='#89CFF0')
        self.temp_button.config(state="disabled")
        self.temp_button.update()
        self.temp_button.pack()
        self.other_button = tk.Button(self.window, text="Others", command=self.other_options, bg='#89CFF0')
        self.other_button.config(state="disabled")
        self.other_button.update()
        self.other_button.pack()

    def getWeather(self, canvas: tk) -> None:
        """Gathers information for starting screen

        Args:
            canvas: A tkinter window
        """
        city = self.textfield.get()
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + KEY
        self.json_data = requests.get(api).json()
        cod = self.json_data['cod']
        if cod == '404':
            not_found_message = tk.Label(self.window, text="An error occurred, please try again", fg="red", bg='#89CFF0')
            not_found_message.pack()
            not_found_message.after(5000, not_found_message.destroy)
        else:
            found_message = tk.Label(self.window, text="City found!", fg="green", bg='#89CFF0')
            found_message.pack()
            found_message.after(5000, found_message.destroy)
            if self.first_entry:
                self.first_entry = False
                self.in_temp = True
                self.in_options = False
                self.icon_id = self.json_data['weather'][0]['icon']
                self.image_url = "http://openweathermap.org/img/wn/" + self.icon_id + "@2x.png"
                u = urlopen(self.image_url)
                raw_data = u.read()
                u.close()
                self.photo = ImageTk.PhotoImage(data=raw_data)
                self.icon_label = tk.Label(self.window, image=self.photo, bg='#89CFF0')
                self.icon_label.pack()
                self.other_button.config(state="normal")
                self.condition = self.json_data['weather'][0]['main']
                self.condition_label = tk.Label(self.window, text="Condition: " + self.condition, font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                self.condition_label.pack()
                self.far_temp = int((self.json_data['main']['temp'] - 273.15) * 9/5 + 32)
                self.far_temp_label = tk.Label(self.window, text="Temperature: " + str(self.far_temp) + "°F",
                                            font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                self.far_temp_label.pack()
                self.far_min_temp = int((self.json_data['main']['temp_min'] - 273.15) * 9/5 + 32)
                self.far_min_temp_label = tk.Label(self.window, text="Min Temperature: " + str(self.far_min_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                self.far_min_temp_label.pack()
                self.far_max_temp = int((self.json_data['main']['temp_max'] - 273.15) * 9/5 + 32)
                self.far_max_temp_label = tk.Label(self.window, text="Max Temperature: " + str(self.far_max_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                self.far_max_temp_label.pack()
                self.far_feels_like_temp = int((self.json_data['main']['feels_like'] - 273.15) * 9/5 + 32)
                self.far_feels_like_temp_label = tk.Label(self.window, text="Feels Like Temperature: " + str(self.far_feels_like_temp) + "°F",
                                                        font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                self.far_feels_like_temp_label.pack()
            else:
                if self.in_temp:
                    self.icon_label.destroy()
                    self.condition_label.destroy()
                    self.far_temp_label.destroy()
                    self.far_min_temp_label.destroy()
                    self.far_max_temp_label.destroy()
                    self.far_feels_like_temp_label.destroy()
                    self.icon_id = self.json_data['weather'][0]['icon']
                    self.image_url = "http://openweathermap.org/img/wn/" + self.icon_id + "@2x.png"
                    u = urlopen(self.image_url)
                    raw_data = u.read()
                    u.close()
                    self.photo = ImageTk.PhotoImage(data=raw_data)
                    self.icon_label = tk.Label(self.window, image=self.photo, bg='#89CFF0')
                    self.icon_label.pack()
                    self.condition = self.json_data['weather'][0]['main']
                    self.condition_label = tk.Label(self.window, text="Condition: " + self.condition, font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.condition_label.pack()
                    self.far_temp = int((self.json_data['main']['temp'] - 273.15) * 9/5 + 32)
                    self.far_temp_label = tk.Label(self.window, text="Temperature: " + str(self.far_temp) + "°F",
                                                font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.far_temp_label.pack()
                    self.far_min_temp = int((self.json_data['main']['temp_min'] - 273.15) * 9/5 + 32)
                    self.far_min_temp_label = tk.Label(self.window, text="Min Temperature: " + str(self.far_min_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.far_min_temp_label.pack()
                    self.far_max_temp = int((self.json_data['main']['temp_max'] - 273.15) * 9/5 + 32)
                    self.far_max_temp_label = tk.Label(self.window, text="Max Temperature: " + str(self.far_max_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.far_max_temp_label.pack()
                    self.far_feels_like_temp = int((self.json_data['main']['feels_like'] - 273.15) * 9/5 + 32)
                    self.far_feels_like_temp_label = tk.Label(self.window, text="Feels Like Temperature: " + str(self.far_feels_like_temp) + "°F",
                                                            font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.far_feels_like_temp_label.pack()
                if self.in_options:
                    self.icon_label.destroy()
                    self.pressure_label.destroy()
                    self.humidity_label.destroy()
                    self.wind_label.destroy()
                    self.sunrise_label.destroy()
                    self.sunset_label.destroy()
                    self.icon_id = self.json_data['weather'][0]['icon']
                    self.image_url = "http://openweathermap.org/img/wn/" + self.icon_id + "@2x.png"
                    u = urlopen(self.image_url)
                    raw_data = u.read()
                    u.close()
                    self.photo = ImageTk.PhotoImage(data=raw_data)
                    self.icon_label = tk.Label(self.window, image=self.photo, bg='#89CFF0')
                    self.icon_label.pack()
                    pressure = self.json_data['main']['pressure']
                    self.pressure_label = tk.Label(self.window, text="Pressure: " + str(pressure) + " hPa", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.pressure_label.pack()
                    humidity = self.json_data['main']['humidity']
                    self.humidity_label = tk.Label(self.window, text="Humidity: " + str(humidity) + "%", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.humidity_label.pack()
                    wind = self.json_data['wind']['speed']
                    self.wind_label = tk.Label(self.window, text="Wind: " + str(wind) + " Meter/Second", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.wind_label.pack()
                    sunrise = time.strftime("%I:%M:%S", time.gmtime(self.json_data['sys']['sunrise'] - 25200))
                    self.sunrise_label = tk.Label(self.window, text=f"Sunrise: {sunrise}", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.sunrise_label.pack()
                    sunset = time.strftime("%I:%M:%S", time.gmtime(self.json_data['sys']['sunset'] - 25200))
                    self.sunset_label = tk.Label(self.window, text=f"Sunset: {sunset}", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
                    self.sunset_label.pack()

    def temp_options(self) -> None:
        """Display of classic weather information including: condition, current temp, high temp, low temp, and feels like temp
        """
        self.in_temp = True
        self.in_options = False
        self.other_button.config(state='normal')
        self.temp_button.config(state='disabled')
        self.pressure_label.destroy()
        self.humidity_label.destroy()
        self.wind_label.destroy()
        self.sunrise_label.destroy()
        self.sunset_label.destroy()
        self.condition_label = tk.Label(self.window, text="Condition: " + self.condition, font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.condition_label.pack()
        self.far_temp_label = tk.Label(self.window, text="Temperature: " + str(self.far_temp) + "°F",
                                       font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.far_temp_label.pack()
        self.far_min_temp_label = tk.Label(self.window, text="Min Temperature: " + str(self.far_min_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.far_min_temp_label.pack()
        self.far_max_temp_label = tk.Label(self.window, text="Max Temperature: " + str(self.far_max_temp) + "°F", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.far_max_temp_label.pack()
        self.far_feels_like_temp_label = tk.Label(self.window, text="Feels Like Temperature: " + str(self.far_feels_like_temp) + "°F",
                                                  font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.far_feels_like_temp_label.pack()

    def other_options(self) -> None:
        """Display of other weather information including: pressure, humidity, wind speeds, sunrise time, and sunset time
        """
        self.in_temp = False
        self.in_options = True
        self.other_button.config(state='disabled')
        self.temp_button.config(state='normal')
        self.condition_label.destroy()
        self.far_temp_label.destroy()
        self.far_min_temp_label.destroy()
        self.far_max_temp_label.destroy()
        self.far_feels_like_temp_label.destroy()
        pressure = self.json_data['main']['pressure']
        self.pressure_label = tk.Label(self.window, text="Pressure: " + str(pressure) + " hPa", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.pressure_label.pack()
        humidity = self.json_data['main']['humidity']
        self.humidity_label = tk.Label(self.window, text="Humidity: " + str(humidity) + "%", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.humidity_label.pack()
        wind = self.json_data['wind']['speed']
        self.wind_label = tk.Label(self.window, text="Wind: " + str(wind) + " Meter/Second", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.wind_label.pack()
        sunrise = time.strftime("%I:%M:%S", time.gmtime(self.json_data['sys']['sunrise'] - 25200))
        self.sunrise_label = tk.Label(self.window, text=f"Sunrise: {sunrise}", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.sunrise_label.pack()
        sunset = time.strftime("%I:%M:%S", time.gmtime(self.json_data['sys']['sunset'] - 25200))
        self.sunset_label = tk.Label(self.window, text=f"Sunset: {sunset}", font=("MS Sans Serif", 15, "bold"), bg='#89CFF0')
        self.sunset_label.pack()

    def runWindow(self) -> None:
        self.window.mainloop()

if __name__ == "__main__":
    weatherApp = WeatherApp()
