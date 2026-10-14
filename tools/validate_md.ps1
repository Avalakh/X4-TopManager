param([string]$Sources = 'examples/x4_unpacked', [switch]$IncludeNativeCopies)
$ErrorActionPreference = 'Stop'
$taskModRoot = Split-Path $PSScriptRoot -Parent
$taskSchema = [System.Xml.Schema.XmlSchemaSet]::new()
$taskSchema.XmlResolver = [System.Xml.XmlUrlResolver]::new()
$taskSchema.Add($null, (Resolve-Path (Join-Path $Sources 'md/md.xsd')).Path) | Out-Null
$taskSchema.Compile()
$taskSettings = [System.Xml.XmlReaderSettings]::new()
$taskSettings.Schemas = $taskSchema
$taskSettings.ValidationType = [System.Xml.ValidationType]::Schema
$taskSettings.add_ValidationEventHandler({ param($sender, $eventArgs) throw $eventArgs.Message })
$taskDirs = @((Join-Path $taskModRoot 'md'), (Join-Path $taskModRoot 'tests/diagnostics/extension/md'))
if ($IncludeNativeCopies) {
    $taskDirs += (Join-Path $taskModRoot 'native/md')
    $taskDirs += (Join-Path $taskModRoot 'native/adapted/md')
}
foreach ($taskDir in $taskDirs) {
    if (-not (Test-Path -LiteralPath $taskDir)) { continue }
    foreach ($taskFile in (Get-ChildItem -LiteralPath $taskDir -Filter '*.xml' -File)) {
        $taskReader = [System.Xml.XmlReader]::Create($taskFile.FullName, $taskSettings)
        try {
            while ($taskReader.Read()) {}
            Write-Output ('PASS: ' + $taskFile.FullName)
        } finally { $taskReader.Close() }
    }
}
if ($IncludeNativeCopies) {
    $taskAiSchema = [System.Xml.Schema.XmlSchemaSet]::new()
    $taskAiSchema.XmlResolver = [System.Xml.XmlUrlResolver]::new()
    $taskAiSchema.Add($null, (Resolve-Path (Join-Path $Sources 'aiscripts/aiscripts.xsd')).Path) | Out-Null
    $taskAiSchema.Compile()
    $taskAiSettings = [System.Xml.XmlReaderSettings]::new()
    $taskAiSettings.Schemas = $taskAiSchema
    $taskAiSettings.ValidationType = [System.Xml.ValidationType]::Schema
    $taskAiSettings.add_ValidationEventHandler({ param($sender, $eventArgs) throw $eventArgs.Message })
    $taskAiDir = Join-Path $taskModRoot 'native/adapted/aiscripts'
    if (Test-Path -LiteralPath $taskAiDir) {
        foreach ($taskAiFile in (Get-ChildItem -LiteralPath $taskAiDir -Filter '*.xml' -File)) {
            $taskAiReader = [System.Xml.XmlReader]::Create($taskAiFile.FullName, $taskAiSettings)
            try {
                while ($taskAiReader.Read()) {}
                Write-Output ('PASS: ' + $taskAiFile.FullName)
            } finally { $taskAiReader.Close() }
        }
    }
}
& python (Join-Path $PSScriptRoot 'check_md_scheduling.py')
if ($LASTEXITCODE -ne 0) { throw 'MD scheduling safety check failed' }
