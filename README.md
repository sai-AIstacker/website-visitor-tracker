# Visitor Tracker

A lightweight visitor analytics system built with FastAPI. This project tracks website visits, logs geographic and device information, and stores the data in an Excel file for monitoring and analysis. The frontend provides a clean, minimal, glassmorphism interface to display visitor statistics.

---

## Features

- Tracks visitor IP, location (country, city, region)
- Detects browser, operating system, and device type
- Records timestamp and referrer source
- Saves all analytics in an Excel file (`visitors_data.xlsx`)
- Displays live visitor count on the website UI
- Frontend designed using modern glassmorphism style

---

## Tech Stack

| Layer       | Technology |
|------------|------------|
| Backend    | FastAPI    |
| Frontend   | HTML, CSS (Glassmorphism UI) |
| Database   | Excel (OpenPyXL) |
| Analytics  | IP Geo Lookup API, User Agent Parser |

---



