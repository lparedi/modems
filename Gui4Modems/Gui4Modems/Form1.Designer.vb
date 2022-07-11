<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.SerialPort1 = New System.IO.Ports.SerialPort(Me.components)
        Me.ComboBox1 = New System.Windows.Forms.ComboBox()
        Me.ComboBox2 = New System.Windows.Forms.ComboBox()
        Me.Button1 = New System.Windows.Forms.Button()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.Label3 = New System.Windows.Forms.Label()
        Me.GroupBox1 = New System.Windows.Forms.GroupBox()
        Me.Button16 = New System.Windows.Forms.Button()
        Me.ComboBox6 = New System.Windows.Forms.ComboBox()
        Me.Config = New System.Windows.Forms.GroupBox()
        Me.Button19 = New System.Windows.Forms.Button()
        Me.Button18 = New System.Windows.Forms.Button()
        Me.Button17 = New System.Windows.Forms.Button()
        Me.TextBox9 = New System.Windows.Forms.TextBox()
        Me.Label16 = New System.Windows.Forms.Label()
        Me.CheckBox1 = New System.Windows.Forms.CheckBox()
        Me.Label15 = New System.Windows.Forms.Label()
        Me.Button15 = New System.Windows.Forms.Button()
        Me.TextBox8 = New System.Windows.Forms.TextBox()
        Me.Button14 = New System.Windows.Forms.Button()
        Me.TextBox7 = New System.Windows.Forms.TextBox()
        Me.Label14 = New System.Windows.Forms.Label()
        Me.Button12 = New System.Windows.Forms.Button()
        Me.Label13 = New System.Windows.Forms.Label()
        Me.Button10 = New System.Windows.Forms.Button()
        Me.Label12 = New System.Windows.Forms.Label()
        Me.TextBox5 = New System.Windows.Forms.TextBox()
        Me.Button9 = New System.Windows.Forms.Button()
        Me.TextBox4 = New System.Windows.Forms.TextBox()
        Me.Label11 = New System.Windows.Forms.Label()
        Me.Button8 = New System.Windows.Forms.Button()
        Me.Button7 = New System.Windows.Forms.Button()
        Me.TextBox3 = New System.Windows.Forms.TextBox()
        Me.Label10 = New System.Windows.Forms.Label()
        Me.TextBox2 = New System.Windows.Forms.TextBox()
        Me.Label9 = New System.Windows.Forms.Label()
        Me.Button6 = New System.Windows.Forms.Button()
        Me.Label8 = New System.Windows.Forms.Label()
        Me.Label7 = New System.Windows.Forms.Label()
        Me.Button5 = New System.Windows.Forms.Button()
        Me.ComboBox5 = New System.Windows.Forms.ComboBox()
        Me.Button4 = New System.Windows.Forms.Button()
        Me.Label6 = New System.Windows.Forms.Label()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.Label4 = New System.Windows.Forms.Label()
        Me.Button3 = New System.Windows.Forms.Button()
        Me.Button2 = New System.Windows.Forms.Button()
        Me.ComboBox3 = New System.Windows.Forms.ComboBox()
        Me.ComboBox4 = New System.Windows.Forms.ComboBox()
        Me.Button11 = New System.Windows.Forms.Button()
        Me.TextBox6 = New System.Windows.Forms.TextBox()
        Me.Button13 = New System.Windows.Forms.Button()
        Me.GroupBox1.SuspendLayout()
        Me.Config.SuspendLayout()
        Me.SuspendLayout()
        '
        'SerialPort1
        '
        Me.SerialPort1.BaudRate = 115200
        Me.SerialPort1.Parity = System.IO.Ports.Parity.Even
        Me.SerialPort1.PortName = "COM18"
        Me.SerialPort1.ReadTimeout = 5000
        Me.SerialPort1.WriteTimeout = 5000
        '
        'ComboBox1
        '
        Me.ComboBox1.FormattingEnabled = True
        Me.ComboBox1.Items.AddRange(New Object() {"2400", "9600", "19200", "57600", "115200"})
        Me.ComboBox1.Location = New System.Drawing.Point(24, 45)
        Me.ComboBox1.Name = "ComboBox1"
        Me.ComboBox1.Size = New System.Drawing.Size(70, 21)
        Me.ComboBox1.TabIndex = 1
        '
        'ComboBox2
        '
        Me.ComboBox2.FormattingEnabled = True
        Me.ComboBox2.Items.AddRange(New Object() {"Odd", "Even", "None"})
        Me.ComboBox2.Location = New System.Drawing.Point(24, 72)
        Me.ComboBox2.Name = "ComboBox2"
        Me.ComboBox2.Size = New System.Drawing.Size(70, 21)
        Me.ComboBox2.TabIndex = 2
        '
        'Button1
        '
        Me.Button1.Location = New System.Drawing.Point(24, 99)
        Me.Button1.Name = "Button1"
        Me.Button1.Size = New System.Drawing.Size(70, 23)
        Me.Button1.TabIndex = 3
        Me.Button1.Text = "Set"
        Me.Button1.UseVisualStyleBackColor = True
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(100, 26)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(31, 13)
        Me.Label1.TabIndex = 4
        Me.Label1.Text = "COM"
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(100, 53)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(32, 13)
        Me.Label2.TabIndex = 5
        Me.Label2.Text = "Baud"
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(100, 80)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(33, 13)
        Me.Label3.TabIndex = 6
        Me.Label3.Text = "Parity"
        '
        'GroupBox1
        '
        Me.GroupBox1.Controls.Add(Me.Button16)
        Me.GroupBox1.Controls.Add(Me.ComboBox6)
        Me.GroupBox1.Controls.Add(Me.Label3)
        Me.GroupBox1.Controls.Add(Me.ComboBox1)
        Me.GroupBox1.Controls.Add(Me.Label2)
        Me.GroupBox1.Controls.Add(Me.ComboBox2)
        Me.GroupBox1.Controls.Add(Me.Label1)
        Me.GroupBox1.Controls.Add(Me.Button1)
        Me.GroupBox1.Location = New System.Drawing.Point(12, 12)
        Me.GroupBox1.Name = "GroupBox1"
        Me.GroupBox1.Size = New System.Drawing.Size(175, 129)
        Me.GroupBox1.TabIndex = 7
        Me.GroupBox1.TabStop = False
        Me.GroupBox1.Text = "Serial"
        '
        'Button16
        '
        Me.Button16.Location = New System.Drawing.Point(134, 21)
        Me.Button16.Name = "Button16"
        Me.Button16.Size = New System.Drawing.Size(35, 23)
        Me.Button16.TabIndex = 39
        Me.Button16.Text = "F"
        Me.Button16.UseVisualStyleBackColor = True
        '
        'ComboBox6
        '
        Me.ComboBox6.FormattingEnabled = True
        Me.ComboBox6.Location = New System.Drawing.Point(23, 19)
        Me.ComboBox6.Name = "ComboBox6"
        Me.ComboBox6.Size = New System.Drawing.Size(70, 21)
        Me.ComboBox6.TabIndex = 7
        '
        'Config
        '
        Me.Config.Controls.Add(Me.Button19)
        Me.Config.Controls.Add(Me.Button18)
        Me.Config.Controls.Add(Me.Button17)
        Me.Config.Controls.Add(Me.TextBox9)
        Me.Config.Controls.Add(Me.Label16)
        Me.Config.Controls.Add(Me.CheckBox1)
        Me.Config.Controls.Add(Me.Label15)
        Me.Config.Controls.Add(Me.Button15)
        Me.Config.Controls.Add(Me.TextBox8)
        Me.Config.Controls.Add(Me.Button14)
        Me.Config.Controls.Add(Me.TextBox7)
        Me.Config.Controls.Add(Me.Label14)
        Me.Config.Controls.Add(Me.Button12)
        Me.Config.Controls.Add(Me.Label13)
        Me.Config.Controls.Add(Me.Button10)
        Me.Config.Controls.Add(Me.Label12)
        Me.Config.Controls.Add(Me.TextBox5)
        Me.Config.Controls.Add(Me.Button9)
        Me.Config.Controls.Add(Me.TextBox4)
        Me.Config.Controls.Add(Me.Label11)
        Me.Config.Controls.Add(Me.Button8)
        Me.Config.Controls.Add(Me.Button7)
        Me.Config.Controls.Add(Me.TextBox3)
        Me.Config.Controls.Add(Me.Label10)
        Me.Config.Controls.Add(Me.TextBox2)
        Me.Config.Controls.Add(Me.Label9)
        Me.Config.Controls.Add(Me.Button6)
        Me.Config.Controls.Add(Me.Label8)
        Me.Config.Controls.Add(Me.Label7)
        Me.Config.Controls.Add(Me.Button5)
        Me.Config.Controls.Add(Me.ComboBox5)
        Me.Config.Controls.Add(Me.Button4)
        Me.Config.Controls.Add(Me.Label6)
        Me.Config.Controls.Add(Me.Label5)
        Me.Config.Controls.Add(Me.Label4)
        Me.Config.Controls.Add(Me.Button3)
        Me.Config.Controls.Add(Me.Button2)
        Me.Config.Controls.Add(Me.ComboBox3)
        Me.Config.Controls.Add(Me.ComboBox4)
        Me.Config.Location = New System.Drawing.Point(201, 12)
        Me.Config.Name = "Config"
        Me.Config.Size = New System.Drawing.Size(815, 384)
        Me.Config.TabIndex = 8
        Me.Config.TabStop = False
        Me.Config.Text = "Config"
        '
        'Button19
        '
        Me.Button19.Location = New System.Drawing.Point(638, 271)
        Me.Button19.Name = "Button19"
        Me.Button19.Size = New System.Drawing.Size(160, 23)
        Me.Button19.TabIndex = 40
        Me.Button19.Text = "Write Current Config"
        Me.Button19.UseVisualStyleBackColor = True
        '
        'Button18
        '
        Me.Button18.Location = New System.Drawing.Point(460, 292)
        Me.Button18.Name = "Button18"
        Me.Button18.Size = New System.Drawing.Size(160, 23)
        Me.Button18.TabIndex = 39
        Me.Button18.Text = "Load Configuration"
        Me.Button18.UseVisualStyleBackColor = True
        '
        'Button17
        '
        Me.Button17.Location = New System.Drawing.Point(460, 250)
        Me.Button17.Name = "Button17"
        Me.Button17.Size = New System.Drawing.Size(160, 23)
        Me.Button17.TabIndex = 33
        Me.Button17.Text = "Save Configuration"
        Me.Button17.UseVisualStyleBackColor = True
        '
        'TextBox9
        '
        Me.TextBox9.Location = New System.Drawing.Point(521, 80)
        Me.TextBox9.Name = "TextBox9"
        Me.TextBox9.Size = New System.Drawing.Size(112, 20)
        Me.TextBox9.TabIndex = 38
        '
        'Label16
        '
        Me.Label16.AutoSize = True
        Me.Label16.Location = New System.Drawing.Point(645, 158)
        Me.Label16.Name = "Label16"
        Me.Label16.Size = New System.Drawing.Size(25, 13)
        Me.Label16.TabIndex = 37
        Me.Label16.Text = "Ans"
        '
        'CheckBox1
        '
        Me.CheckBox1.AutoSize = True
        Me.CheckBox1.Location = New System.Drawing.Point(648, 183)
        Me.CheckBox1.Name = "CheckBox1"
        Me.CheckBox1.Size = New System.Drawing.Size(15, 14)
        Me.CheckBox1.TabIndex = 36
        Me.CheckBox1.UseVisualStyleBackColor = True
        '
        'Label15
        '
        Me.Label15.AutoSize = True
        Me.Label15.Location = New System.Drawing.Point(508, 162)
        Me.Label15.Name = "Label15"
        Me.Label15.Size = New System.Drawing.Size(42, 13)
        Me.Label15.TabIndex = 35
        Me.Label15.Text = "Custom"
        '
        'Button15
        '
        Me.Button15.Location = New System.Drawing.Point(669, 178)
        Me.Button15.Name = "Button15"
        Me.Button15.Size = New System.Drawing.Size(47, 23)
        Me.Button15.TabIndex = 34
        Me.Button15.Text = "Send"
        Me.Button15.UseVisualStyleBackColor = True
        '
        'TextBox8
        '
        Me.TextBox8.Location = New System.Drawing.Point(460, 178)
        Me.TextBox8.Name = "TextBox8"
        Me.TextBox8.Size = New System.Drawing.Size(182, 20)
        Me.TextBox8.TabIndex = 33
        '
        'Button14
        '
        Me.Button14.Location = New System.Drawing.Point(328, 343)
        Me.Button14.Name = "Button14"
        Me.Button14.Size = New System.Drawing.Size(57, 23)
        Me.Button14.TabIndex = 32
        Me.Button14.Text = "Red"
        Me.Button14.UseVisualStyleBackColor = True
        '
        'TextBox7
        '
        Me.TextBox7.Location = New System.Drawing.Point(282, 32)
        Me.TextBox7.Name = "TextBox7"
        Me.TextBox7.Size = New System.Drawing.Size(36, 20)
        Me.TextBox7.TabIndex = 30
        '
        'Label14
        '
        Me.Label14.AutoSize = True
        Me.Label14.Location = New System.Drawing.Point(279, 16)
        Me.Label14.Name = "Label14"
        Me.Label14.Size = New System.Drawing.Size(39, 13)
        Me.Label14.TabIndex = 31
        Me.Label14.Text = "Meters"
        '
        'Button12
        '
        Me.Button12.Location = New System.Drawing.Point(464, 115)
        Me.Button12.Name = "Button12"
        Me.Button12.Size = New System.Drawing.Size(51, 23)
        Me.Button12.TabIndex = 29
        Me.Button12.Text = "Set"
        Me.Button12.UseVisualStyleBackColor = True
        '
        'Label13
        '
        Me.Label13.AutoSize = True
        Me.Label13.Location = New System.Drawing.Point(466, 99)
        Me.Label13.Name = "Label13"
        Me.Label13.Size = New System.Drawing.Size(35, 13)
        Me.Label13.TabIndex = 28
        Me.Label13.Text = "Reset"
        '
        'Button10
        '
        Me.Button10.Location = New System.Drawing.Point(225, 343)
        Me.Button10.Name = "Button10"
        Me.Button10.Size = New System.Drawing.Size(57, 23)
        Me.Button10.TabIndex = 27
        Me.Button10.Text = "Set"
        Me.Button10.UseVisualStyleBackColor = True
        '
        'Label12
        '
        Me.Label12.AutoSize = True
        Me.Label12.Location = New System.Drawing.Point(279, 56)
        Me.Label12.Name = "Label12"
        Me.Label12.Size = New System.Drawing.Size(58, 13)
        Me.Label12.TabIndex = 26
        Me.Label12.Text = "Meters List"
        '
        'TextBox5
        '
        Me.TextBox5.Location = New System.Drawing.Point(225, 77)
        Me.TextBox5.Multiline = True
        Me.TextBox5.Name = "TextBox5"
        Me.TextBox5.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        Me.TextBox5.Size = New System.Drawing.Size(160, 252)
        Me.TextBox5.TabIndex = 7
        '
        'Button9
        '
        Me.Button9.Location = New System.Drawing.Point(100, 238)
        Me.Button9.Name = "Button9"
        Me.Button9.Size = New System.Drawing.Size(35, 23)
        Me.Button9.TabIndex = 25
        Me.Button9.Text = "Set"
        Me.Button9.UseVisualStyleBackColor = True
        '
        'TextBox4
        '
        Me.TextBox4.Location = New System.Drawing.Point(6, 238)
        Me.TextBox4.Name = "TextBox4"
        Me.TextBox4.Size = New System.Drawing.Size(70, 20)
        Me.TextBox4.TabIndex = 23
        '
        'Label11
        '
        Me.Label11.AutoSize = True
        Me.Label11.Location = New System.Drawing.Point(25, 222)
        Me.Label11.Name = "Label11"
        Me.Label11.Size = New System.Drawing.Size(31, 13)
        Me.Label11.TabIndex = 24
        Me.Label11.Text = "LPW"
        '
        'Button8
        '
        Me.Button8.Location = New System.Drawing.Point(100, 199)
        Me.Button8.Name = "Button8"
        Me.Button8.Size = New System.Drawing.Size(35, 23)
        Me.Button8.TabIndex = 22
        Me.Button8.Text = "Set"
        Me.Button8.UseVisualStyleBackColor = True
        '
        'Button7
        '
        Me.Button7.Location = New System.Drawing.Point(100, 158)
        Me.Button7.Name = "Button7"
        Me.Button7.Size = New System.Drawing.Size(35, 23)
        Me.Button7.TabIndex = 21
        Me.Button7.Text = "Set"
        Me.Button7.UseVisualStyleBackColor = True
        '
        'TextBox3
        '
        Me.TextBox3.Location = New System.Drawing.Point(6, 199)
        Me.TextBox3.Name = "TextBox3"
        Me.TextBox3.Size = New System.Drawing.Size(88, 20)
        Me.TextBox3.TabIndex = 19
        '
        'Label10
        '
        Me.Label10.AutoSize = True
        Me.Label10.Location = New System.Drawing.Point(25, 183)
        Me.Label10.Name = "Label10"
        Me.Label10.Size = New System.Drawing.Size(44, 13)
        Me.Label10.TabIndex = 20
        Me.Label10.Text = "Sched4"
        '
        'TextBox2
        '
        Me.TextBox2.Location = New System.Drawing.Point(6, 161)
        Me.TextBox2.Name = "TextBox2"
        Me.TextBox2.Size = New System.Drawing.Size(86, 20)
        Me.TextBox2.TabIndex = 17
        '
        'Label9
        '
        Me.Label9.AutoSize = True
        Me.Label9.Location = New System.Drawing.Point(27, 144)
        Me.Label9.Name = "Label9"
        Me.Label9.Size = New System.Drawing.Size(44, 13)
        Me.Label9.TabIndex = 18
        Me.Label9.Text = "Sched2"
        '
        'Button6
        '
        Me.Button6.Location = New System.Drawing.Point(464, 77)
        Me.Button6.Name = "Button6"
        Me.Button6.Size = New System.Drawing.Size(51, 23)
        Me.Button6.TabIndex = 16
        Me.Button6.Text = "Set"
        Me.Button6.UseVisualStyleBackColor = True
        '
        'Label8
        '
        Me.Label8.AutoSize = True
        Me.Label8.Location = New System.Drawing.Point(466, 61)
        Me.Label8.Name = "Label8"
        Me.Label8.Size = New System.Drawing.Size(31, 13)
        Me.Label8.TabIndex = 15
        Me.Label8.Text = "Rstm"
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.Location = New System.Drawing.Point(31, 99)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(29, 13)
        Me.Label7.TabIndex = 12
        Me.Label7.Text = "Npol"
        '
        'Button5
        '
        Me.Button5.Location = New System.Drawing.Point(100, 115)
        Me.Button5.Name = "Button5"
        Me.Button5.Size = New System.Drawing.Size(35, 23)
        Me.Button5.TabIndex = 14
        Me.Button5.Text = "Set"
        Me.Button5.UseVisualStyleBackColor = True
        '
        'ComboBox5
        '
        Me.ComboBox5.FormattingEnabled = True
        Me.ComboBox5.Items.AddRange(New Object() {"0", "1"})
        Me.ComboBox5.Location = New System.Drawing.Point(6, 117)
        Me.ComboBox5.Name = "ComboBox5"
        Me.ComboBox5.Size = New System.Drawing.Size(66, 21)
        Me.ComboBox5.TabIndex = 13
        '
        'Button4
        '
        Me.Button4.Location = New System.Drawing.Point(464, 35)
        Me.Button4.Name = "Button4"
        Me.Button4.Size = New System.Drawing.Size(51, 23)
        Me.Button4.TabIndex = 11
        Me.Button4.Text = "Set"
        Me.Button4.UseVisualStyleBackColor = True
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(464, 19)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(53, 13)
        Me.Label6.TabIndex = 10
        Me.Label6.Text = "Erase List"
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(27, 56)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(33, 13)
        Me.Label5.TabIndex = 7
        Me.Label5.Text = "Parity"
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(28, 16)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(32, 13)
        Me.Label4.TabIndex = 7
        Me.Label4.Text = "Baud"
        '
        'Button3
        '
        Me.Button3.Location = New System.Drawing.Point(100, 75)
        Me.Button3.Name = "Button3"
        Me.Button3.Size = New System.Drawing.Size(35, 23)
        Me.Button3.TabIndex = 9
        Me.Button3.Text = "Set"
        Me.Button3.UseVisualStyleBackColor = True
        '
        'Button2
        '
        Me.Button2.Location = New System.Drawing.Point(100, 31)
        Me.Button2.Name = "Button2"
        Me.Button2.Size = New System.Drawing.Size(35, 23)
        Me.Button2.TabIndex = 7
        Me.Button2.Text = "Set"
        Me.Button2.UseVisualStyleBackColor = True
        '
        'ComboBox3
        '
        Me.ComboBox3.FormattingEnabled = True
        Me.ComboBox3.Items.AddRange(New Object() {"2400", "9600", "19200", "57600", "115200"})
        Me.ComboBox3.Location = New System.Drawing.Point(6, 33)
        Me.ComboBox3.Name = "ComboBox3"
        Me.ComboBox3.Size = New System.Drawing.Size(70, 21)
        Me.ComboBox3.TabIndex = 7
        '
        'ComboBox4
        '
        Me.ComboBox4.FormattingEnabled = True
        Me.ComboBox4.Items.AddRange(New Object() {"Odd", "Even", "None"})
        Me.ComboBox4.Location = New System.Drawing.Point(6, 72)
        Me.ComboBox4.Name = "ComboBox4"
        Me.ComboBox4.Size = New System.Drawing.Size(70, 21)
        Me.ComboBox4.TabIndex = 8
        '
        'Button11
        '
        Me.Button11.Location = New System.Drawing.Point(12, 167)
        Me.Button11.Name = "Button11"
        Me.Button11.Size = New System.Drawing.Size(160, 23)
        Me.Button11.TabIndex = 28
        Me.Button11.Text = "Read Config"
        Me.Button11.UseVisualStyleBackColor = True
        '
        'TextBox6
        '
        Me.TextBox6.Location = New System.Drawing.Point(201, 417)
        Me.TextBox6.Multiline = True
        Me.TextBox6.Name = "TextBox6"
        Me.TextBox6.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
        Me.TextBox6.Size = New System.Drawing.Size(815, 189)
        Me.TextBox6.TabIndex = 30
        '
        'Button13
        '
        Me.Button13.Location = New System.Drawing.Point(35, 433)
        Me.Button13.Name = "Button13"
        Me.Button13.Size = New System.Drawing.Size(160, 23)
        Me.Button13.TabIndex = 32
        Me.Button13.Text = "Clear Log"
        Me.Button13.UseVisualStyleBackColor = True
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(1052, 618)
        Me.Controls.Add(Me.Button13)
        Me.Controls.Add(Me.TextBox6)
        Me.Controls.Add(Me.Button11)
        Me.Controls.Add(Me.Config)
        Me.Controls.Add(Me.GroupBox1)
        Me.Name = "Form1"
        Me.Text = "POC Config"
        Me.GroupBox1.ResumeLayout(False)
        Me.GroupBox1.PerformLayout()
        Me.Config.ResumeLayout(False)
        Me.Config.PerformLayout()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents SerialPort1 As IO.Ports.SerialPort
    Friend WithEvents ComboBox1 As ComboBox
    Friend WithEvents ComboBox2 As ComboBox
    Friend WithEvents Button1 As Button
    Friend WithEvents Label1 As Label
    Friend WithEvents Label2 As Label
    Friend WithEvents Label3 As Label
    Friend WithEvents GroupBox1 As GroupBox
    Friend WithEvents Config As GroupBox
    Friend WithEvents ComboBox3 As ComboBox
    Friend WithEvents ComboBox4 As ComboBox
    Friend WithEvents TextBox3 As TextBox
    Friend WithEvents Label10 As Label
    Friend WithEvents TextBox2 As TextBox
    Friend WithEvents Label9 As Label
    Friend WithEvents Button6 As Button
    Friend WithEvents Label8 As Label
    Friend WithEvents Label7 As Label
    Friend WithEvents Button5 As Button
    Friend WithEvents ComboBox5 As ComboBox
    Friend WithEvents Button4 As Button
    Friend WithEvents Label6 As Label
    Friend WithEvents Label5 As Label
    Friend WithEvents Label4 As Label
    Friend WithEvents Button3 As Button
    Friend WithEvents Button2 As Button
    Friend WithEvents Button8 As Button
    Friend WithEvents Button7 As Button
    Friend WithEvents TextBox5 As TextBox
    Friend WithEvents Button9 As Button
    Friend WithEvents TextBox4 As TextBox
    Friend WithEvents Label11 As Label
    Friend WithEvents Button10 As Button
    Friend WithEvents Label12 As Label
    Friend WithEvents Button11 As Button
    Friend WithEvents Button12 As Button
    Friend WithEvents Label13 As Label
    Friend WithEvents TextBox6 As TextBox
    Friend WithEvents TextBox7 As TextBox
    Friend WithEvents Label14 As Label
    Friend WithEvents Button13 As Button
    Friend WithEvents Button14 As Button
    Friend WithEvents Label16 As Label
    Friend WithEvents CheckBox1 As CheckBox
    Friend WithEvents Label15 As Label
    Friend WithEvents Button15 As Button
    Friend WithEvents TextBox8 As TextBox
    Friend WithEvents TextBox9 As TextBox
    Friend WithEvents Button16 As Button
    Friend WithEvents ComboBox6 As ComboBox
    Friend WithEvents Button17 As Button
    Friend WithEvents Button19 As Button
    Friend WithEvents Button18 As Button
End Class
