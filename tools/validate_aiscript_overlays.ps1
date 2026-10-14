param([string]$Sources = 'examples/x4_unpacked', [string[]]$ForeignOverlays = @(), [switch]$ForeignLast)
$ErrorActionPreference = 'Stop'
$taskModRoot = Split-Path $PSScriptRoot -Parent
$taskSchemas = [System.Xml.Schema.XmlSchemaSet]::new()
$taskSchemas.XmlResolver = [System.Xml.XmlUrlResolver]::new()
$taskSchemas.Add($null, (Resolve-Path (Join-Path $Sources 'aiscripts/aiscripts.xsd')).Path) | Out-Null
$taskSchemas.Compile()
foreach ($taskPatchFile in Get-ChildItem -LiteralPath (Join-Path $taskModRoot 'aiscripts') -Filter '*.xml' -File) {
    $taskNativePath = Join-Path $Sources ('aiscripts/' + $taskPatchFile.Name)
    $taskNativeHash = (Get-FileHash -LiteralPath $taskNativePath -Algorithm SHA256).Hash
    $taskNative = [System.Xml.XmlDocument]::new()
    $taskNative.Load((Resolve-Path -LiteralPath $taskNativePath).Path)
    $taskPatchPaths = @($taskPatchFile.FullName)
    $taskForeignHashes = @{}
    foreach ($taskForeignPath in $ForeignOverlays) {
        if ((Split-Path $taskForeignPath -Leaf) -ne $taskPatchFile.Name) { continue }
        $taskForeignHashes[$taskForeignPath] = (Get-FileHash -LiteralPath $taskForeignPath -Algorithm SHA256).Hash
        if ($ForeignLast) { $taskPatchPaths += $taskForeignPath }
        else { $taskPatchPaths = @($taskForeignPath) + $taskPatchPaths }
    }
    foreach ($taskPatchPath in $taskPatchPaths) {
      $taskPatch = [System.Xml.XmlDocument]::new()
      $taskPatch.Load((Resolve-Path -LiteralPath $taskPatchPath).Path)
      foreach ($taskOperation in $taskPatch.DocumentElement.ChildNodes) {
        if ($taskOperation.NodeType -ne [System.Xml.XmlNodeType]::Element) { continue }
        $taskMatches = $taskNative.SelectNodes($taskOperation.sel)
        if ($taskMatches.Count -ne 1) { throw ('Expected one native boundary: ' + $taskOperation.sel) }
        $taskAnchor = $taskMatches[0]
        if ($taskOperation.Name -eq 'replace' -and $taskAnchor.NodeType -eq [System.Xml.XmlNodeType]::Attribute) {
            $taskAnchor.Value = $taskOperation.InnerText
            continue
        }
        if ($taskOperation.Name -ne 'add' -or $taskOperation.pos -notin @('before', 'after')) {
            throw 'Unsupported overlay operation; extend validation before use'
        }
        foreach ($taskChild in $taskOperation.ChildNodes) {
            $taskImported = $taskNative.ImportNode($taskChild, $true)
            if ($taskOperation.pos -eq 'before') {
                $taskAnchor.ParentNode.InsertBefore($taskImported, $taskAnchor) | Out-Null
            } else {
                $taskAnchor.ParentNode.InsertAfter($taskImported, $taskAnchor) | Out-Null
                $taskAnchor = $taskImported
            }
        }
      }
    }
    foreach ($taskForeignPath in $taskForeignHashes.Keys) {
        if ((Get-FileHash -LiteralPath $taskForeignPath -Algorithm SHA256).Hash -ne $taskForeignHashes[$taskForeignPath]) {
            throw 'Foreign source changed during validation'
        }
    }
    # Native expression attributes can contain literal line breaks. Normalize
    # them only in this in-memory validation copy, as XML attribute whitespace.
    foreach ($taskAttribute in $taskNative.SelectNodes('//@*')) {
        $taskAttribute.Value = $taskAttribute.Value -replace '[\r\n\t]', ' '
    }
    $taskNative.Schemas = $taskSchemas
    $taskNative.Validate({ param($sender, $eventArgs) throw $eventArgs.Message })
    if ((Get-FileHash -LiteralPath $taskNativePath -Algorithm SHA256).Hash -ne $taskNativeHash) {
        throw 'Native source changed during validation'
    }
    Write-Output ('PASS: native selectors, merged XSD, unchanged source: ' + $taskPatchFile.Name)
}
