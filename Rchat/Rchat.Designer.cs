namespace Rchat
{
	public partial class Rchat : global::System.Windows.Forms.Form
	{
		protected override void Dispose(bool disposing)
		{
			if (disposing && this.components != null)
			{
				this.components.Dispose();
			}
			base.Dispose(disposing);
		}

		private void InitializeComponent()
		{
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Rchat));
            this.Send = new System.Windows.Forms.Button();
            this.MainInput = new System.Windows.Forms.RichTextBox();
            this.VersionLabel = new System.Windows.Forms.Label();
            this.MI_MaxChars = new System.Windows.Forms.Label();
            this.Resize = new System.Windows.Forms.Button();
            this.Exit = new System.Windows.Forms.Button();
            this.Minimise = new System.Windows.Forms.Button();
            this.TopPanel = new System.Windows.Forms.Panel();
            this.Menu = new System.Windows.Forms.MenuStrip();
            this.optionsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.uIToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.reloadToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.restartToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.quitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.accountToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.changeNameToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.changePasswordToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.logoutToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.logoutThisDeviceToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.logoutAllDevicesToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.confirmLogoutOfAllDevicesToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.deleteAccountToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.confirmAccountDeletetionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.preferencesToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.fontToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.arialToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.lucidaSansUnicodeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.fontSizeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem5 = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem2 = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem3 = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem4 = new System.Windows.Forms.ToolStripMenuItem();
            this.fontCommandToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.MainInput_pic = new System.Windows.Forms.PictureBox();
            this.MainOutput_backing_pic = new System.Windows.Forms.PictureBox();
            this.Background = new System.Windows.Forms.Panel();
            this.LeftPanel = new System.Windows.Forms.Panel();
            this.DM_select = new System.Windows.Forms.ListBox();
            this.Friends_label = new System.Windows.Forms.Label();
            this.clock = new System.Windows.Forms.Label();
            this.runtime = new System.Windows.Forms.Label();
            this.Mninp_Bk = new System.Windows.Forms.Panel();
            this.MainOutput = new System.Windows.Forms.RichTextBox();
            this.Timer1 = new System.Windows.Forms.Timer(this.components);
            this.BottomPanel = new System.Windows.Forms.Panel();
            this.TopPanel.SuspendLayout();
            this.Menu.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.MainInput_pic)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.MainOutput_backing_pic)).BeginInit();
            this.Background.SuspendLayout();
            this.LeftPanel.SuspendLayout();
            this.SuspendLayout();
            // 
            // Send
            // 
            this.Send.FlatAppearance.BorderSize = 0;
            this.Send.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Send.Image = ((System.Drawing.Image)(resources.GetObject("Send.Image")));
            this.Send.Location = new System.Drawing.Point(1201, 564);
            this.Send.Name = "Send";
            this.Send.Size = new System.Drawing.Size(50, 50);
            this.Send.TabIndex = 5;
            this.Send.Text = ">";
            this.Send.UseVisualStyleBackColor = true;
            this.Send.Click += new System.EventHandler(this.Send_Click);
            // 
            // MainInput
            // 
            this.MainInput.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.MainInput.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(40)))), ((int)(((byte)(40)))), ((int)(((byte)(40)))));
            this.MainInput.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.MainInput.EnableAutoDragDrop = true;
            this.MainInput.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MainInput.ForeColor = System.Drawing.Color.White;
            this.MainInput.Location = new System.Drawing.Point(278, 601);
            this.MainInput.MaxLength = 4000;
            this.MainInput.Name = "MainInput";
            this.MainInput.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.Vertical;
            this.MainInput.Size = new System.Drawing.Size(849, 35);
            this.MainInput.TabIndex = 6;
            this.MainInput.Text = "";
            this.MainInput.LinkClicked += new System.Windows.Forms.LinkClickedEventHandler(this.MainInput_LinkClicked);
            this.MainInput.TextChanged += new System.EventHandler(this.MainInput_TextChanged);
            this.MainInput.KeyDown += new System.Windows.Forms.KeyEventHandler(this.MainInput_KeyDown);
            // 
            // VersionLabel
            // 
            this.VersionLabel.AutoSize = true;
            this.VersionLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.VersionLabel.ForeColor = System.Drawing.Color.White;
            this.VersionLabel.Location = new System.Drawing.Point(5, 2);
            this.VersionLabel.Name = "VersionLabel";
            this.VersionLabel.Size = new System.Drawing.Size(118, 20);
            this.VersionLabel.TabIndex = 7;
            this.VersionLabel.Tag = "";
            this.VersionLabel.Text = "RDISC V0.x.x";
            this.VersionLabel.MouseEnter += new System.EventHandler(this.VersionLabel_MouseEnter);
            this.VersionLabel.MouseLeave += new System.EventHandler(this.VersionLabel_MouseLeave);
            this.VersionLabel.MouseMove += new System.Windows.Forms.MouseEventHandler(this.label1_MouseMove);
            // 
            // MI_MaxChars
            // 
            this.MI_MaxChars.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.MI_MaxChars.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(40)))), ((int)(((byte)(40)))), ((int)(((byte)(40)))));
            this.MI_MaxChars.ForeColor = System.Drawing.Color.Coral;
            this.MI_MaxChars.Location = new System.Drawing.Point(1154, 615);
            this.MI_MaxChars.Name = "MI_MaxChars";
            this.MI_MaxChars.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.MI_MaxChars.Size = new System.Drawing.Size(42, 13);
            this.MI_MaxChars.TabIndex = 11;
            this.MI_MaxChars.Text = "4000";
            this.MI_MaxChars.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // Resize
            // 
            this.Resize.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(25)))), ((int)(((byte)(25)))), ((int)(((byte)(25)))));
            this.Resize.FlatAppearance.BorderSize = 0;
            this.Resize.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Resize.ForeColor = System.Drawing.Color.White;
            this.Resize.Image = ((System.Drawing.Image)(resources.GetObject("Resize.Image")));
            this.Resize.Location = new System.Drawing.Point(1204, 0);
            this.Resize.Name = "Resize";
            this.Resize.Size = new System.Drawing.Size(23, 23);
            this.Resize.TabIndex = 10;
            this.Resize.UseVisualStyleBackColor = false;
            this.Resize.Click += new System.EventHandler(this.Resize_Click);
            // 
            // Exit
            // 
            this.Exit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(25)))), ((int)(((byte)(25)))), ((int)(((byte)(25)))));
            this.Exit.FlatAppearance.BorderSize = 0;
            this.Exit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Exit.ForeColor = System.Drawing.Color.White;
            this.Exit.Image = ((System.Drawing.Image)(resources.GetObject("Exit.Image")));
            this.Exit.Location = new System.Drawing.Point(1231, 0);
            this.Exit.Name = "Exit";
            this.Exit.Size = new System.Drawing.Size(29, 23);
            this.Exit.TabIndex = 8;
            this.Exit.UseVisualStyleBackColor = false;
            this.Exit.Click += new System.EventHandler(this.Exit_Click);
            this.Exit.MouseEnter += new System.EventHandler(this.Exit_MouseEnter);
            this.Exit.MouseLeave += new System.EventHandler(this.Exit_MouseLeave);
            // 
            // Minimise
            // 
            this.Minimise.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(25)))), ((int)(((byte)(25)))), ((int)(((byte)(25)))));
            this.Minimise.FlatAppearance.BorderSize = 0;
            this.Minimise.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Minimise.ForeColor = System.Drawing.Color.White;
            this.Minimise.Image = ((System.Drawing.Image)(resources.GetObject("Minimise.Image")));
            this.Minimise.Location = new System.Drawing.Point(1177, 0);
            this.Minimise.Name = "Minimise";
            this.Minimise.Size = new System.Drawing.Size(23, 23);
            this.Minimise.TabIndex = 11;
            this.Minimise.UseVisualStyleBackColor = false;
            this.Minimise.Click += new System.EventHandler(this.Minimise_Click);
            // 
            // TopPanel
            // 
            this.TopPanel.Controls.Add(this.Minimise);
            this.TopPanel.Controls.Add(this.Exit);
            this.TopPanel.Controls.Add(this.Resize);
            this.TopPanel.Location = new System.Drawing.Point(2, 0);
            this.TopPanel.Name = "TopPanel";
            this.TopPanel.Size = new System.Drawing.Size(1262, 24);
            this.TopPanel.TabIndex = 9;
            this.TopPanel.MouseMove += new System.Windows.Forms.MouseEventHandler(this.panel1_MouseMove);
            // 
            // Menu
            // 
            this.Menu.AllowDrop = true;
            this.Menu.AutoSize = false;
            this.Menu.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.Menu.Dock = System.Windows.Forms.DockStyle.None;
            this.Menu.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.optionsToolStripMenuItem,
            this.accountToolStripMenuItem,
            this.preferencesToolStripMenuItem});
            this.Menu.LayoutStyle = System.Windows.Forms.ToolStripLayoutStyle.Flow;
            this.Menu.Location = new System.Drawing.Point(4, 650);
            this.Menu.Name = "Menu";
            this.Menu.RenderMode = System.Windows.Forms.ToolStripRenderMode.Professional;
            this.Menu.Size = new System.Drawing.Size(1258, 20);
            this.Menu.TabIndex = 12;
            // 
            // optionsToolStripMenuItem
            // 
            this.optionsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.uIToolStripMenuItem,
            this.reloadToolStripMenuItem,
            this.restartToolStripMenuItem,
            this.quitToolStripMenuItem});
            this.optionsToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.optionsToolStripMenuItem.Name = "optionsToolStripMenuItem";
            this.optionsToolStripMenuItem.Size = new System.Drawing.Size(41, 19);
            this.optionsToolStripMenuItem.Text = "App";
            // 
            // uIToolStripMenuItem
            // 
            this.uIToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(60)))), ((int)(((byte)(60)))), ((int)(((byte)(60)))));
            this.uIToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.uIToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.uIToolStripMenuItem.Name = "uIToolStripMenuItem";
            this.uIToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Alt | System.Windows.Forms.Keys.U)));
            this.uIToolStripMenuItem.Size = new System.Drawing.Size(195, 24);
            this.uIToolStripMenuItem.Text = "Disable UI";
            this.uIToolStripMenuItem.Click += new System.EventHandler(this.uIToolStripMenuItem_Click);
            // 
            // reloadToolStripMenuItem
            // 
            this.reloadToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(66)))), ((int)(((byte)(66)))), ((int)(((byte)(66)))));
            this.reloadToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.reloadToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.reloadToolStripMenuItem.Name = "reloadToolStripMenuItem";
            this.reloadToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.R)));
            this.reloadToolStripMenuItem.Size = new System.Drawing.Size(195, 24);
            this.reloadToolStripMenuItem.Text = "Reload";
            this.reloadToolStripMenuItem.Click += new System.EventHandler(this.reloadToolStripMenuItem_Click);
            // 
            // restartToolStripMenuItem
            // 
            this.restartToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(60)))), ((int)(((byte)(60)))), ((int)(((byte)(60)))));
            this.restartToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.restartToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.restartToolStripMenuItem.Name = "restartToolStripMenuItem";
            this.restartToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)(((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Alt) 
            | System.Windows.Forms.Keys.R)));
            this.restartToolStripMenuItem.Size = new System.Drawing.Size(195, 24);
            this.restartToolStripMenuItem.Text = "Restart";
            this.restartToolStripMenuItem.Click += new System.EventHandler(this.restartToolStripMenuItem_Click_1);
            // 
            // quitToolStripMenuItem
            // 
            this.quitToolStripMenuItem.BackColor = System.Drawing.Color.Red;
            this.quitToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.quitToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.quitToolStripMenuItem.Name = "quitToolStripMenuItem";
            this.quitToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Alt | System.Windows.Forms.Keys.F4)));
            this.quitToolStripMenuItem.Size = new System.Drawing.Size(195, 24);
            this.quitToolStripMenuItem.Text = "Quit";
            this.quitToolStripMenuItem.Click += new System.EventHandler(this.quitToolStripMenuItem_Click_1);
            // 
            // accountToolStripMenuItem
            // 
            this.accountToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.changeNameToolStripMenuItem1,
            this.changePasswordToolStripMenuItem,
            this.logoutToolStripMenuItem1,
            this.deleteAccountToolStripMenuItem});
            this.accountToolStripMenuItem.Name = "accountToolStripMenuItem";
            this.accountToolStripMenuItem.Size = new System.Drawing.Size(64, 19);
            this.accountToolStripMenuItem.Text = "Account";
            // 
            // changeNameToolStripMenuItem1
            // 
            this.changeNameToolStripMenuItem1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(66)))), ((int)(((byte)(66)))), ((int)(((byte)(66)))));
            this.changeNameToolStripMenuItem1.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.changeNameToolStripMenuItem1.ForeColor = System.Drawing.Color.Yellow;
            this.changeNameToolStripMenuItem1.Name = "changeNameToolStripMenuItem1";
            this.changeNameToolStripMenuItem1.Size = new System.Drawing.Size(185, 24);
            this.changeNameToolStripMenuItem1.Text = "Change name";
            this.changeNameToolStripMenuItem1.Click += new System.EventHandler(this.changeNameToolStripMenuItem1_Click);
            // 
            // changePasswordToolStripMenuItem
            // 
            this.changePasswordToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(60)))), ((int)(((byte)(60)))), ((int)(((byte)(60)))));
            this.changePasswordToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.changePasswordToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.changePasswordToolStripMenuItem.Name = "changePasswordToolStripMenuItem";
            this.changePasswordToolStripMenuItem.Size = new System.Drawing.Size(185, 24);
            this.changePasswordToolStripMenuItem.Text = "Change password";
            this.changePasswordToolStripMenuItem.Click += new System.EventHandler(this.changePasswordToolStripMenuItem_Click);
            // 
            // logoutToolStripMenuItem1
            // 
            this.logoutToolStripMenuItem1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(66)))), ((int)(((byte)(66)))), ((int)(((byte)(66)))));
            this.logoutToolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.logoutThisDeviceToolStripMenuItem,
            this.logoutAllDevicesToolStripMenuItem});
            this.logoutToolStripMenuItem1.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.logoutToolStripMenuItem1.ForeColor = System.Drawing.Color.Yellow;
            this.logoutToolStripMenuItem1.Name = "logoutToolStripMenuItem1";
            this.logoutToolStripMenuItem1.Size = new System.Drawing.Size(185, 24);
            this.logoutToolStripMenuItem1.Text = "Logout";
            // 
            // logoutThisDeviceToolStripMenuItem
            // 
            this.logoutThisDeviceToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(66)))), ((int)(((byte)(66)))), ((int)(((byte)(66)))));
            this.logoutThisDeviceToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.logoutThisDeviceToolStripMenuItem.Name = "logoutThisDeviceToolStripMenuItem";
            this.logoutThisDeviceToolStripMenuItem.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.L)));
            this.logoutThisDeviceToolStripMenuItem.Size = new System.Drawing.Size(238, 24);
            this.logoutThisDeviceToolStripMenuItem.Text = "Logout this device";
            this.logoutThisDeviceToolStripMenuItem.Click += new System.EventHandler(this.logoutThisDeviceToolStripMenuItem_Click);
            // 
            // logoutAllDevicesToolStripMenuItem
            // 
            this.logoutAllDevicesToolStripMenuItem.BackColor = System.Drawing.Color.Red;
            this.logoutAllDevicesToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.confirmLogoutOfAllDevicesToolStripMenuItem1});
            this.logoutAllDevicesToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.logoutAllDevicesToolStripMenuItem.Name = "logoutAllDevicesToolStripMenuItem";
            this.logoutAllDevicesToolStripMenuItem.Size = new System.Drawing.Size(238, 24);
            this.logoutAllDevicesToolStripMenuItem.Text = "Logout all devices";
            // 
            // confirmLogoutOfAllDevicesToolStripMenuItem1
            // 
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.BackColor = System.Drawing.Color.Red;
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.ForeColor = System.Drawing.Color.Yellow;
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.Name = "confirmLogoutOfAllDevicesToolStripMenuItem1";
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.Size = new System.Drawing.Size(252, 24);
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.Text = "Confirm logout of all devices";
            this.confirmLogoutOfAllDevicesToolStripMenuItem1.Click += new System.EventHandler(this.confirmLogoutOfAllDevicesToolStripMenuItem1_Click);
            // 
            // deleteAccountToolStripMenuItem
            // 
            this.deleteAccountToolStripMenuItem.BackColor = System.Drawing.Color.Red;
            this.deleteAccountToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.confirmAccountDeletetionToolStripMenuItem});
            this.deleteAccountToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.deleteAccountToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.deleteAccountToolStripMenuItem.Name = "deleteAccountToolStripMenuItem";
            this.deleteAccountToolStripMenuItem.Size = new System.Drawing.Size(185, 24);
            this.deleteAccountToolStripMenuItem.Text = "Delete account";
            // 
            // confirmAccountDeletetionToolStripMenuItem
            // 
            this.confirmAccountDeletetionToolStripMenuItem.BackColor = System.Drawing.Color.Red;
            this.confirmAccountDeletetionToolStripMenuItem.ForeColor = System.Drawing.Color.Yellow;
            this.confirmAccountDeletetionToolStripMenuItem.Name = "confirmAccountDeletetionToolStripMenuItem";
            this.confirmAccountDeletetionToolStripMenuItem.Size = new System.Drawing.Size(244, 24);
            this.confirmAccountDeletetionToolStripMenuItem.Text = "Confirm account deletetion";
            this.confirmAccountDeletetionToolStripMenuItem.Click += new System.EventHandler(this.confirmAccountDeletetionToolStripMenuItem_Click);
            // 
            // preferencesToolStripMenuItem
            // 
            this.preferencesToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fontToolStripMenuItem,
            this.fontSizeToolStripMenuItem,
            this.fontCommandToolStripMenuItem});
            this.preferencesToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.preferencesToolStripMenuItem.Name = "preferencesToolStripMenuItem";
            this.preferencesToolStripMenuItem.Size = new System.Drawing.Size(80, 19);
            this.preferencesToolStripMenuItem.Text = "Preferences";
            // 
            // fontToolStripMenuItem
            // 
            this.fontToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.fontToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.arialToolStripMenuItem,
            this.lucidaSansUnicodeToolStripMenuItem});
            this.fontToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.fontToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.fontToolStripMenuItem.Name = "fontToolStripMenuItem";
            this.fontToolStripMenuItem.Size = new System.Drawing.Size(169, 24);
            this.fontToolStripMenuItem.Text = "Font";
            // 
            // arialToolStripMenuItem
            // 
            this.arialToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.arialToolStripMenuItem.Name = "arialToolStripMenuItem";
            this.arialToolStripMenuItem.Size = new System.Drawing.Size(203, 24);
            this.arialToolStripMenuItem.Text = "Arial";
            this.arialToolStripMenuItem.Click += new System.EventHandler(this.arialToolStripMenuItem_Click);
            // 
            // lucidaSansUnicodeToolStripMenuItem
            // 
            this.lucidaSansUnicodeToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.lucidaSansUnicodeToolStripMenuItem.Name = "lucidaSansUnicodeToolStripMenuItem";
            this.lucidaSansUnicodeToolStripMenuItem.Size = new System.Drawing.Size(203, 24);
            this.lucidaSansUnicodeToolStripMenuItem.Text = "Lucida Sans Unicode";
            this.lucidaSansUnicodeToolStripMenuItem.Click += new System.EventHandler(this.lucidaSansUnicodeToolStripMenuItem_Click);
            // 
            // fontSizeToolStripMenuItem
            // 
            this.fontSizeToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.fontSizeToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripMenuItem5,
            this.toolStripMenuItem2,
            this.toolStripMenuItem3,
            this.toolStripMenuItem4});
            this.fontSizeToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.fontSizeToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.fontSizeToolStripMenuItem.Name = "fontSizeToolStripMenuItem";
            this.fontSizeToolStripMenuItem.Size = new System.Drawing.Size(169, 24);
            this.fontSizeToolStripMenuItem.Text = "Font size";
            // 
            // toolStripMenuItem5
            // 
            this.toolStripMenuItem5.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.toolStripMenuItem5.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(0)))), ((int)(((byte)(162)))));
            this.toolStripMenuItem5.Name = "toolStripMenuItem5";
            this.toolStripMenuItem5.Size = new System.Drawing.Size(94, 24);
            this.toolStripMenuItem5.Text = "13";
            this.toolStripMenuItem5.Click += new System.EventHandler(this.toolStripMenuItem5_Click);
            // 
            // toolStripMenuItem2
            // 
            this.toolStripMenuItem2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.toolStripMenuItem2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(0)))), ((int)(((byte)(162)))));
            this.toolStripMenuItem2.Name = "toolStripMenuItem2";
            this.toolStripMenuItem2.Size = new System.Drawing.Size(94, 24);
            this.toolStripMenuItem2.Text = "12";
            this.toolStripMenuItem2.Click += new System.EventHandler(this.toolStripMenuItem2_Click);
            // 
            // toolStripMenuItem3
            // 
            this.toolStripMenuItem3.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.toolStripMenuItem3.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(0)))), ((int)(((byte)(162)))));
            this.toolStripMenuItem3.Name = "toolStripMenuItem3";
            this.toolStripMenuItem3.Size = new System.Drawing.Size(94, 24);
            this.toolStripMenuItem3.Text = "11";
            this.toolStripMenuItem3.Click += new System.EventHandler(this.toolStripMenuItem3_Click);
            // 
            // toolStripMenuItem4
            // 
            this.toolStripMenuItem4.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.toolStripMenuItem4.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(0)))), ((int)(((byte)(162)))));
            this.toolStripMenuItem4.Name = "toolStripMenuItem4";
            this.toolStripMenuItem4.Size = new System.Drawing.Size(94, 24);
            this.toolStripMenuItem4.Text = "10";
            this.toolStripMenuItem4.Click += new System.EventHandler(this.toolStripMenuItem4_Click);
            // 
            // fontCommandToolStripMenuItem
            // 
            this.fontCommandToolStripMenuItem.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.fontCommandToolStripMenuItem.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.fontCommandToolStripMenuItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.fontCommandToolStripMenuItem.Name = "fontCommandToolStripMenuItem";
            this.fontCommandToolStripMenuItem.Size = new System.Drawing.Size(169, 24);
            this.fontCommandToolStripMenuItem.Text = "Font command";
            this.fontCommandToolStripMenuItem.Click += new System.EventHandler(this.fontCommandToolStripMenuItem_Click);
            // 
            // MainInput_pic
            // 
            this.MainInput_pic.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("MainInput_pic.BackgroundImage")));
            this.MainInput_pic.Location = new System.Drawing.Point(18, 588);
            this.MainInput_pic.Name = "MainInput_pic";
            this.MainInput_pic.Size = new System.Drawing.Size(0, 0);
            this.MainInput_pic.TabIndex = 15;
            this.MainInput_pic.TabStop = false;
            // 
            // MainOutput_backing_pic
            // 
            this.MainOutput_backing_pic.Image = ((System.Drawing.Image)(resources.GetObject("MainOutput_backing_pic.Image")));
            this.MainOutput_backing_pic.Location = new System.Drawing.Point(8, 29);
            this.MainOutput_backing_pic.Name = "MainOutput_backing_pic";
            this.MainOutput_backing_pic.Size = new System.Drawing.Size(0, 0);
            this.MainOutput_backing_pic.TabIndex = 16;
            this.MainOutput_backing_pic.TabStop = false;
            // 
            // Background
            // 
            this.Background.AllowDrop = true;
            this.Background.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.Background.Controls.Add(this.LeftPanel);
            this.Background.Controls.Add(this.clock);
            this.Background.Controls.Add(this.runtime);
            this.Background.Controls.Add(this.Mninp_Bk);
            this.Background.Controls.Add(this.Send);
            this.Background.Location = new System.Drawing.Point(4, 25);
            this.Background.Name = "Background";
            this.Background.Size = new System.Drawing.Size(1259, 643);
            this.Background.TabIndex = 17;
            // 
            // LeftPanel
            // 
            this.LeftPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(45)))), ((int)(((byte)(45)))), ((int)(((byte)(45)))));
            this.LeftPanel.Controls.Add(this.DM_select);
            this.LeftPanel.Controls.Add(this.Friends_label);
            this.LeftPanel.Location = new System.Drawing.Point(0, 0);
            this.LeftPanel.Name = "LeftPanel";
            this.LeftPanel.Size = new System.Drawing.Size(250, 635);
            this.LeftPanel.TabIndex = 8;
            // 
            // DM_select
            // 
            this.DM_select.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(45)))), ((int)(((byte)(45)))), ((int)(((byte)(45)))));
            this.DM_select.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.DM_select.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold);
            this.DM_select.ForeColor = System.Drawing.Color.White;
            this.DM_select.FormattingEnabled = true;
            this.DM_select.ItemHeight = 16;
            this.DM_select.Location = new System.Drawing.Point(18, 41);
            this.DM_select.Name = "DM_select";
            this.DM_select.Size = new System.Drawing.Size(213, 544);
            this.DM_select.TabIndex = 2;
            // 
            // Friends_label
            // 
            this.Friends_label.AutoSize = true;
            this.Friends_label.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold);
            this.Friends_label.ForeColor = System.Drawing.Color.White;
            this.Friends_label.Location = new System.Drawing.Point(76, 6);
            this.Friends_label.Name = "Friends_label";
            this.Friends_label.Size = new System.Drawing.Size(81, 17);
            this.Friends_label.TabIndex = 0;
            this.Friends_label.Text = "Online (0)";
            // 
            // clock
            // 
            this.clock.AutoSize = true;
            this.clock.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.clock.ForeColor = System.Drawing.Color.Red;
            this.clock.Location = new System.Drawing.Point(1168, 11);
            this.clock.Name = "clock";
            this.clock.Size = new System.Drawing.Size(67, 20);
            this.clock.TabIndex = 7;
            this.clock.Text = "CLOCK";
            // 
            // runtime
            // 
            this.runtime.AutoSize = true;
            this.runtime.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(128)));
            this.runtime.ForeColor = System.Drawing.Color.Red;
            this.runtime.Location = new System.Drawing.Point(1168, 41);
            this.runtime.Name = "runtime";
            this.runtime.Size = new System.Drawing.Size(64, 20);
            this.runtime.TabIndex = 6;
            this.runtime.Text = "RTIME";
            this.runtime.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Mninp_Bk
            // 
            this.Mninp_Bk.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(40)))), ((int)(((byte)(40)))), ((int)(((byte)(40)))));
            this.Mninp_Bk.Location = new System.Drawing.Point(264, 565);
            this.Mninp_Bk.Name = "Mninp_Bk";
            this.Mninp_Bk.Size = new System.Drawing.Size(932, 50);
            this.Mninp_Bk.TabIndex = 0;
            // 
            // MainOutput
            // 
            this.MainOutput.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(50)))), ((int)(((byte)(50)))), ((int)(((byte)(50)))));
            this.MainOutput.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.MainOutput.Cursor = System.Windows.Forms.Cursors.Default;
            this.MainOutput.Font = new System.Drawing.Font("Lucida Sans Unicode", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MainOutput.ForeColor = System.Drawing.Color.White;
            this.MainOutput.Location = new System.Drawing.Point(278, 36);
            this.MainOutput.Name = "MainOutput";
            this.MainOutput.ReadOnly = true;
            this.MainOutput.Size = new System.Drawing.Size(875, 524);
            this.MainOutput.TabIndex = 4;
            this.MainOutput.TabStop = false;
            this.MainOutput.Text = "";
            this.MainOutput.LinkClicked += new System.Windows.Forms.LinkClickedEventHandler(this.MainOutput_LinkClicked);
            this.MainOutput.TextChanged += new System.EventHandler(this.MainOutput_TextChanged);
            // 
            // Timer1
            // 
            this.Timer1.Enabled = true;
            this.Timer1.Interval = 1000;
            this.Timer1.Tick += new System.EventHandler(this.Clock_Tick);
            // 
            // BottomPanel
            // 
            this.BottomPanel.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(98)))), ((int)(((byte)(81)))), ((int)(((byte)(255)))));
            this.BottomPanel.Location = new System.Drawing.Point(4, 652);
            this.BottomPanel.Name = "BottomPanel";
            this.BottomPanel.Size = new System.Drawing.Size(1259, 26);
            this.BottomPanel.TabIndex = 0;
            // 
            // Rchat
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(25)))), ((int)(((byte)(25)))), ((int)(((byte)(25)))));
            this.ClientSize = new System.Drawing.Size(1264, 681);
            this.ControlBox = false;
            this.Controls.Add(this.MainOutput);
            this.Controls.Add(this.MI_MaxChars);
            this.Controls.Add(this.VersionLabel);
            this.Controls.Add(this.MainInput);
            this.Controls.Add(this.TopPanel);
            this.Controls.Add(this.Menu);
            this.Controls.Add(this.MainInput_pic);
            this.Controls.Add(this.MainOutput_backing_pic);
            this.Controls.Add(this.Background);
            this.Controls.Add(this.BottomPanel);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "Rchat";
            this.Text = "Rchat";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.TopPanel.ResumeLayout(false);
            this.Menu.ResumeLayout(false);
            this.Menu.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.MainInput_pic)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.MainOutput_backing_pic)).EndInit();
            this.Background.ResumeLayout(false);
            this.Background.PerformLayout();
            this.LeftPanel.ResumeLayout(false);
            this.LeftPanel.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

		}

		private global::System.ComponentModel.IContainer components;
		private global::System.Windows.Forms.Button Send;
		private global::System.Windows.Forms.RichTextBox MainInput;
		private global::System.Windows.Forms.Label VersionLabel;
		private global::System.Windows.Forms.Label MI_MaxChars;
		private new global::System.Windows.Forms.Button Resize;
		private global::System.Windows.Forms.Button Exit;
		private global::System.Windows.Forms.Button Minimise;
		private global::System.Windows.Forms.Panel TopPanel;
		private new global::System.Windows.Forms.MenuStrip Menu;
		private global::System.Windows.Forms.ToolStripMenuItem optionsToolStripMenuItem;
		private global::System.Windows.Forms.ToolStripMenuItem restartToolStripMenuItem;
		private global::System.Windows.Forms.ToolStripMenuItem quitToolStripMenuItem;
		private global::System.Windows.Forms.PictureBox MainInput_pic;
		private global::System.Windows.Forms.PictureBox MainOutput_backing_pic;
        private System.Windows.Forms.ToolStripMenuItem preferencesToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem fontToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem fontSizeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem2;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem3;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem4;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem5;
        private System.Windows.Forms.ToolStripMenuItem lucidaSansUnicodeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem arialToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem fontCommandToolStripMenuItem;
        private System.Windows.Forms.Panel Background;
        private System.Windows.Forms.Panel Mninp_Bk;
        private System.Windows.Forms.RichTextBox MainOutput;
        private System.Windows.Forms.Label runtime;
        private System.Windows.Forms.Label clock;
        private System.Windows.Forms.Timer Timer1;
        private System.Windows.Forms.ToolStripMenuItem reloadToolStripMenuItem;
        private System.Windows.Forms.Panel LeftPanel;
        private System.Windows.Forms.Panel BottomPanel;
        private System.Windows.Forms.ToolStripMenuItem accountToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem logoutToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem logoutThisDeviceToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem logoutAllDevicesToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem confirmLogoutOfAllDevicesToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem deleteAccountToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem confirmAccountDeletetionToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem changeNameToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem changePasswordToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem uIToolStripMenuItem;
        private System.Windows.Forms.Label Friends_label;
        private System.Windows.Forms.ListBox DM_select;
    }
}
