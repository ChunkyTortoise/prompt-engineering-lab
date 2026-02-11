# Streamlit Cloud Deployment Guide

This guide covers deploying the Prompt Engineering Lab to Streamlit Cloud.

## Prerequisites

- GitHub account
- Repository pushed to GitHub (`ChunkyTortoise/prompt-engineering-lab`)
- Streamlit Cloud account (free tier available)

## Quick Deploy

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=ChunkyTortoise/prompt-engineering-lab&branch=main&fileName=app.py)

## Manual Deployment Steps

### 1. Push to GitHub

Ensure your code is pushed to the GitHub repository:

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Create Streamlit Cloud App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select:
   - **Repository**: `ChunkyTortoise/prompt-engineering-lab`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **Custom subdomain**: `ct-prompt-lab`
5. Click "Deploy"

## Project Structure for Deployment

```
prompt-engineering-lab/
├── app.py                # Entry point for Streamlit Cloud
├── requirements.txt      # Python dependencies (includes -e . for local package)
├── pyproject.toml        # Package configuration
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── prompt_lab/           # Core package used by app.py
│   ├── __init__.py
│   ├── patterns.py
│   ├── evaluator.py
│   ├── ab_tester.py
│   ├── benchmark.py
│   ├── categories.py
│   └── report_generator.py
└── prompt_engineering_lab/  # CLI and extended modules
    ├── __init__.py
    └── ...
```

## How It Works

1. **Entry Point**: Streamlit Cloud runs `app.py`
2. **Dependencies**: `requirements.txt` installs core deps; `-e .` installs local packages
3. **No API Keys Required**: The app uses local evaluation logic -- no external LLM calls needed
4. **Features**: Pattern library, prompt evaluation, A/B comparison, benchmarks

## Local Development

```bash
# Clone the repository
git clone https://github.com/ChunkyTortoise/prompt-engineering-lab.git
cd prompt-engineering-lab

# Install dependencies
pip install -e ".[dev]"

# Run the Streamlit app
streamlit run app.py
```

## Troubleshooting

### App won't start
- Check that `app.py` exists in the root directory
- Verify `requirements.txt` has `-e .` to install local packages
- Check Streamlit Cloud logs for import errors

### Import errors
- Ensure `prompt_lab/` directory has `__init__.py`
- The package is installed via `-e .` in requirements.txt

## Updating the Deployment

Any push to the `main` branch automatically triggers a redeploy on Streamlit Cloud.

```bash
git add .
git commit -m "Update app"
git push origin main
```

## Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Prompt Engineering Lab README](./README.md)
- [Streamlit App URL](https://ct-prompt-lab.streamlit.app)
