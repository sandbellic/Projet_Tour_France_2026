#ifndef MyAppVersion
#define MyAppVersion "0.0.0"
#endif

[Setup]
AppName=Tour de France
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\TourFrance
DefaultGroupName=Tour de France

OutputDir=..\dist
OutputBaseFilename=TourFrance-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\dist\tour-france.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Tour de France"; Filename: "{app}\tour-france.exe"
Name: "{autodesktop}\Tour de France"; Filename: "{app}\tour-france.exe"

[Run]
Filename: "{app}\tour-france.exe"; Description: "Lancer Appli tour de France"; Flags: nowait postinstall skipifsilent
