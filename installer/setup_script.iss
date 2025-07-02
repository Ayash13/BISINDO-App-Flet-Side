; Inno Setup Script for BisindoApp

[Setup]
AppName={cm:AppName}
AppVersion=1.0
AppPublisher=Ayash
DefaultDirName={autopf}\{cm:AppName}
DefaultGroupName={cm:AppName}
OutputBaseFilename=BisindoApp-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UsePreviousLanguage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
AppName=Bisindo App
OBSInstallBody=PENTING: Setup akan mengunduh dan menginstal OBS Studio, proses ini memerlukan koneksi internet, tunggu hingga selesai.
WingetStatus=Mengunduh dan menginstal OBS Studio (memerlukan internet)...

[Files]
Source: "BisindoApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{cm:AppName}"; Filename: "{app}\BisindoApp.exe"
Name: "{autodesktop}\{cm:AppName}"; Filename: "{app}\BisindoApp.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Buat ikon di Desktop"; GroupDescription: "Pintasan Tambahan";

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
  begin
    MsgBox(ExpandConstant('{cm:OBSInstallBody}'), mbInformation, MB_OK);
    WizardForm.ProgressGauge.Style := npbstMarquee;
  end;
end;

[Run]
Filename: "{cmd}"; Parameters: "/C winget install -e --id OBSProject.OBSStudio --accept-source-agreements --accept-package-agreements"; Flags: waituntilterminated runhidden; StatusMsg: "{cm:WingetStatus}";