Public Class Form1
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Dim parity As Integer
        SerialPort1.PortName = ComboBox6.Text
        SerialPort1.BaudRate = CInt(ComboBox1.Text)
        Select Case ComboBox2.Text
            Case "None"
                parity = 0
            Case "Odd"
                parity = 1
            Case "Even"
                parity = 2

        End Select
        SerialPort1.Parity = parity
    End Sub

    Private Sub Button12_Click(sender As Object, e As EventArgs) Handles Button12.Click
        SerialPort1.Open()
        SerialPort1.Write("$$$AT+MCRS=1;")
        SerialPort1.Close()
    End Sub

    Private Sub Button11_Click(sender As Object, e As EventArgs) Handles Button11.Click
        Dim ans As String
        Dim baud() As String
        Dim parity() As String
        Dim npol() As String
        Dim sched2() As String
        Dim sched4() As String
        Dim lpw() As String
        Dim meters() As String
        Dim rstm As String

        Try
            SerialPort1.Open()
            TextBox6.AppendText("$$$AT+BAUD=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+BAUD=?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            baud = ans.Split(":")
            ComboBox3.Text = baud(1)


            TextBox6.AppendText("$$$AT+EVEN=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+EVEN=?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            parity = ans.Split(":")
            If parity(1) = 0 Then
                ComboBox4.Text = "None"
            Else
                ComboBox4.Text = "Event"
            End If

            TextBox6.AppendText("$$$AT+NPOL=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+NPOL=?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            npol = ans.Split(":")
            ComboBox5.Text = npol(1)

            TextBox6.AppendText("$$$AT+SCHED2=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+SCHD=2-?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            sched2 = ans.Split(":")
            TextBox2.Text = sched2(1)

            TextBox6.AppendText("$$$AT+SCHED4=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+SCHD=4-?;")

            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            sched4 = ans.Split(":")
            TextBox3.Text = sched4(1)

            TextBox6.AppendText("$$$AT+LPWR=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+LPWR=?;")
            ans = SerialPort1.ReadTo(";")

            TextBox6.AppendText(ans & ";" & vbCrLf)
            lpw = ans.Split(":")
            TextBox4.Text = lpw(1)

            TextBox6.AppendText("$$$AT+VLSN=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+VLSN=?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            meters = ans.Split(":")
            TextBox7.Text = meters(1)

            TextBox6.AppendText("$$$AT+RSTM=?;" & vbCrLf)
            SerialPort1.Write("$$$AT+RSTM=?;")
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
            TextBox9.Text = ans.Replace("TIME:", "")

            SerialPort1.Close()

        Catch ex As Exception
            TextBox6.AppendText(ex.ToString)
            SerialPort1.Close()



        End Try

        Call setallwhite()
    End Sub

    Private Sub Button10_Click(sender As Object, e As EventArgs) Handles Button10.Click
        Dim buff As String
        Dim meters() As String
        Dim meter As String
        Dim telegram As String
        Dim prefix As String
        Dim suffix As String
        Dim rows As Integer
        Dim byten As Integer
        Dim ntelegram As Integer
        Dim ans As String

        telegram = ""
        prefix = "$$$AT+WRSN="
        suffix = ";"
        byten = 0
        ntelegram = 0
        SerialPort1.Open()
        buff = TextBox5.Text
        meters = buff.Split(vbCrLf)

        For Each meter In meters
            byten = byten + 1
            If byten Mod 10 <> 0 And meter <> "" Then
                telegram = telegram & "-" & meter.Replace(vbLf, "")
            Else
                telegram = prefix & "10" & telegram & "-" & meter.Replace(vbLf, "") & suffix

                TextBox6.AppendText(telegram & vbCrLf)
                SerialPort1.Write(telegram)
                telegram = ""
                ans = SerialPort1.ReadTo(";")
                TextBox6.AppendText(ans & ";" & vbCrLf)
            End If

        Next
        If telegram <> "" Then
            telegram = prefix & CStr(byten Mod 10) & telegram & suffix

            TextBox6.AppendText(telegram & vbCrLf)
            SerialPort1.Write(telegram)
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans & ";" & vbCrLf)
        End If
        SerialPort1.Close()
        TextBox6.AppendText("Lista Caricata" & vbCrLf)
        TextBox5.BackColor = Color.Green
    End Sub

    Private Sub Button13_Click(sender As Object, e As EventArgs) Handles Button13.Click
        TextBox6.Text = ""
    End Sub

    Private Sub TextBox5_TextChanged(sender As Object, e As EventArgs) Handles TextBox5.TextChanged

        TextBox5.BackColor = Color.Red
    End Sub

    Private Sub ComboBox3_TextUpdate(sender As Object, e As EventArgs) Handles ComboBox3.TextUpdate
        ComboBox3.BackColor = Color.Red

    End Sub

    Private Sub ComboBox3_TextChanged(sender As Object, e As EventArgs) Handles ComboBox3.TextChanged
        ComboBox3.BackColor = Color.Red
    End Sub

    Private Sub setallwhite()
        ComboBox3.BackColor = Color.White
        ComboBox4.BackColor = Color.White
        ComboBox5.BackColor = Color.White
        TextBox2.BackColor = Color.White
        TextBox3.BackColor = Color.White
        TextBox4.BackColor = Color.White
    End Sub

    Private Sub ComboBox4_TextChanged(sender As Object, e As EventArgs) Handles ComboBox4.TextChanged
        ComboBox4.BackColor = Color.Red
    End Sub

    Private Sub ComboBox5_TextChanged(sender As Object, e As EventArgs) Handles ComboBox5.TextChanged
        ComboBox5.BackColor = Color.Red
    End Sub

    Private Sub TextBox2_TextChanged(sender As Object, e As EventArgs) Handles TextBox2.TextChanged
        TextBox2.BackColor = Color.Red
    End Sub

    Private Sub TextBox3_TextChanged(sender As Object, e As EventArgs) Handles TextBox3.TextChanged
        TextBox3.BackColor = Color.Red
    End Sub

    Private Sub TextBox4_TextChanged(sender As Object, e As EventArgs) Handles TextBox4.TextChanged
        TextBox4.BackColor = Color.Red
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        SerialPort1.Open()
        TextBox6.AppendText("$$$AT+ERSN=*;" & vbCrLf)
        SerialPort1.Write("$$$AT+ERSN=*;")
        SerialPort1.Close()
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        MsgBox("Cambiando il BAUD rate dovrai riconnetterti al modem")
        SerialPort1.Open()
        SerialPort1.Write("$$$AT+BAUD=" & ComboBox3.Text & ";")
        TextBox6.AppendText("$$$AT+BAUD=" & ComboBox3.Text & ";")
        SerialPort1.Close()
        ComboBox3.BackColor = Color.Green
    End Sub

    Private Sub ComboBox4_SelectedIndexChanged(sender As Object, e As EventArgs) Handles ComboBox4.SelectedIndexChanged

    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Dim parita As Integer

        MsgBox("Cambiando il la parita' dovrai riconnetterti al modem")
        If ComboBox4.Text = "Even" Then
            parita = 1
        Else
            parita = 0
        End If
        SerialPort1.Open()
        SerialPort1.Write("$$$AT+EVEN=" & CStr(parita) & ";")
        TextBox6.AppendText("$$$AT+EVEN=" & CStr(parita) & ";")
        SerialPort1.Close()
        ComboBox4.BackColor = Color.Green
    End Sub

    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
        MsgBox("Cambiando la polarita il momdem non sara' piu' accessibile via seriale", vbCritical)
        SerialPort1.Open()
        TextBox6.AppendText("$$$AT+NPOL=" & ComboBox5.Text & ";")
        If False Then
            SerialPort1.Write("$$$AT+NPOL=" & ComboBox5.Text & ";")
        End If

        SerialPort1.Close()
        ComboBox5.BackColor = Color.Green
    End Sub

    Private Sub Button7_Click(sender As Object, e As EventArgs) Handles Button7.Click
        If validatecron(TextBox2.Text) Then

            SerialPort1.Open()
            TextBox6.AppendText("$$$AT+SCHD=2-" & TextBox2.Text & ";")
            SerialPort1.Write("$$$AT+SCHD=2-" & TextBox2.Text & ";")
            SerialPort1.Close()
            TextBox2.BackColor = Color.Green
        Else
            MsgBox("formato non valido", vbCritical)
        End If

    End Sub
    Private Function validatecron(cron As String) As Boolean
        Dim buff() As String
        Dim element As String

        buff = cron.Split("-")
        If buff.Length <> 8 Then
            Return False
        End If
        For Each element In buff
            If element.IndexOfAny("/*1234567890".ToCharArray) = -1 Then
                Return False
            End If
        Next
        Return True
    End Function

    Private Sub Button8_Click(sender As Object, e As EventArgs) Handles Button8.Click
        If validatecron(TextBox3.Text) Then
            SerialPort1.Open()
            TextBox6.AppendText("$$$AT+SCHD=4-" & TextBox3.Text & ";")
            SerialPort1.Write("$$$AT+SCHD=4-" & TextBox3.Text & ";")
            SerialPort1.Close()
            TextBox3.BackColor = Color.Green
        Else
            MsgBox("formato non valido", vbCritical)
        End If
    End Sub

    Private Sub Button9_Click(sender As Object, e As EventArgs) Handles Button9.Click
        SerialPort1.Open()
        TextBox6.AppendText("$$$AT+LPWR=" & TextBox4.Text & ";")
        SerialPort1.Write("$$$AT+LPWR=" & TextBox4.Text & ";")
        SerialPort1.Close()
        TextBox4.BackColor = Color.Green
    End Sub

    Private Sub Button14_Click(sender As Object, e As EventArgs) Handles Button14.Click
        SerialPort1.Open()
        SerialPort1.Write("$$$AT+RDSN=?;")
        'While SerialPort1.BytesToRead <> 0
        MsgBox(SerialPort1.ReadTo(";"))
        'End While
        SerialPort1.Close()
    End Sub

    Private Sub Button15_Click(sender As Object, e As EventArgs) Handles Button15.Click
        Dim ans As String
        SerialPort1.Open()
        SerialPort1.Write(TextBox8.Text)
        TextBox6.AppendText(TextBox8.Text & vbCrLf)
        If CheckBox1.Checked Then
            ans = SerialPort1.ReadTo(";")
            TextBox6.AppendText(ans + ";" & vbCrLf)
        End If
        SerialPort1.Close()
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        SerialPort1.Open()
        TextBox6.AppendText("$$$AT+RSTM=" & Today.ToString("yyyy-MM-dd") & " " & Now.ToString("HH:mm:ss") & ";")
        SerialPort1.Write("$$$AT+RSTM=" & Today.ToString("yyyy-MM-dd") & " " & Now.ToString("HH:mm:ss") & ";")
        SerialPort1.Close()
    End Sub

    Private Sub Button16_Click(sender As Object, e As EventArgs) Handles Button16.Click

        ComboBox6.Items.Clear()

        For Each sp As String In My.Computer.Ports.SerialPortNames
            ComboBox6.Items.Add(sp)
        Next
    End Sub

    Private Sub Button17_Click(sender As Object, e As EventArgs) Handles Button17.Click
        Dim buff As String

        buff = "<config>" & vbCrLf
        buff = buff & "<baud>" & vbCrLf
        buff = buff & ComboBox3.Text & vbCrLf
        buff = buff & "<\baud>" & vbCrLf

        buff = buff & "<parity>" & vbCrLf
        buff = buff & ComboBox4.Text & vbCrLf
        buff = buff & "<\parity>" & vbCrLf

        buff = buff & "<npol>" & vbCrLf
        buff = buff & ComboBox5.Text & vbCrLf
        buff = buff & "<\npol>" & vbCrLf

        buff = buff & "<sched2>" & vbCrLf
        buff = buff & TextBox2.Text & vbCrLf
        buff = buff & "<\sched2>" & vbCrLf

        buff = buff & "<sched4>" & vbCrLf
        buff = buff & TextBox3.Text & vbCrLf
        buff = buff & "<\sched4>" & vbCrLf

        buff = buff & "<lpw>" & vbCrLf
        buff = buff & TextBox4.Text & vbCrLf
        buff = buff & "<\lpw>" & vbCrLf

        buff = buff & "<list>" & vbCrLf
        buff = buff & TextBox5.Text & vbCrLf
        buff = buff & "<\list>" & vbCrLf

        buff = buff & "<\config>" & vbCrLf


        Dim savedialog As New SaveFileDialog
        If savedialog.ShowDialog = DialogResult.OK Then
            Dim ofile As New IO.StreamWriter(savedialog.OpenFile)
            If (ofile IsNot Nothing) Then
                ofile.WriteLine(buff)
                ofile.Close()
            End If
        End If

        MsgBox("File salvato!")
    End Sub

    Private Sub Button19_Click(sender As Object, e As EventArgs) Handles Button19.Click

    End Sub

    Private Sub Button18_Click(sender As Object, e As EventArgs) Handles Button18.Click
        Dim content As String
        Dim ok As Boolean
        Dim loaddialog As New OpenFileDialog
        If loaddialog.ShowDialog = DialogResult.OK Then
            Dim ifile As New IO.StreamReader(loaddialog.OpenFile)
            If (ifile IsNot Nothing) Then
                content = ifile.ReadToEnd
                ok = parseconfig(content)
            End If
        End If
        If ok Then
            MsgBox("Configurazione caricata con successo!")
        End If
    End Sub
    Private Function parseconfig(content As String) As Boolean
        Dim buffer() As String
        Dim tmp As String
        Dim confdic As New Dictionary(Of String, String)
        Dim value As String
        Dim key As String
        Dim bird As Boolean
        value = ""

        buffer = content.Split(vbCrLf)
        For Each current As String In buffer

            If current.IndexOf("config") = -1 Then
                If current.IndexOfAny("\") = -1 Then

                    If current.IndexOfAny("<") <> -1 Then
                        tmp = current.Replace("<", "")
                        tmp = tmp.Replace(vbLf, "")
                        key = tmp.Replace(">", "")
                        value = ""

                    Else
                        value = value & current.Replace(vbLf, "") & vbCrLf

                    End If
                Else
                    confdic.Add(key, value)


                End If
            End If

        Next

        For Each kp As KeyValuePair(Of String, String) In confdic
            Select Case kp.Key
                Case "baud"
                    ComboBox3.Text = kp.Value
                Case "parity"
                    ComboBox4.Text = kp.Value
                Case "npol"
                    ComboBox5.Text = kp.Value
                Case "sched2"
                    TextBox2.Text = kp.Value
                Case "sched4"
                    TextBox3.Text = kp.Value
                Case "lpw"
                    TextBox4.Text = kp.Value
                Case "list"
                    TextBox5.Text = kp.Value
            End Select
        Next

        Return True

    End Function
End Class
