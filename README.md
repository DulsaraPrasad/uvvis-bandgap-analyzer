# 🔬 UV-Vis Spectroscopy: Tauc Plot & Optical Band Gap (E<sub>g</sub>) Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://uvvis-bandgap-analyzer-wypuvivxmvsntx4hwmavd3.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An interactive web application built for materials science researchers, laboratory analysts, and students to automate **Tauc Plot generation** and **Optical Band Gap (E<sub>g</sub>)** determination from UV-Vis absorption spectroscopy data.

---

## 🚀 Live Demo

👉 **[Launch Interactive Web App](https://uvvis-bandgap-analyzer-wypuvivxmvsntx4hwmavd3.streamlit.app/)**

*(Includes a built-in synthetic ZnO nanoparticle dataset so you can test the linear regression sliders immediately without uploading a file.)*

---

## ✨ Key Features

- **Automated Data Processing:** Upload raw UV-Vis spectra directly in `.csv` or `.xlsx` formats with flexible column mapping.
- **Direct & Indirect Transitions:** Instant switching between **Direct Allowed (n = 1/2)** and **Indirect Allowed (n = 2)** electronic transitions.
- **Interactive Linear Extrapolation:** Adjust the photon energy (*hν*) fit window using real-time sliders to isolate the linear absorption edge.
- **Live Goodness-of-Fit Metrics:** Displays calculated Optical Band Gap (E<sub>g</sub> in eV), corresponding absorption edge wavelength (λ in nm), and linear regression R² score.
- **Dual Interactive Charts:** Side-by-side Plotly visualizations of the raw UV-Vis Absorbance Spectrum and the extrapolated Tauc Curve.
- **One-Click Data Export:** Download the processed photon energy (*hν*), absorption coefficient (α), and Tauc coordinates as a clean CSV file for reports or manuscripts.

---

## 📐 Theoretical Background & Equations

The optical band gap energy (E<sub>g</sub>) of a semiconductor or nanomaterial is determined using the **Tauc relation**:

> **(αhν)<sup>1/n</sup> = B(hν − E<sub>g</sub>)**

Where:
- **hν** is the incident photon energy in electron-volts (eV), calculated from wavelength λ (nm):
  > **hν = hc / λ ≈ 1240 / λ (nm)**
- **α** is the optical absorption coefficient (cm⁻¹), derived from measured absorbance *A* and sample path length/thickness *d* (cm):
  > **α = (2.303 × A) / d**
- **B** is an energy-independent proportionality constant.
- **n** characterizes the nature of the electronic transition:
  - **n = 1/2** for **direct allowed** transitions → plots *(αhν)²* vs. *hν*
  - **n = 2** for **indirect allowed** transitions → plots *(αhν)<sup>1/2</sup>* vs. *hν*

### Band Gap Extraction
Fitting a linear regression line (*y = mx + c*) to the steep linear absorption edge and extrapolating to the photon-energy axis (*y = 0*) yields the optical band gap:

> **E<sub>g</sub> = −c / m**

---

## 🛠️ Tech Stack

- **Frontend & Hosting:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Scientific Computing:** SciPy (`scipy.stats.linregress`)
- **Interactive Visualization:** Plotly

---

## 💻 Local Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DulsaraPrasad/uvvis-bandgap-analyzer.git](https://github.com/DulsaraPrasad/uvvis-bandgap-analyzer.git)
   cd uvvis-bandgap-analyzer
