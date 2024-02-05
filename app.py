import tkinter as tk
from PIL import Image, ImageTk
import requests

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # You can use "imperial" for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        return temperature, description, icon_code
    else:
        return None, None, None

def display_weather():
    city = entry.get()
    temperature, description, icon_code = get_weather(api_key, city)

    if temperature is not None and description is not None:
        result_label.config(text=f"Temperature: {temperature}°C\nDescription: {description}")

        # Add images based on description
        image_path = get_icon_path(description)
        if image_path:
            weather_icon = Image.open(image_path)
            weather_icon = weather_icon.resize((70, 70))
            icon_photo = ImageTk.PhotoImage(weather_icon)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack()
        else:
            icon_label.pack_forget()  # Hide the icon if not available
    else:
        result_label.config(text="Error fetching weather data.")
        icon_label.pack_forget()  # Hide the icon if there's an error

def clear_input():
    entry.delete(0, tk.END)
    result_label.config(text="")
    icon_label.pack_forget()  # Hide the icon when clearing input

def get_icon_path(description):
    # Map weather descriptions to local image files
    icon_mapping = {
        "mist": "assets/mist.jpg",
        "clear sky": "assets/clear_sky.jpg",
        "few clouds": "assets/few_clouds.jpg",
        "scattered clouds": "assets/scattered_clouds.jpg",
        "broken clouds": "assets/broken_clouds.jpg",
        "rain": "assets/rain.jpg",
        "thunderstorm": "assets/thunderstorm.jpg",
        "snow": "assets/snow.jpg",
    }
    return icon_mapping.get(description.lower(), None)

# Set up the GUI
app = tk.Tk()
app.title("Weather App")

# Add a logo
logo_image = Image.open("assets/logo.png")  
logo_image = logo_image.resize((50, 50))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(app, image=logo_photo)
logo_label.image = logo_photo
logo_label.pack()

label = tk.Label(app, text="Enter City:", font=('Arial', '14', 'bold'))
label.pack(pady=10)

entry = tk.Entry(app)
entry.pack(pady=10)

search_button = tk.Button(app, text="Search", font=('Arial', '12'), command=display_weather)
search_button.pack(pady=10)

clear_button = tk.Button(app, text="Clear", font=('Arial', '12'), command=clear_input)
clear_button.pack(pady=10)

result_label = tk.Label(app, text="", font=('Helvetica', '12'))
result_label.pack(pady=10)

icon_label = tk.Label(app) 
icon_label.pack()

api_key = "43d7abfe318e16063a364981a2b0cacd"

app.mainloop()
