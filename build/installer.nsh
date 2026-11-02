!macro customInstall
  Delete "$DESKTOP\AI模拟面试平台.lnk"
  CreateShortCut "$DESKTOP\AI模拟面试平台.lnk" "$INSTDIR\AI模拟面试平台.exe" "" "$INSTDIR\AI模拟面试平台.exe" 0

  Delete "$SMPROGRAMS\AI模拟面试平台.lnk"
  CreateShortCut "$SMPROGRAMS\AI模拟面试平台.lnk" "$INSTDIR\AI模拟面试平台.exe" "" "$INSTDIR\AI模拟面试平台.exe" 0
!macroend
