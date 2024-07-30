# Bulk Email Sender and Configuration of rsyslog with Postfix Maillog

This project contains a Python script for sending emails using SMTP. It supports sending emails to multiple recipients concurrently using threading. It also includes configuration of rsyslog with Postfix logging 

## Prerequisites

- Python 3.x
- `smtplib` module (included with Python)
- `json` module (included with Python)
- `email` module (included with Python)
- `recipients.txt` file containing the list of recipient email addresses
- `config.json` file containing SMTP configuration

## Configuration

1. **`config.json`**: 
   This file should contain the SMTP server configuration. Example:
   ```json
   {
     "smtp_server": "smtp.example.com",
     "smtp_port": 587,
     "smtp_username": "your_username",
     "smtp_password": "your_password",
     "from_email": "your_email@example.com",
     "subject": "Your Subject Here",
     "body": "Email body content here."
   }
   ```
   
2. Create a `recipients.txt` file in the project root with the list of email addresses (one per line):
	
	```plaintext
	recipient1@example.com
	recipient2@example.com
	recipient3@example.com
	```

## Usage

1. Ensure `config.json` and `recipients.txt` are properly configured.
     
2. Run the Python script

	```bash
	python send_email.py
	```
	
## rsyslog and Postfix Mail Log Configuration

### Configuration Steps

1. rsyslog Configuration

Create a file `/etc/rsyslog.d/50-mysql.conf` with the following content:

```plaintext
    action(type="ommysql" server="127.0.0.1" serverport="3306"
    db="Syslog" uid="your_db_username" pwd="your_db_password")
```
	
2. Database Schema

Create a MySQL database and table to store the logs:

```plaintext
CREATE DATABASE Syslog;
USE Syslog;
CREATE TABLE SystemEvents
(
	ID int unsigned not null auto_increment primary key,
	CustomerID bigint,
	ReceivedAt datetime NULL,
	DeviceReportedTime datetime NULL,
	Facility smallint NULL,
	Priority smallint NULL,
	FromHost varchar(60) NULL,
	Message text,
	NTSeverity int NULL,
	Importance int NULL,
	EventSource varchar(60),
	EventUser varchar(60) NULL,
	EventCategory int NULL,
	EventID int NULL,
	EventBinaryData text NULL,
	MaxAvailable int NULL,
	CurrUsage int NULL,
	MinUsage int NULL,
	MaxUsage int NULL,
	InfoUnitID int NULL,
	SysLogTag varchar(60),
	EventLogType varchar(60),
	GenericFileName VarChar(60),
	SystemID int NULL
);
	
```
	
3. Restart rsyslog

After configuring `rsyslog`, restart it to apply changes:

```bash
sudo systemctl restart rsyslog
```