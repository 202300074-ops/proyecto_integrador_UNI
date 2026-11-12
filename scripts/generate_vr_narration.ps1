param(
  [string]$OutputPath = (Join-Path $PSScriptRoot "..\assets\audio\narracion-recorrido-vr.wav")
)

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$outputDirectory = Split-Path -Parent $resolvedOutput
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$text = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(
  'QmllbnZlbmlkbyBhbCBtZWxpcG9uYXJpbyBkZSBTYWsgUCdvJyBLYWFiLiBFc3RlIGVzcGFjaW8gcmXDum5lIGpvYm9uZXMsIGZsb3JlcyB5IGZhdW5hIGRlIGphcmTDrW4gYWxyZWRlZG9yIGRlIGxhcyBhYmVqYXMgbWVsaXBvbmFzLCBwb2xpbml6YWRvcmFzIG5hdGl2YXMgc2luIGFndWlqw7NuLiBPYnNlcnZhIGPDs21vIGxhcyBhYmVqYXMgdmlzaXRhbiBkaXN0aW50YXMgZmxvcmVzIHkgYXl1ZGFuIGFsIHRyYW5zcG9ydGUgZGVsIHBvbGVuLiBMb3Mgam9ib25lcyBvZnJlY2VuIGNhdmlkYWRlcyBwcm90ZWdpZGFzIHBhcmEgc3VzIGNvbG9uaWFzLiBFbCBjdWlkYWRvIGRlbCBow6FiaXRhdCB5IGVsIGNvbm9jaW1pZW50byBjb211bml0YXJpbyBheXVkYW4gYSBtYW50ZW5lciBlc3RhIHJlbGFjacOzbjsgbGFzIHByw6FjdGljYXMgdmFyw61hbiBlbnRyZSBjb211bmlkYWRlcy4gQWPDqXJjYXRlIGEgbG9zIHB1bnRvcyBkb3JhZG9zIHBhcmEgZXhwbG9yYXIuIEVzdGEgZXNjZW5hIGVzIHVuYSByZWNyZWFjacOzbiBlZHVjYXRpdmEsIG5vIHJlcHJlc2VudGEgdW4gc2l0aW8gcmVhbC4='
))

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  $voice = $synth.GetInstalledVoices() |
    Where-Object { $_.VoiceInfo.Name -eq 'Microsoft Sabina Desktop' } |
    Select-Object -First 1
  if (-not $voice) {
    throw 'No se encontró la voz Microsoft Sabina Desktop (es-MX).'
  }

  $synth.SelectVoice($voice.VoiceInfo.Name)
  $synth.Rate = -1
  $synth.Volume = 96
  $synth.SetOutputToWaveFile($resolvedOutput)
  $synth.Speak($text)
  $synth.SetOutputToNull()
} finally {
  $synth.Dispose()
}

Get-Item -LiteralPath $resolvedOutput | Select-Object FullName, Length
