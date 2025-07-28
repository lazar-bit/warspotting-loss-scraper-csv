# Russian Equipment Losses (WarSpotting API CSV Extractor)

This Python script downloads and saves documented Russian equipment losses from the open-source [WarSpotting.net](https://ukr.warspotting.net) API into a structured CSV file for further analysis and research.

---

## 🔧 Features

- Fetches equipment loss data for each day from **February 24, 2022** onward
- Based on the **official WarSpotting.net public API**
- Automatically paginates through **all available records per day**
- Outputs data into a structured `.csv` file
- Parses key fields including type, model, location, coordinates, unit, tags, sources, and photos
- Includes polite delays between API calls to respect server load

---

## ⚠️ Limitations & Disclaimers

- 📅 Only **Russian losses** are accessible through the API; Ukrainian data is not available
- ⏱️ Script adds delays between daily queries to avoid overwhelming the API
- 🧪 This project is intended strictly for **research and educational purposes**
- 💬 All data is sourced from [WarSpotting.net](https://ukr.warspotting.net) — maintained by a public contributor network

---

## 🛠️ How It Works

1. The script loops through each day from **2022-02-24 to today**
2. It queries the WarSpotting API for each day, including all paginated pages
3. Each record is flattened and cleaned, including GPS coordinate parsing (if present)
4. The final result is saved as `warspotting_losses.csv` in the project directory

---

## 📄 Example Output Columns

- `id`
- `date`
- `type`
- `model`
- `status`
- `lost_by`
- `nearest_location`
- `geo` (original string)
- `latitude` / `longitude` (parsed from `geo`)
- `unit`
- `tags`
- `comment`
- `sources`
- `photos`

---

## ✅ Requirements

- Python 3.x
- [`requests`](https://pypi.org/project/requests/)

Install dependencies with:

```bash
pip install requests
````

---

## 🚀 Usage

Run the script directly:

```bash
python warspotting_loss_scraper_csv.py
```

The script will:

* Start from February 24, 2022
* Retrieve all available records (with pagination) from the API
* Save the output to `warspotting_losses.csv`

---

## 📂 Output File

* Format: CSV (`warspotting_losses.csv`)
* Encoding: UTF-8
* File is overwritten each time the script is run

---

## 📄 License

This project is licensed under the **MIT License** — see the `LICENSE` file for full terms.

---

## 🙏 Acknowledgments

* Data and API provided by [WarSpotting.net](https://ukr.warspotting.net)
* Built by [Zsolt Lazar](https://medium.com/@zsoltlazar) for academic and open-source research into conflict monitoring and OSINT workflows
