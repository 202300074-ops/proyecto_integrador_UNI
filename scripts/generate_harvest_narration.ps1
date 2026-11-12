param(
  [string]$OutputPath = (Join-Path $PSScriptRoot "..\assets\audio\narracion-cosecha.wav")
)

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
$outputDirectory = Split-Path -Parent $resolvedOutput
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

# PowerShell 5.1 may read a UTF-8 script without BOM as ANSI; decode narration bytes explicitly.
$text = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String(
  'RW4gWXVjYXTDoW4sIGFsZ3VuYXMgZmFtaWxpYXMgY3VpZGFuIGEgbGEgWHVuw6FhbiBLYWFiIGVuIGpvYm9uZXM6IHRyb25jb3MgaHVlY29zIHF1ZSBwcm90ZWdlbiBsYSBjb2xvbmlhIHkgc3VzIHJlc2VydmFzLiBBbnRlcyBkZSBjb3NlY2hhciwgcHJlcGFyYW4gdW4gZXNwYWNpbyBsaW1waW8geSByZXZpc2FuIGVsIG5pZG8gY29uIHBhY2llbmNpYS4gQWJyZW4gZWwgam9iw7NuIGNvbiBjdWlkYWRvIHBhcmEgbG9jYWxpemFyIGxvcyBwb3RlcyBkZSBtaWVsLCBwb2xlbiB5IGNyw61hLiBFbiBlc3RlIGVqZW1wbG8sIHBlcmZvcmFuIGFsZ3Vub3MgcG90ZXMgbWFkdXJvcyBlIGluY2xpbmFuIGVsIGpvYsOzbi4gTGEgbWllbCBlc2N1cnJlIHBvciBncmF2ZWRhZDsgbm8gc2UgY2VudHJpZnVnYS4gTGEgbWllbCBzZSBmaWx0cmEgY29uIG1hbGxhIGxpbXBpYSB5IHNlIGVudmFzYS4gRGVzcHXDqXMsIGxpbXBpYW4geSB2dWVsdmVuIGEgc2VsbGFyIGVsIGpvYsOzbi4gU2UgZGVqYW4gcG90ZXMgaW50YWN0b3MgY29tbyByZXNlcnZhLiBMYXMgcHLDoWN0aWNhcyB2YXLDrWFuIGVudHJlIGNvbXVuaWRhZGVzLiBFc3RhIGFuaW1hY2nDs24gZXMgdW5hIHJlY3JlYWNpw7NuIGRpZMOhY3RpY2EsIG5vIG1ldHJhamUgZG9jdW1lbnRhbC4='
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
