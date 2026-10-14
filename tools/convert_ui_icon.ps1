param([Parameter(Mandatory)][string]$Source, [Parameter(Mandatory)][string]$Destination)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$taskInput = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $Source).Path)
$taskIcon = [System.Drawing.Bitmap]::new(128, 128, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
try {
    $taskGraphics = [System.Drawing.Graphics]::FromImage($taskIcon)
    try {
        $taskGraphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
        $taskGraphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $taskGraphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $taskGraphics.DrawImage($taskInput, [System.Drawing.Rectangle]::new(0, 0, 128, 128))
    } finally { $taskGraphics.Dispose() }
    $taskPixels = [byte[]]::new(128 * 128 * 4)
    $taskLock = $taskIcon.LockBits([System.Drawing.Rectangle]::new(0, 0, 128, 128),
        [System.Drawing.Imaging.ImageLockMode]::ReadOnly, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    try {
        if ($taskLock.Stride -ne 512) { throw 'Unexpected bitmap stride' }
        [System.Runtime.InteropServices.Marshal]::Copy($taskLock.Scan0, $taskPixels, 0, $taskPixels.Length)
    } finally { $taskIcon.UnlockBits($taskLock) }
    # Native UI .gz is a gzip-compressed DDS, referenced as .tga in icons.xml.
    # DDS header: uncompressed BGRA8 with alpha. No creative image changes.
    $taskMemory = [System.IO.MemoryStream]::new()
    $taskWriter = [System.IO.BinaryWriter]::new($taskMemory)
    try {
        $taskWriter.Write([System.Text.Encoding]::ASCII.GetBytes('DDS '))
        $taskHeader = [uint32[]]@(124, 0x100f, 128, 128, 512, 0, 0,
            0,0,0,0,0,0,0,0,0,0,0,
            32, 0x41, 0, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 4278190080,
            0x1000, 0, 0, 0, 0)
        if ($taskHeader.Count -ne 31) { throw 'Invalid DDS header' }
        foreach ($taskWord in $taskHeader) { $taskWriter.Write($taskWord) }
        $taskWriter.Write($taskPixels)
        $taskWriter.Flush()
        $taskOutput = [System.IO.Path]::GetFullPath($Destination)
        [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($taskOutput)) | Out-Null
        $taskFile = [System.IO.File]::Create($taskOutput)
        try {
            $taskGzip = [System.IO.Compression.GZipStream]::new($taskFile, [System.IO.Compression.CompressionLevel]::Optimal)
            try { $taskGzip.Write($taskMemory.ToArray()) } finally { $taskGzip.Dispose() }
        } finally { $taskFile.Dispose() }
        Write-Output ('Encoded 128x128 RGBA icon: ' + $taskOutput)
    } finally { $taskWriter.Dispose(); $taskMemory.Dispose() }
} finally { $taskIcon.Dispose(); $taskInput.Dispose() }
