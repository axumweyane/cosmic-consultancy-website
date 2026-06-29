@echo off
cd /d "%~dp0"
echo ============================================================
echo  Pushing Cosmic Consultancy website to GitHub
echo  Repo: https://github.com/axumweyane/cosmic-consultancy-website
echo ============================================================
echo.

rem --- Check Git is installed ---
where git >nul 2>nul
if errorlevel 1 (
    echo.
    echo  ^>^>  GIT IS NOT INSTALLED.
    echo  Download it from https://git-scm.com/download/win
    echo  Install it ^(click Next through the installer^), then run this file again.
    echo.
    pause
    exit /b
)

rem --- Remove any leftover/broken repo so we start clean ---
if exist ".git" (
    echo Cleaning up previous .git folder...
    rmdir /s /q ".git"
)

rem --- Fresh init ---
git init
git config user.name  "axumweyane"
git config user.email "axumweyane@gmail.com"

rem --- Stage and commit ---
git add .
git commit -m "Initial commit: Cosmic Consultancy website"

rem --- Branch + remote ---
git branch -M main
git remote add origin https://github.com/axumweyane/cosmic-consultancy-website.git

rem --- Push (a GitHub sign-in window may appear the first time) ---
echo.
echo Pushing... if a GitHub sign-in window appears, approve it.
echo.
git push -u origin main

echo.
echo ============================================================
echo  If you see no red errors above, it worked.
echo  Refresh your GitHub repo page to see the files.
echo ============================================================
pause
