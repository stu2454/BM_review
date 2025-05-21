# AT Benchmark Explorer

A Streamlit-based interactive tool for visualising Assistive-Technology (AT) payment benchmarks, comparing current vs. proposed benchmarks against policy-driven cost tiers and positional "windows of concern." Simulated payment distributions (Normal, Log-normal, Gamma) can be overlaid to assess how typical payments align with funding increments.

## Features

* **Dynamic dual-marker plot:** Overlay *current* (red) and *proposed* (green) benchmark points on a single number-line diagram.
* **Tier shading:** Light-blue (low-cost), light-green (mid-cost), light-orange (high-cost) zones.
* **Positional windows:** ± window half-widths around \$0, \$5k, \$10k, and \$15k increments, configurable per tier.
* **Simulated distributions:** Choose Normal, Log-normal, or Gamma; moment-matched to your summary stats; truncated to your min/max bounds.
* **Advanced stats inputs:** Enter mean, median, percentiles (25th, 75th, 90th), standard deviation, skewness, kurtosis, plus bucket counts.
* **Responsive layout:** Single vertical view; sidebar controls for all parameters; responsive X-axis scaling or manual limit.

## Getting Started

### Prerequisites

* Docker Engine & Docker Compose
* (Optional) Python 3.11+ and pip for native runs

### Repository Structure

```text
├── app.py                # Streamlit application
├── at_visuals.py         # Plot helper functions
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container spec
├── docker-compose.yml    # Compose orchestration
└── README.md             # This file
```

## Installation & Usage

### 1. Docker Compose (Recommended)

```bash
# Build and start the app
docker compose up --build
```

The app will be available at [http://localhost:8501](http://localhost:8501)

To rebuild after code changes:

```bash
docker compose up --build
```

To stop and remove containers:

```bash
docker compose down
```

### 2. Native Python (Optional)

```bash
git clone <your-repo-url>
cd at-benchmark-explorer
python3 -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

Browse [http://localhost:8501](http://localhost:8501)

## Configuration & Secrets

If you need to store API keys or private settings, create `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
API_TOKEN = "your_token_here"
```

Access via `st.secrets.API_TOKEN` in your code.

## Deployment to Streamlit Cloud

1. Push this repository to GitHub.
2. On Streamlit Cloud, **New app** → connect your repo → select branch `main` → set main file `app.py`.
3. Click **Deploy**; the service will respect your `docker-compose.yml`.

## Customisation

* **Window sizes:** Adjust low/mid/high half-widths in the sidebar.
* **X-axis limit:** Choose manual or auto-scaling in sidebar.
* **Distribution family:** Switch between Normal, Log-normal, or Gamma.

## Troubleshooting

* **Port conflicts:** Change port in `docker-compose.yml` under `services.benchmark-app.ports`.
* **Rebuild issues:** `docker compose up --build --force-recreate`
* **Streamlit cache:** Clear via `streamlit cache clear` for native runs.

## License

MIT © Your Organisation

