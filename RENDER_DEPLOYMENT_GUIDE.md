# Render Deployment Settings Guide for Symptom Triage API

## Overview
This guide provides the exact settings needed to deploy your FastAPI symptom triage application on Render. These settings are derived from your code structure and requirements.

## Environment Variables
Set the following environment variable in Render:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `JWT_SECRET` | `supersecret` | Secret key for JWT token authentication (change this to a secure value in production) |

## Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Python Version**: 3.9 or higher (recommended: 3.11)

## Start Settings
- **Start Command**: `./start.sh`

## Health Check Settings
- **Health Check Path**: `/healthz`
- **Health Check Timeout**: 30 seconds (default)

## Runtime Settings
- **Instance Type**: Starter (Free) or Standard (Paid)
- **Region**: Choose the region closest to your users

## File Structure Verification
Ensure your project has these files before deployment:

```
/symptom-triage/
├── requirements.txt
├── start.sh
├── src/
│   ├── __init__.py
│   ├── app.py
│   └── ... (other Python files)
├── models/
│   ├── model.joblib
│   └── vectorizer.joblib
├── data/
│   └── raw.csv
└── .env (optional for local development)
```

## Deployment Steps

1. **Connect Repository**: Link your GitHub repository to Render
2. **Set Environment Variables**: Add `JWT_SECRET` as shown above
3. **Configure Build & Start**: Use the commands specified above
4. **Set Health Check**: Configure `/healthz` path
5. **Deploy**: Trigger deployment and monitor logs

## API Endpoints After Deployment
Once deployed, your API will be available at:
- `https://your-app-name.onrender.com/healthz` - Health check
- `https://your-app-name.onrender.com/get-token` - Get JWT token
- `https://your-app-name.onrender.com/predict` - Symptom prediction (requires JWT token)

## Troubleshooting
- If deployment fails, check the build logs for missing dependencies
- Ensure `start.sh` has execute permissions: `chmod +x start.sh`
- Verify that model files exist in the `models/` directory
- Check that all required environment variables are set

## Security Notes
- Change `JWT_SECRET` to a strong, random value in production
- Consider adding rate limiting for the prediction endpoint
- Monitor API usage and costs on Render dashboard
