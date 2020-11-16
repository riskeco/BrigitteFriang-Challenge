using System;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using Main.Tools;

namespace Main
{
	public class FormEncryptedFiles : Form
	{
		private IContainer components;

		private DataGridView dataGridViewEncryptedFiles;

		private DataGridViewTextBoxColumn ColumnDeleted;

		private DataGridViewTextBoxColumn ColumnPath;

		public FormEncryptedFiles()
		{
			InitializeComponent();
		}

		private void FormEncryptedFiles_Load(object sender, EventArgs e)
		{
			foreach (string encryptedFile in Locker.GetEncryptedFiles())
			{
				if (File.Exists(encryptedFile + ".evil"))
				{
					dataGridViewEncryptedFiles.Rows.Add("", encryptedFile);
				}
				else
				{
					dataGridViewEncryptedFiles.Rows.Add("YES", encryptedFile);
				}
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
			dataGridViewEncryptedFiles = new System.Windows.Forms.DataGridView();
			ColumnDeleted = new System.Windows.Forms.DataGridViewTextBoxColumn();
			ColumnPath = new System.Windows.Forms.DataGridViewTextBoxColumn();
			((System.ComponentModel.ISupportInitialize)dataGridViewEncryptedFiles).BeginInit();
			SuspendLayout();
			dataGridViewEncryptedFiles.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
			dataGridViewEncryptedFiles.Columns.AddRange(ColumnDeleted, ColumnPath);
			dataGridViewEncryptedFiles.Dock = System.Windows.Forms.DockStyle.Fill;
			dataGridViewEncryptedFiles.Location = new System.Drawing.Point(0, 0);
			dataGridViewEncryptedFiles.Name = "dataGridViewEncryptedFiles";
			dataGridViewEncryptedFiles.Size = new System.Drawing.Size(594, 326);
			dataGridViewEncryptedFiles.TabIndex = 0;
			ColumnDeleted.HeaderText = "Deleted";
			ColumnDeleted.Name = "ColumnDeleted";
			ColumnDeleted.ReadOnly = true;
			ColumnDeleted.Width = 50;
			ColumnPath.HeaderText = "Path";
			ColumnPath.Name = "ColumnPath";
			ColumnPath.ReadOnly = true;
			ColumnPath.Width = 500;
			base.AutoScaleDimensions = new System.Drawing.SizeF(6f, 13f);
			base.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new System.Drawing.Size(594, 326);
			base.Controls.Add(dataGridViewEncryptedFiles);
			base.Name = "FormEncryptedFiles";
			Text = "EncryptedFiles";
			base.Load += new System.EventHandler(FormEncryptedFiles_Load);
			((System.ComponentModel.ISupportInitialize)dataGridViewEncryptedFiles).EndInit();
			ResumeLayout(false);
		}
	}
}
