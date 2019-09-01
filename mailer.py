#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author:		Trisna
# Creation date:	20-2-2019
# Language:		python
# Program name:		Mailer

import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def banner():
	print("\n███╗   ███╗ █████╗ ██╗██╗     ███████╗██████╗ ")
	print("████╗ ████║██╔══██╗██║██║     ██╔════╝██╔══██╗")
	print("██╔████╔██║███████║██║██║     █████╗  ██████╔╝")
	print("██║╚██╔╝██║██╔══██║██║██║     ██╔══╝  ██╔══██╗")
	print("██║ ╚═╝ ██║██║  ██║██║███████╗███████╗██║  ██║")
	print("╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝")
	print("\nAuthor: ramb0\n")

def main():
	# Servername of our mailserver
	server_name = raw_input("Server: ")

	try:
		server = smtplib.SMTP(server_name, 587)
		server.starttls()
		server.ehlo_or_helo_if_needed()
	except smtp.SMTPConnectError:
		print("\033[31mWe can't connect to the smtp mail server!\033[0m")
		return
	except smtp.SMTPServerDisconnected:
		print("\033[31mThe mail server disconnected unexpectedly!\033[0m")
		return
	except smtp.SMTPHeloError:
		print("\033[31mThe server denied our HELO message!\033[0m")
		return
	else:
		print("\033[32mSuccesfully connected with the mail server!\n\033[0m");

	# Username and password for login
	username = raw_input("EmailAddr: ")
	password = getpass.getpass("Password: ")

	try:
		server.login(username, password)
	except smtp.SMTPAuthenticationError:
		print("\033[31mThe server didn't accept your login and password!\033[0m\n")
		return
	except smtp.SMTPServerDisconnected:
                print("\033[31mThe mail server disconnected unexpectedly!\033[0m")
		return
	else:
		print("\033[32mSuccesfully logged in!\033[0m\n")

	# The receiver of our mail
	remote = raw_input("Mail-To: ")

	# Creating our email
	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = remote
	msg['Subject'] = raw_input("Subject: ")

	# Message input loop
	print("To end the message press enter 3 times!")
	body = ""
	new_lines = 0
	while 1:
		try:
			line = raw_input("=")
		except EOFError:
			break
		if not line:
			new_lines = new_lines + 1
			if new_lines == 3:
				break
			body = body + "\n"
		else:
			body = body + line + "\n"
			new_lines = 0

	print("Message length: " + str(len(body)))

	msg.attach(MIMEText(body, 'plain'))
	dataToSend = msg.as_string()

	try:
		server.sendmail(username, remote, dataToSend)
	except smtp.SMTPRecipientsRefused:
		print("\033[31mAll recepients refused! Nobody got the mail!\033[0m\n")
		return
	except smtp.SMTPDataError:
		print("\033[31mThe server replied with an unknown error!\033[0m\n")
		return
	except smtp.SMTPHeloError:
		print("\033[31mThe server didn't reply properly to the HELO greeting!\033[0m\n")
		return
	else:
		print("\033[32mMail succesfully sent!\033[0m\n")

if __name__ == "__main__":
	banner()
	main()

# More info about smtplib libary? visit:
# https://docs.python.org/2/library/smtplib.html
