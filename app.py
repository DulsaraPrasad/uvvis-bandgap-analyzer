import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import linregress

# Page configuration
st.set_page_config(page_title="UV-Vis Tauc Plot & Band Gap Analyzer", layout="wide")

st.title("🔬 UV-Vis Spectroscopy: Tauc Plot & Band Gap ($E_g$) Analyzer")
st.markdown(
    "Upload your UV-Vis absorbance spectrum (CSV/Excel) to automatically generate a **Tauc Plot** "
    "and extract the **Optical Band Gap ($E_g$)** via linear regression."
)

# Sidebar controls
st.sidebar.header("1. Data Input")
use_sample = st.sidebar.checkbox("Use built-in Sample Data (ZnO Nanoparticles)", value=True)
uploaded_file = st.sidebar.file_uploader("Or upload CSV / Excel file", type=["csv", "xlsx"])

# Generate realistic synthetic ZnO UV-Vis data for testing/demo
def get_sample_data():
    wavelength = np.linspace(250, 700, 451)  # 250 nm to 700 nm
    hv = 1240.0 / wavelength
    # Simulate absorption edge around 3.25 eV (~381 nm)
    absorbance = 0.05 + 1.8 / (1 + np.exp(-15 * (hv - 3.28)))
    # Add slight realistic instrument noise
    np.random.seed(42)
    absorbance += np.random.normal(0, 0.005, size=wavelength.shape)
    absorbance = np.clip(absorbance, 0.001, None)
    return pd.DataFrame({"Wavelength (nm)": wavelength, "Absorbance (a.u.)": absorbance})

df = None
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
elif use_sample:
    df = get_sample_data()

if df is not None:
    st.sidebar.header("2. Column Mapping")
    cols = df.columns.tolist()
    wl_col = st.sidebar.selectbox("Wavelength Column (nm)", cols, index=0)
    abs_col = st.sidebar.selectbox("Absorbance Column", cols, index=min(1, len(cols) - 1))

    st.sidebar.header("3. Tauc Parameters")
    transition_type = st.sidebar.radio(
        "Electronic Transition Type",
        [
            "Direct Allowed (n = 1/2) → (αhν)²",
            "Indirect Allowed (n = 2) → (αhν)^(1/2)",
        ],
    )
    thickness_cm = st.sidebar.number_input(
        "Sample Thickness d (cm) [Optional]", min_value=0.0001, value=1.0, format="%.4f"
    )

    # Clean data & calculate Tauc parameters
    data = df[[wl_col, abs_col]].dropna().copy()
    data.columns = ["wavelength", "absorbance"]
    data = data[data["wavelength"] > 0]
    data = data.sort_values("wavelength")

    # Photon energy hv (eV)
    data["hv"] = 1240.0 / data["wavelength"]
    # Absorption coefficient alpha (cm^-1)
    data["alpha"] = (2.303 * data["absorbance"]) / thickness_cm

    if "Direct" in transition_type:
        data["tauc_y"] = (data["alpha"] * data["hv"]) ** 2
        y_label = "(αhν)² (eV·cm⁻¹)²"
    else:
        data["tauc_y"] = np.sqrt(np.maximum(data["alpha"] * data["hv"], 0))
        y_label = "(αhν)^(1/2) (eV·cm⁻¹)^(1/2)"

    # Sort by photon energy for plotting
    data = data.sort_values("hv")

    st.sidebar.header("4. Linear Fit Region (eV)")
    min_hv, max_hv = float(data["hv"].min()), float(data["hv"].max())
    default_low = min(max(3.15, min_hv), max_hv - 0.1)
    default_high = min(max(3.38, default_low + 0.05), max_hv)

    fit_range = st.sidebar.slider(
        "Select linear absorption edge range (eV)",
        min_value=round(min_hv, 2),
        max_value=round(max_hv, 2),
        value=(round(default_low, 2), round(default_high, 2)),
        step=0.01,
    )

    # Filter data inside selected linear region
    fit_df = data[(data["hv"] >= fit_range[0]) & (data["hv"] <= fit_range[1])]

    eg_value = None
    r_squared = None
    slope, intercept = None, None

    if len(fit_df) >= 2:
        res = linregress(fit_df["hv"], fit_df["tauc_y"])
        slope = res.slope
        intercept = res.intercept
        r_squared = res.rvalue ** 2
        if slope > 0:
            eg_value = -intercept / slope

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        if eg_value is not None and eg_value > 0:
            st.metric("Calculated Band Gap (Eg)", f"{eg_value:.3f} eV")
        else:
            st.metric("Calculated Band Gap (Eg)", "Adjust Fit Range")
    with col2:
        st.metric("Linear Fit R²", f"{r_squared:.4f}" if r_squared is not None else "N/A")
    with col3:
        if eg_value is not None and eg_value > 0:
            st.metric("Corresponding Edge λ", f"{1240.0 / eg_value:.1f} nm")
        else:
            st.metric("Corresponding Edge λ", "N/A")

    # Plotting Row
    plot_col1, plot_col2 = st.columns(2)

    with plot_col1:
        fig_abs = go.Figure()
        fig_abs.add_trace(
            go.Scatter(
                x=data["wavelength"],
                y=data["absorbance"],
                mode="lines",
                name="Absorbance",
                line=dict(color="#2563EB", width=2),
            )
        )
        fig_abs.update_layout(
            title="UV-Vis Absorption Spectrum",
            xaxis_title="Wavelength λ (nm)",
            yaxis_title="Absorbance (a.u.)",
            template="plotly_white",
            height=450,
        )
        st.plotly_chart(fig_abs, use_container_width=True)

    with plot_col2:
        fig_tauc = go.Figure()
        # Full Tauc Curve
        fig_tauc.add_trace(
            go.Scatter(
                x=data["hv"],
                y=data["tauc_y"],
                mode="lines",
                name="Tauc Curve",
                line=dict(color="#0F172A", width=2),
            )
        )
        # Highlighted fit points
        fig_tauc.add_trace(
            go.Scatter(
                x=fit_df["hv"],
                y=fit_df["tauc_y"],
                mode="markers",
                name="Selected Linear Region",
                marker=dict(color="#16A34A", size=6),
            )
        )
        # Extrapolated tangent line down to y = 0
        if eg_value is not None and eg_value > 0:
            x_line = np.linspace(eg_value, fit_range[1], 50)
            y_line = slope * x_line + intercept
            fig_tauc.add_trace(
                go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    name=f"Tangent Fit (Eg = {eg_value:.3f} eV)",
                    line=dict(color="#DC2626", width=2, dash="dash"),
                )
            )
            # Mark Eg intercept point on x-axis
            fig_tauc.add_trace(
                go.Scatter(
                    x=[eg_value],
                    y=[0],
                    mode="markers+text",
                    name="Band Gap (Eg)",
                    text=[f"Eg = {eg_value:.3f} eV"],
                    textposition="top left",
                    marker=dict(color="#DC2626", size=10, symbol="diamond"),
                )
            )

        fig_tauc.update_layout(
            title="Tauc Plot & Linear Extrapolation",
            xaxis_title="Photon Energy hν (eV)",
            yaxis_title=y_label,
            template="plotly_white",
            height=450,
        )
        st.plotly_chart(fig_tauc, use_container_width=True)

    # Download processed data
    csv_export = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Processed Tauc Data (CSV)",
        data=csv_export,
        file_name="tauc_plot_results.csv",
        mime="text/csv",
    )
else:
    st.info("👈 Upload a UV-Vis CSV/Excel file from the sidebar or check 'Use built-in Sample Data' to start.")