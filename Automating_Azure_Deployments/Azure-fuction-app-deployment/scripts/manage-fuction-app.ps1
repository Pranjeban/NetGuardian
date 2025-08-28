param (
    [string]$FunctionApp
)

try {
    Write-Host "Function App to enable: $FunctionApp"
    
    $apps = az functionapp list --query "[].name" -o tsv

    foreach ($app in $apps) {
        if ($app -eq $FunctionApp) {
            Write-Host "Enabling $app..."
            az functionapp start --name $app --resource-group "<your-rg-name>"
        } else {
            Write-Host "Disabling $app..."
            az functionapp stop --name $app --resource-group "<your-rg-name>"
        }
    }

    Write-Host "Function App management completed."
}
catch {
    Write-Error "Failed: $_"
    Write-Host "##vso[task.logissue type=error]$($_.Exception.Message)"
    Write-Host "##vso[task.complete result=Failed;]"
}
