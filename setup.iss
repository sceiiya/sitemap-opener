[Setup]
AppName=Sitemap Opener
AppVersion=1.0
DefaultDirName={autopf}\Sitemap Opener
DefaultGroupName=Sitemap Opener
OutputDir=.\installer
OutputBaseFilename=SitemapOpenerSetup
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Sitemap Opener.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sitemap Opener"; Filename: "{app}\Sitemap Opener.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{autodesktop}\Sitemap Opener"; Filename: "{app}\Sitemap Opener.exe"; IconFilename: "{app}\app_icon.ico"