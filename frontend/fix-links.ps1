# 修复HTML文件中的链接，添加.html后缀
# 排除备份文件和测试文件

$excludePatterns = @('*-backup.html', '*-test*.html', '*-new*.html', '*-v*.html')
$files = Get-ChildItem -Path "." -Filter "*.html" | Where-Object {
    $file = $_
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($file.Name -like $pattern) {
            $exclude = $true
            break
        }
    }
    -not $exclude
}

$linkMapping = @{
    'href="/register"' = 'href="/register.html"'
    'href="/login"' = 'href="/login.html"'
    'href="/survey"' = 'href="/survey.html"'
    'href="/history"' = 'href="/history.html"'
    'href="/admin"' = 'href="/admin.html"'
    'href="/rules"' = 'href="/rules.html"'
    'href="/knowledge"' = 'href="/knowledge.html"'
    'href="/ai-config"' = 'href="/ai-config.html"'
    'href="/customers"' = 'href="/customers.html"'
    'href="/reports"' = 'href="/reports.html"'
    'href="/users"' = 'href="/users.html"'
    'href="/config"' = 'href="/config.html"'
    'href="/report"' = 'href="/report.html"'
    'href="/home"' = 'href="/home.html"'
    'href="/index"' = 'href="/index.html"'
    "href='/register'" = "href='/register.html'"
    "href='/login'" = "href='/login.html'"
    "href='/survey'" = "href='/survey.html'"
    "href='/history'" = "href='/history.html'"
    "href='/admin'" = "href='/admin.html'"
    "href='/rules'" = "href='/rules.html'"
    "href='/knowledge'" = "href='/knowledge.html'"
    "href='/ai-config'" = "href='/ai-config.html'"
    "href='/customers'" = "href='/customers.html'"
    "href='/reports'" = "href='/reports.html'"
    "href='/users'" = "href='/users.html'"
    "href='/config'" = "href='/config.html'"
    "href='/report'" = "href='/report.html'"
    "href='/home'" = "href='/home.html'"
    "href='/index'" = "href='/index.html'"
}

foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)"
    $content = Get-Content -Path $file.FullName -Raw
    $modified = $false
    
    foreach ($oldLink in $linkMapping.Keys) {
        $newLink = $linkMapping[$oldLink]
        if ($content -match [regex]::Escape($oldLink)) {
            $content = $content -replace [regex]::Escape($oldLink), $newLink
            $modified = $true
            Write-Host "  Replaced: $oldLink -> $newLink"
        }
    }
    
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Saved!" -ForegroundColor Green
    } else {
        Write-Host "  No changes needed" -ForegroundColor Gray
    }
}

Write-Host "`nDone! All links have been fixed." -ForegroundColor Cyan
