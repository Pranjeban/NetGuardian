# Pipeline Automation for Deployment 


Note: Feature --> Main (it is blocked for everyone)
PR Creating in Any Branch -> Triggering PR Pipeline (This will be search for format)


Chnages - 
Function App: "az-rg-1"
```bash
if ($desc -match 'Function App\s*-\s*"([^"]+)"') {
    $functionApp = $matches[1]
    Write-Host "Extracted Function App: $functionApp"
    Write-Host "##vso[task.setvariable variable=functionAppName]$functionApp"
} else {
    Write-Error "No Function App found in PR body"
    exit 1
}
```
## PR template should to be followed:

Chnages Made in <File Name>

To Be Deployed in Fuction App : <App Name>



# CI pipeline is triggered ONLY on PRs targeting the 'main' branch
trigger: none
pr:
  branches:
    include:
      - main

# Use Microsoft-hosted agent with latest Windows image
pool:
  vmImage: 'windows-latest'

# Declare a variable to hold the Function App name (it will be populated later)
variables:
  FUNCTION_NAME: ''

steps:
  # Step 1: PowerShell script to extract Function App name from the PR description
  - task: PowerShell@2
    name: ExtractFunctionApp
    inputs:
      targetType: 'inline'
      script: |
        # Get the Pull Request ID from Azure DevOps predefined variable
        $prId = "$(System.PullRequest.PullRequestId)"

        # Get repository name
        $repo = "$(Build.Repository.Name)"

        # Azure DevOps organization URL
        $orgUrl = "$(System.CollectionUri)"

        # Current project name in Azure DevOps
        $project = "$(System.TeamProject)"

        Write-Host "Fetching PR description..."

        # Use System.AccessToken for authentication
        $token = "$(System.AccessToken)"

        # Create authorization header for REST API
        $headers = @{Authorization = "Bearer $token"}

        # Construct Azure DevOps REST API URL to fetch PR metadata
        $url = "$orgUrl$project/_apis/git/repositories/$repo/pullRequests/$prId?api-version=7.0"

        # Make GET request to fetch PR details
        $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get

        # Extract the PR description
        $description = $response.description

        # Use regex to search for Function App name in the format: Function App - "abc-xyz"
        if ($description -match 'Function App\s*-\s*"(.+?)"') {
          $functionAppName = $matches[1]

          # Set the extracted name as a pipeline variable so that it can be used later
          Write-Host "##vso[task.setvariable variable=FUNCTION_NAME]$functionAppName"
          Write-Host "Function App: $functionAppName"
        } else {
          # Fail the pipeline if Function App name is not found
          Write-Error "Function App name not found in PR description!"
          exit 1
        }

  # Step 2: Publish the pipeline workspace as an artifact named 'drop'
  # This can be used in the release pipeline to access files or variables
  - publish: $(Pipeline.Workspace)
    artifact: drop
