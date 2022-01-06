using System;
using System.Windows.Forms;

namespace Rchat
{
	// Token: 0x02000003 RID: 3
	internal static class Program
	{
		// Token: 0x06000020 RID: 32 RVA: 0x00003708 File Offset: 0x00001908
		[STAThread]
		private static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new Rchat());
		}
	}
}
