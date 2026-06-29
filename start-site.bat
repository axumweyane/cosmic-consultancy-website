@echo off
rem Opens the Cosmic Consultancy site directly in your default browser.
rem No server, no Python, no Node required - works on any Windows PC.
cd /d "%~dp0"
start "" "%~dp0index.html"
