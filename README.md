# 🚑 AI-Driven Smart Ambulance Routing System

A real-time web-based ambulance routing system that identifies the nearest hospitals, calculates ETA using live traffic, and visualizes the route dynamically. This project combines geospatial APIs, weather data, and a responsive frontend to enhance emergency medical response.

[![GitHub repo](https://img.shields.io/github/stars/fabine-bobby/AI-Driven-Smart-Ambulance-Routing-System?style=social)](https://github.com/fabine-bobby/AI-Driven-Smart-Ambulance-Routing-System)

---

## 🌟 Features

- 🔍 Google Places-powered **location autocomplete**
- 🏥 **Nearest hospital detection** with ETA & distance
- 🛣️ **Traffic-aware routing** with visual polylines
- 🚦 Real-time **traffic level heatmap** (green/yellow/red)
- 🌡️ **Weather and temperature** display (OpenWeatherMap)
- 📄 **PDF route export** using jsPDF
- 📱 **Mobile-friendly** UI using Tailwind CSS
- 🔗 One-click **WhatsApp route sharing**

---

## 🧠 Tech Stack

| Layer     | Technologies |
|-----------|--------------|
| Backend   | Python Flask |
| Frontend  | HTML, JavaScript, Tailwind CSS |
| Mapping   | Leaflet.js, Google Maps API |
| APIs      | Google Directions, Geocoding, Places, OpenWeatherMap |
| Others    | jsPDF, responsive design, WhatsApp link generation |

---

## 🚀 Getting Started

### 🔧 Installation

```bash
git clone https://github.com/fabine-bobby/AI-Driven-Smart-Ambulance-Routing-System.git
cd AI-Driven-Smart-Ambulance-Routing-System
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
