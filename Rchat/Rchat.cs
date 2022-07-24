using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Forms;

namespace Rchat
{
	public partial class Rchat
	{
		[DllImport("user32.dll")]
		public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);
		[DllImport("user32.dll")]
		public static extern bool ReleaseCapture();
		[DllImport("Gdi32.dll")]
		private static extern IntPtr CreateRoundRectRgn(int nLeftRect, int nTopRect, int nRightRect, int nBottomRect, int nWidthEllipse, int nHeightEllipse);

	public Rchat()
		{
			InitializeComponent();
			Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Width, Height, 20, 20));
			Background.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Background.Width, Background.Height, 20, 20));
			Mninp_Bk.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Mninp_Bk.Width, Mninp_Bk.Height, 20, 20));
			Send.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Send.Width, Send.Height, 20, 20));
			BottomPanel.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, BottomPanel.Width, BottomPanel.Height, 20, 20));
		}

		private void Form1_Load(object sender, EventArgs e)
		{
			try
			{
				readData = "\n -> Starting internal socket (30677)";
				msg();
				clientSocket.Connect("127.0.0.1", 30677);
				new Thread(new ThreadStart(getMessage)).Start();
			}
			catch (Exception d)
			{
				if (!(File.Exists("validation_keys.txt")))
					try
					{
						Process.Start("launch.bat");
						Application.Exit();
					}
					catch
					{
						MainOutput.SelectionColor = Color.Red;
						MainOutput.AppendText("\n[!] RDISC could not initialize, please close this window and start the launcher\n\n"+d);
					}
                else
                {
					MainOutput.SelectionColor = Color.Green;
					MainOutput.AppendText("\nNew UI version successfully compiled");
				}
			}
			MI_MaxChars.Visible = Send.Visible = Mninp_Bk.Visible = MainInput.Visible = false;
		}

		private void getMessage()
		{
			for (;;)
			{
				serverStream = clientSocket.GetStream();
				byte[] array = new byte[100025];
				int receiveBufferSize = clientSocket.ReceiveBufferSize;
				serverStream.Read(array, 0, receiveBufferSize);
				string @string = Encoding.Unicode.GetString(array);
				readData = (@string ?? "");
				msg();
			}
		}

		static public Font ChangeFontSize(Font font, float fontSize)
		{
			if (font != null)
			{
				float currentSize = font.Size;
				if (currentSize != fontSize)
				{
					font = new Font(font.Name, fontSize,
						font.Style, font.Unit,
						font.GdiCharSet, font.GdiVerticalFont);
				}
			}
			return font;
		}

		private void msg()
		{
			if (InvokeRequired)
			{
				Invoke(new MethodInvoker(msg));
				return;
			}

			//if (readData.StartsWith("🱫[SMELNE]"))
			//{
			//	MainOutput.ReadOnly = false;
			//	//MainOutput.Lines.Length
			//	MainOutput.Lines = MainOutput.Lines.CopyTo(MainOutput.Lines.Length - 3).ToArray;
			//	readData = readData.Replace("🱫[SMELNE]", "");
			//}

			if (readData.StartsWith("﻿🱫[EXIT]"))
			{
				Application.Exit();
			}


			if (readData.StartsWith("﻿🱫[LODVS]"))
			{
				string version_text2 = Regex.Split(readData, "🱫\\[LODVS]")[1];
				string format = "RDISC{0}";
				version_text2 = string.Format(format, version_text2);
				if (VersionLabel.InvokeRequired)
				{
					VersionLabel.Invoke(new MethodInvoker(delegate()
					{
						version_text2 = VersionLabel.Text;
					}));
				}
				VersionLabel.Text = version_text2;
			}

			if (readData.StartsWith("🱫[LODVS_E]"))
			{
				string version_text2 = Regex.Split(readData, "🱫\\[LODVS_E]")[1];
				string format = "RDISC{0}";
				version_text2 = string.Format(format, version_text2);
				if (VersionLabel.InvokeRequired)
				{
					VersionLabel.Invoke(new MethodInvoker(delegate()
					{
						version_text2 = VersionLabel.Text;
					}));
				}
				VersionLabel.Text = version_text2;
			}

			//if (readData.StartsWith("-font"));
			//	readData = readData[6:];
			//	MainOutput.Font = new Font("Arial", MainOutput.Font.Size, MainOutput.Font.Style);

			//if (IsHttpURL(readData))
			//{
			//	MainOutput.SelectionColor = Color.Cyan;
			//	MainOutput.AppendText(Environment.NewLine + readData);
			//}


			if (readData.StartsWith("﻿🱫[INP SHOW]"))
			{
				MI_MaxChars.Visible = Send.Visible = Mninp_Bk.Visible = MainInput.Visible = true;
				MainInput.Select();
				readData = readData.Replace("🱫[INPUT SHOW]", "");
			}

			if (readData.StartsWith("﻿🱫[INP HIDE]"))
            {
				MI_MaxChars.Visible = Send.Visible = Mninp_Bk.Visible = MainInput.Visible = false;
				readData = readData.Replace("🱫[INPUT HIDE]", "");
			}

			if (readData.StartsWith("🱫﻿[MNINPTXT]"))
			{
				readData = readData.Replace("🱫[MNINPTXT] ", "");
				MainInput.Text = readData;
				MainInput.Focus();
				MainInput.SelectionStart = MainInput.Text.Length;
			}

			if (readData.StartsWith("﻿🱫[CLRO]"))
			{
				MainOutput.Text = "";
			}

			if (readData.StartsWith("\n🱫﻿[COL-"))
			{
				readData = readData.Replace("🱫[COL-", "");
				if (readData.StartsWith("\n﻿GRN]"))
                {
					MainOutput.SelectionColor = Color.LightGreen;
					readData = readData.Replace("GRN]", "");
				}
				if (readData.StartsWith("\n﻿YEL]"))
                {
					MainOutput.SelectionColor = Color.Yellow;
					readData = readData.Replace("YEL]", "");
				}
				if (readData.StartsWith("﻿\nRED]"))
                {
					MainOutput.SelectionColor = Color.Red;
					readData = readData.Replace("RED]", "");
				}
			}
			else
			{
				MainOutput.SelectionColor = Color.White;

			}
			if (!(readData.StartsWith("🱫")))
				MainOutput.AppendText(readData);

			if (readData.StartsWith("﻿🱫[DC]"))
			{
				ConnectionStatus.ForeColor = Color.Red;
			}

			if (readData.StartsWith("﻿🱫[CONNECTED]"))
			{
				ConnectionStatus.ForeColor = Color.Yellow;
			}

			if (readData.StartsWith("﻿🱫[LOGGED_IN]"))
			{
				ConnectionStatus.ForeColor = Color.LightGreen;
			}


			if (readData.StartsWith("🱫﻿[MNINPLEN]"))
            {
				readData = readData.Replace("🱫[MNINPLEN]", "");
				if (readData.StartsWith("﻿[4000]"))
                {
					MainInput.MaxLength = 4000;
					MI_MaxChars.Text = "4000";
					readData = readData.Replace("[4000]", "");
				}
				if (readData.StartsWith("﻿[256]"))
				{
					MainInput.MaxLength = 256;
					MI_MaxChars.Text = "256";
					readData = readData.Replace("[256]", "");
				}
				if (readData.StartsWith("﻿[96]"))
				{
					MainInput.MaxLength = 96;
					MI_MaxChars.Text = "96";
					readData = readData.Replace("[96]", "");
				}
				if (readData.StartsWith("﻿[64]"))
				{
					MainInput.MaxLength = 64;
					MI_MaxChars.Text = "64";
					readData = readData.Replace("[64]", "");
				}
			}
			if (readData.StartsWith("UON:"))
            {
				string user_item = Regex.Split(readData, "﻿UON:")[1];
				DM_select.Items.Add(user_item);
			}
		}

		private void VersionLabel_MouseEnter(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("🱫[GET_VDATA_E]");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

		private void VersionLabel_MouseLeave(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("🱫[GET_VDATA]");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

		private void MainOutput_TextChanged(object sender, EventArgs e)
		{
			MainOutput.SelectionStart = MainOutput.Text.Length;
			MainOutput.ScrollToCaret();
		}

		private void MainInput_KeyDown(object sender, KeyEventArgs e)
		{
			if (MainInput.Visible == true)
            {
				if (e.KeyCode == Keys.Return)
				{
					e.Handled = true;
					e.SuppressKeyPress = true;
					byte[] bytes = Encoding.Unicode.GetBytes(MainInput.Text);
					MainInput.Text = "";
					serverStream.Write(bytes, 0, bytes.Length);
					serverStream.Flush();
				}
				if (e.KeyCode == Keys.Back && MainInput.Text.Length == 0)
				{
					e.Handled = true;
					e.SuppressKeyPress = true;
				}
			}


		}

		private void MainOutput_LinkClicked(object sender, LinkClickedEventArgs e)
		{
			if (IsHttpURL(e.LinkText))
			{
				Process.Start(e.LinkText);
			}
		}

		private void MainInput_LinkClicked(object sender, LinkClickedEventArgs e)
        {
			if (IsHttpURL(e.LinkText))
			{
				Process.Start(e.LinkText);
			}
		}

		private bool IsHttpURL(string url)
		{
			return !string.IsNullOrWhiteSpace(url) && url.ToLower().StartsWith("http");
		}

		private void Send_Click(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes(MainInput.Text);
			MainInput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

		private void panel1_MouseMove(object sender, MouseEventArgs e)
		{
			if (e.Button == MouseButtons.Left)
			{
				ReleaseCapture();
				Rchat.SendMessage(Handle, 161, 2, 0);
			}
		}

		private void label1_MouseMove(object sender, MouseEventArgs e)
		{
			if (e.Button == MouseButtons.Left)
			{
				ReleaseCapture();
				Rchat.SendMessage(Handle, 161, 2, 0);
			}
		}

		private void Exit_MouseEnter(object sender, EventArgs e)
		{
			Exit.BackColor = Color.Red;
		}

		private void Exit_MouseLeave(object sender, EventArgs e)
		{
			Exit.BackColor = Color.FromArgb(25, 25, 25);
		}

		private void Exit_Click(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("🱫[QUIT]");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
			Application.Exit();
		}

		private void Resize_Click(object sender, EventArgs e)
		{
			WindowState = FormWindowState.Maximized;
		}

		private void Minimise_Click(object sender, EventArgs e)
		{
			WindowState = FormWindowState.Minimized;
		}

		private void MainInput_TextChanged(object sender, EventArgs e)
		{
			MainInput.Text = MainInput.Text.Replace("\n", "");
			MainInput.SelectionStart = MainInput.Text.Length;
			MI_MaxChars.Text = (MainInput.MaxLength-MainInput.Text.Length).ToString();
		}

		private TcpClient clientSocket = new TcpClient();
		private NetworkStream serverStream;
		private string readData;
		public const int WM_NCLBUTTONDOWN = 161;
		public const int HT_CAPTION = 2;

		private void toolStripMenuItem5_Click(object sender, EventArgs e)
		{
			MainOutput.Font = ChangeFontSize(MainOutput.Font, 13);
		}

		private void toolStripMenuItem2_Click(object sender, EventArgs e)
        {
			MainOutput.Font = ChangeFontSize(MainOutput.Font, 12);
		}

        private void toolStripMenuItem3_Click(object sender, EventArgs e)
        {
			MainOutput.Font = ChangeFontSize(MainOutput.Font, 11);
		}

        private void toolStripMenuItem4_Click(object sender, EventArgs e)
        {
			MainOutput.Font = ChangeFontSize(MainOutput.Font, 10);
		}

        private void lucidaSansUnicodeToolStripMenuItem_Click(object sender, EventArgs e)
        {
			MainOutput.Font = new Font("Lucida Sans Unicode", MainOutput.Font.Size);
			MainInput.Font = new Font("Lucida Sans Unicode", MainInput.Font.Size);
		}

        private void arialToolStripMenuItem_Click(object sender, EventArgs e)
        {
			MainOutput.Font = new Font("Arial", MainOutput.Font.Size);
			MainInput.Font = new Font("Arial", MainInput.Font.Size);
		}

        private void fontCommandToolStripMenuItem_Click(object sender, EventArgs e)
        {
			MainInput.Text = "-font "+MainOutput.Font.Name+"-"+MainOutput.Font.Size;
		}

		private void reloadToolStripMenuItem_Click(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("-reload");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

		private void restartToolStripMenuItem_Click_1(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("ui reload");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
			Application.Exit();
		}

		private void quitToolStripMenuItem_Click_1(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("-exit");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
			Application.Exit();
		}

		int watch = 1;
		private void Clock_Tick(object sender, EventArgs e)
        {
			watch += 1;
			var timeSpan = TimeSpan.FromSeconds(watch);
			string hh = timeSpan.Hours.ToString();
			string mm = timeSpan.Minutes.ToString();
			string ss = timeSpan.Seconds.ToString();
			clock.Text = DateTime.Now.ToString("HH:mm:ss");
			runtime.Text = hh + "h" + mm + "m" + ss + "s";
		}

        private void logoutThisDeviceToolStripMenuItem_Click(object sender, EventArgs e)
        {
			byte[] bytes = Encoding.Unicode.GetBytes("🱫[LOG]");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

        private void confirmLogoutOfAllDevicesToolStripMenuItem1_Click(object sender, EventArgs e)
        {
			byte[] bytes = Encoding.Unicode.GetBytes("🱫[LOG_A]");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

        private void confirmAccountDeletetionToolStripMenuItem_Click(object sender, EventArgs e)
        {
			byte[] bytes = Encoding.Unicode.GetBytes("-delete account");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

        private void changeNameToolStripMenuItem1_Click(object sender, EventArgs e)
        {
			MainInput.Text = "-change name ";
			MainInput.Select(MainInput.Text.Length, 0);
		}

		private void addFriendToolStripMenuItem_Click(object sender, EventArgs e)
		{
			MainInput.Text = "-add friend ";
			MainInput.Select(MainInput.Text.Length, 0);
		}

		private void changePasswordToolStripMenuItem_Click(object sender, EventArgs e)
        {
			byte[] bytes = Encoding.Unicode.GetBytes("-change pass");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}

        private void uIToolStripMenuItem_Click(object sender, EventArgs e)
        {
			byte[] bytes = Encoding.Unicode.GetBytes("-ui");
			MainOutput.Text = "";
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
		}
    }
}
