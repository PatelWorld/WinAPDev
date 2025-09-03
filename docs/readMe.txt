https://windows.php.net/downloads/releases/php-8.4.5-Win32-vs17-x64.zip
https://archive.mariadb.org///mariadb-11.4.4/winx64-packages/mariadb-11.4.4-winx64.zip
https://www.apachelounge.com/download/VS17/binaries/httpd-2.4.63-250207-win64-VS17.zip
https://download.visualstudio.microsoft.com/download/pr/285b28c7-3cf9-47fb-9be8-01cf5323a8df/8F9FB1B3CFE6E5092CF1225ECD6659DAB7CE50B8BF935CB79BFEDE1F3C895240/VC_redist.x64.exe

In case of issue in installing packages (error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/)
Please follow the below command
.\src\prerequisite\vs_BuildTools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools