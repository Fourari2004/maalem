# Stop any existing servers
Write-Host "Stopping any existing servers..." -ForegroundColor Yellow
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue

# Get the current directory
$currentDir = Get-Location

# Start backend server
Write-Host "Starting Django Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$currentDir\maalem-backend'; python manage.py runserver" -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start frontend server
Write-Host "Starting React Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$currentDir\maalem-frontend'; npm run dev" -WindowStyle Normal

Write-Host "Servers started!" -ForegroundColor Cyan
Write-Host "Django Backend: http://localhost:8000" -ForegroundColor White
Write-Host "React Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "API Endpoint: http://localhost:8000/api/" -ForegroundColor White
Write-Host ""
Write-Host "If you have connection issues:" -ForegroundColor Yellow
Write-Host "1. Check that both terminals remain open" -ForegroundColor Yellow
Write-Host "2. Verify the .env file in maalem-frontend has VITE_API_URL=http://localhost:8000/api" -ForegroundColor Yellow
Write-Host "3. Make sure no firewall is blocking the connections" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")