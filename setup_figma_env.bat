@echo off
echo Setting up Figma MCP Environment Variables
echo =========================================

echo.
echo To get your Figma Personal Access Token:
echo 1. Go to Figma.com and log in
echo 2. Go to Settings > Personal Access Tokens
echo 3. Generate a new token
echo.

echo To get your Figma File Key:
echo 1. Open your Figma file in browser
echo 2. Copy the file ID from URL: figma.com/file/[FILE_KEY]/...
echo.

set /p FIGMA_PAT=Enter your Figma Personal Access Token: 
set /p FIGMA_FILE_KEY=Enter your Figma File Key: 

echo.
echo Setting environment variables...
setx FIGMA_PAT "%FIGMA_PAT%"
setx FIGMA_FILE_KEY "%FIGMA_FILE_KEY%"

echo.
echo Environment variables set! Restart VS Code for changes to take effect.
echo You can now use the Figma MCP server in AI Toolkit.
pause