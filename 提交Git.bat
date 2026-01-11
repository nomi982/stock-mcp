@echo off
chcp 65001 >nul

git config --global core.autocrlf true
git add .
git commit -m "更新 AI系统提示词.md"
git branch -M main
git push -u origin main