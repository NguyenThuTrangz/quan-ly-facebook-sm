# Liet ke cua so trinh duyet; neu co -Mo thi khoi phuc (khong chiem focus) cac cua so bi thu nho co tieu de chua chuoi do
param([string]$Mo = "")
Add-Type @"
using System;using System.Runtime.InteropServices;using System.Text;using System.Collections.Generic;
public class CuaSo{[DllImport("user32.dll")]public static extern bool ShowWindow(IntPtr h,int c);[DllImport("user32.dll")]public static extern bool IsIconic(IntPtr h);
public delegate bool EP(IntPtr h,IntPtr l);[DllImport("user32.dll")]public static extern bool EnumWindows(EP f,IntPtr l);
[DllImport("user32.dll")]public static extern int GetWindowText(IntPtr h,StringBuilder s,int n);[DllImport("user32.dll")]public static extern bool IsWindowVisible(IntPtr h);
public static List<string> Chay(string mo){var r=new List<string>();EnumWindows((h,l)=>{var sb=new StringBuilder(256);GetWindowText(h,sb,256);var t=sb.ToString();
if(IsWindowVisible(h)&&(t.Contains("Chrome")||t.Contains("Edge"))){bool m=IsIconic(h);if(mo!=""&&m&&t.Contains(mo)){ShowWindow(h,4);t="[DA MO] "+t;}r.Add(t+" | min="+m);}return true;},IntPtr.Zero);return r;}}
"@
[CuaSo]::Chay($Mo)
