using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace App
{
	public class Form1 : Form
	{
		private IContainer components;

		public Form1()
		{
			InitializeComponent();
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
			base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new System.Drawing.Size(800, 450);
			Text = "Form1";
		}
	}
}
