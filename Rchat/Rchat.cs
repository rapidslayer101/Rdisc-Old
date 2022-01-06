using System;
using System.Diagnostics;
using System.Drawing;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Forms;

namespace Rchat
{
	public partial class Rchat : Form
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
			FormBorderStyle = FormBorderStyle.None;
			Region = Region.FromHrgn(Rchat.CreateRoundRectRgn(0, 0, Width, Height, 20, 20));
			Background.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Background.Width, Background.Height, 20, 20));
			Mninp_Bk.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Mninp_Bk.Width, Mninp_Bk.Height, 20, 20));
			Send.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, Send.Width, Send.Height, 20, 20));
		}

		private void Form1_Load(object sender, EventArgs e)
		{
			try
			{
				if (System.IO.File.Exists("rdisc.py"))
				{
					readData = "\n -> Starting internal socket (8078)";
					msg();
					clientSocket.Connect("127.0.0.1", 8078);
					new Thread(new ThreadStart(getMessage)).Start();
				}
                else
                {
					readData = "\n -> Starting internal socket (8079)";
					msg();
					clientSocket.Connect("127.0.0.1", 8079);
					new Thread(new ThreadStart(getMessage)).Start();
				}
			}
			catch (Exception d)
			{
				try
				{
					Process.Start("rdisc.exe");
					Application.Exit();
				}
				catch
				{
					MainOutput.SelectionColor = Color.Red;
					MainOutput.AppendText("\n[!] RDISC could not initialize, you might have launched ui.exe instead of rdisc.exe, please relaunch rdisc.exe\n\n" + d);
				}
			}
			MI_MaxChars.Visible = false;
			Send.Visible = false;
			Mninp_Bk.Visible = false;
			MainInput.Visible = false;
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


			if (readData.StartsWith("🱫[QUIT]"))
            {
				Application.Exit();
			}


			if (readData.StartsWith("Loaded version is"))
			{
				string version_text2 = Regex.Split(readData, "Loaded version is")[1];
				string format = "RDISC{0}";
				object[] args = Regex.Split(version_text2, "NE");
				version_text2 = string.Format(format, args);
				version_text2 = version_text2.Replace("[", "");
				if (label1.InvokeRequired)
				{
					label1.Invoke(new MethodInvoker(delegate()
					{
						version_text2 = label1.Text;
					}));
				}
				label1.Text = version_text2;
			}

			if (readData.StartsWith("Verified version is"))
			{
				string version_text2 = Regex.Split(readData, "Verified version is")[1];
				string format = "RDISC{0}";
				object[] args = Regex.Split(version_text2, "NE");
				version_text2 = string.Format(format, args);
				version_text2 = version_text2.Replace("[", "");
				if (label1.InvokeRequired)
				{
					label1.Invoke(new MethodInvoker(delegate ()
					{
						version_text2 = label1.Text;
					}));
				}
				label1.Text = version_text2;
			}

			if (readData.StartsWith("﻿🱫[TMKYT]"))
			{
				readData = readData.Replace("🱫[TMKYT]", "");
				tmkyt.Text = readData;
			}

			//if (readData.StartsWith("-font"));
			//	readData = readData[6:];
			//	MainOutput.Font = new Font("Arial", MainOutput.Font.Size, MainOutput.Font.Style);

			//if (IsHttpURL(readData))
			//{
			//	MainOutput.SelectionColor = Color.Cyan;
			//	MainOutput.AppendText(Environment.NewLine + readData);
			//}


			if (readData.StartsWith("﻿🱫[INPUT SHOW]"))
			{
				MI_MaxChars.Visible = true;
				Send.Visible = true;
				Mninp_Bk.Visible = true;
				MainInput.Visible = true;
				MainInput.Select();
				readData = readData.Replace("🱫[INPUT SHOW]", "");
			}

			if (readData.StartsWith("﻿🱫[INPUT HIDE]"))
            {
				MI_MaxChars.Visible = false;
				Send.Visible = false;
				Mninp_Bk.Visible = false;
				MainInput.Visible = false;
				readData = readData.Replace("🱫[INPUT HIDE]", "");
			}

			if (readData.StartsWith("🱫﻿[MNINPTXT]"))
			{
				readData = readData.Replace("🱫[MNINPTXT] ", "");
				MainInput.Text = readData;
				MainInput.Focus();
				MainInput.SelectionStart = MainInput.Text.Length;
			}

			if (readData.StartsWith("\n🱫﻿[COLOR THREAD]"))
			{
				readData = readData.Replace("🱫[COLOR THREAD]", "");
				if (readData.StartsWith("\n﻿[GREEN]"))
                {
					MainOutput.SelectionColor = Color.LightGreen;
					readData = readData.Replace("[GREEN]", "");
				}
				if (readData.StartsWith("\n﻿[YELLOW]"))
                {
					MainOutput.SelectionColor = Color.Yellow;
					readData = readData.Replace("[YELLOW]", "");
				}
				if (readData.StartsWith("﻿\n[RED]"))
                {
					MainOutput.SelectionColor = Color.Red;
					readData = readData.Replace("[RED]", "");
				}
			}
			else
			{
				MainOutput.SelectionColor = Color.White;

			}
			if (readData.StartsWith("\n"))
				MainOutput.AppendText(readData);

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
		}

		private void MainOutput_TextChanged(object sender, EventArgs e)
		{
			MainOutput.SelectionStart = MainOutput.Text.Length;
			MainOutput.ScrollToCaret();
		}

		private void MainInput_KeyDown(object sender, KeyEventArgs e)
		{

			if (e.KeyCode == Keys.Enter && e.Shift)
			{
				MainInput.AppendText("");
			}
			else
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
			}
			if (e.KeyCode == Keys.Back && MainInput.Text.Length == 0)
			{
				e.Handled = true;
				e.SuppressKeyPress = true;
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
			try
			{
				byte[] bytes = Encoding.Unicode.GetBytes("-quit");
				serverStream.Write(bytes, 0, bytes.Length);
				serverStream.Flush();
			}
			catch {}
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
			MI_MaxChars.Text = (MainInput.MaxLength - MainInput.Text.Length).ToString();
		}

		private void quitToolStripMenuItem_Click_1(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("-quit");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
			Application.Exit();
		}

		private void restartToolStripMenuItem_Click_1(object sender, EventArgs e)
		{
			byte[] bytes = Encoding.Unicode.GetBytes("-restart");
			serverStream.Write(bytes, 0, bytes.Length);
			serverStream.Flush();
			InitializeComponent();
			Application.Exit();
		}

		private void clearToolStripMenuItem_Click(object sender, EventArgs e)
		{
			MainOutput.Text = "";
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

        private void timer1_Tick_1(object sender, EventArgs e)
        {
			clock.Text = DateTime.Now.ToString("HH:mm:ss");
		}

        private void changeNameToolStripMenuItem_Click(object sender, EventArgs e)
        {
			MainInput.Text = "-change name ";
			MainInput.Select(MainInput.Text.Length, 0);
		}

        private void changePasswordToolStripMenuItem_Click(object sender, EventArgs e)
        {
			MainInput.Text = "-change password ";
			MainInput.SelectionStart = MainInput.Text.Length;
		}
    }
}
