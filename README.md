# 🎨 GanttCraft

Welcome to **GanttCraft**, a sleek and intuitive web app created by **[Parthiv Koli](https://github.com/Parthivkoli)** that transforms your text, CSV, or Excel files into stunning Gantt charts. Whether you're a student, project manager, or developer, GanttCraft makes project planning **visual, easy, and effective**. 

Upload your task data, customize your chart, and export it—all from a clean, responsive UI powered by **Streamlit** and **Plotly**.
[![HuggingFace Spaces](https://img.shields.io/badge/HF%20Spaces-GanttCraftPro-blueviolet?logo=huggingface&logoColor=white)](https://huggingface.co/spaces/ParthivKoli/GanttCraftPro)
[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://parthivkoli-ganttcraft.streamlit.app/)

> 🚀 _Turning data into timelines, one chart at a time._

---

## ✨ Features

- 📁 **File Flexibility**  
  Supports `.txt` (tab-separated), `.csv`, and `.xlsx` formats.

- 📊 **Interactive Visuals**  
  Dynamic Gantt charts using Plotly with zoom and pan features.

- 🎨 **Customizable Inputs**  
  Choose columns for Task Name, Start/End Dates, and even color by Category or Priority.

- 📤 **Export Options**  
  Download charts as **PNG, JPEG, or PDF** via Kaleido.

- ☁️ **Cloud-Optimized**  
  Perfect for deployment on **Streamlit Cloud**—access your planner from anywhere!

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- Git (for cloning the repo)
- [Streamlit Cloud](https://streamlit.io/cloud) account (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/Parthivkoli/GanttCraft.git
cd GanttCraft

# Set up a virtual environment
python -m venv venv
# Activate it
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt
````

---

## 📈 How to Use

### Launch Locally

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

### Upload Your File

Supported formats: `.txt` (tab-separated), `.csv`, `.xlsx`
Make sure your file has these **required columns**:

* **Task Name** (string)
* **Start Date** (format: YYYY-MM-DD)
* **End Date** (format: YYYY-MM-DD)

Optionally, add a column for task color grouping (like Category or Priority).

### Preview & Export

* View your beautiful interactive Gantt chart.
* Export as PNG, JPEG, or PDF.

---

## ☁️ Deploying to Streamlit Cloud

Want to share your charts with the world? Deploy with just a few clicks:

1. Push your code to GitHub:

   ```bash
   git push origin main
   ```

2. Sign in to [Streamlit Cloud](https://streamlit.io/cloud).

3. Create a new app linked to your repo `Parthivkoli/GanttCraft`.

4. Set `app.py` as the main file and hit **Deploy**.

🎉 Your app will be live at:
`https://parthivkoli-ganttcraft.streamlit.app`

---

## 🚀 Try the Pro Version!

Looking for **AI-powered features**, a smoother UI, and better performance?

👉 **[Explore GanttCraft Pro](https://huggingface.co/spaces/ParthivKoli/GanttCraftPro)**
Built on Hugging Face Spaces — it's fast, elegant, and smarter.

---

## 🤝 Contributing

Love GanttCraft and want to make it even better?

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-idea`
3. Commit: `git commit -m "Add awesome idea"`
4. Push: `git push origin feature/your-idea`
5. Submit a pull request!

I’ll be happy to review it!

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for full details.

---

## 💬 Get in Touch

Got feedback, feature requests, or just want to connect?

* 📬 Open an [issue](https://github.com/Parthivkoli/GanttCraft/issues)
* 🔗 Connect with me on [GitHub](https://github.com/Parthivkoli)

---

Crafted with ❤️ by **Parthiv Koli**

> "*Helping you craft clarity from complexity, one chart at a time.*"
