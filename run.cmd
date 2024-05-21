@echo off
cd /d "%~dp0"
flask --debug run -h 0.0.0.0 -p 8080