import pandas as pd
import datetime

attendance_df = pd.read_csv('attendance.txt', sep='\t')


def get_employee_list(attendance_df):
	return attendance_df['Name GMNo'].unique()

def get_logs_by_month(mm, yy, attendance_df):
	attendance_df['DateTime'] = attendance_df['DateTime'].astype('datetime64[ns]')
	return attendance_df[(attendance_df['DateTime']>datetime.date(yy,mm,1)) & (attendance_df['DateTime']<datetime.date(yy,mm+1,1))]

def get_in_out(attendance_df):
	# report = {}
	attendance_df['DateTime'] = attendance_df['DateTime'].astype('datetime64[ns]')
	
	emps = get_employee_list(attendance_df)
	for emp in emps[2:]:
		pass

def gen_emp_report(attendance_df, emp_approx):
	emps = get_employee_list(attendance_df)
	emp = ''
	for e in emps:
		if emp_approx.lower() in e.lower():
			emp = e
	report = {
			"date": [],
			"day":[],
			"status": [],
			"in": [],
			"out": [],
			"work hours": [],
			"late time": []
		}
	dates = attendance_df['DateTime'].dt.strftime('%Y-%m-%d').unique()
	for date in dates:
		in_out = attendance_df[(attendance_df['DateTime'].dt.strftime('%Y-%m-%d')==date) & (attendance_df['Name GMNo']==emp)]
		if len(in_out) == 2:
			timedelta_obj = in_out.iloc[1]['DateTime']-in_out.iloc[0]['DateTime']
			
			status = 'Present'
			late_time = datetime.datetime.strptime(in_out.iloc[0]['DateTime'].strftime('%H:%M'),'%H:%M') - datetime.datetime.strptime('9:30','%H:%M') 
			if datetime.datetime.strptime(in_out.iloc[0]['DateTime'].strftime('%H:%M'),'%H:%M') > datetime.datetime.strptime('9:40','%H:%M'):
				status = 'Late'
			if late_time.days < 0 and late_time.total_seconds() < 600:
				late_time = 0
			report["date"].append(date),
			report["day"].append(in_out.iloc[0]['DateTime'].strftime('%A')),
			report["status"].append(status),
			report["in"].append(in_out.iloc[0]['DateTime'].strftime('%H:%M')),
			report["out"].append(in_out.iloc[1]['DateTime'].strftime('%H:%M')),
			report["work hours"].append(timedelta_obj),
			report['late time'].append(late_time)
			
		elif len(in_out) == 1:
			report["date"].append(date),
			report["day"].append(in_out.iloc[0]['DateTime'].strftime('%A')),
			report["status"].append("Invalid"),
			report["in"].append(in_out.iloc[0]['DateTime'].strftime('%H:%M')),
			report["out"].append('N/A'),
			report["work hours"].append(0),
			report['late time'].append('N/A')
		else:
			report["date"].append(date),
			report["day"].append(datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')),
			report["status"].append("Absent"),
			report["in"].append('N/A'),
			report["out"].append('N/A'),
			report["work hours"].append(0),
			report['late time'].append('N/A')
	return pd.DataFrame(report)
			

def get_emp_report_by_month(year, month, emp):
	logs = get_logs_by_month(month,year,attendance_df)
	return gen_emp_report(logs, emp)

def report_stats(report):
	return report['status'].value_counts()

# report = get_emp_report_by_month(2020, 2, "Girish")
# report_stats(report)

from flask import Flask, abort, request, render_template, redirect

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		name = request.form['name']
		month = int(request.form['month'])
		year = int(request.form['year'])
		report = get_emp_report_by_month(year, month, name)
		print(report)
		return report.to_html() + '<br>' + str(report_stats(report))
	return render_template('index.html')

if __name__ == '__main__':
    app.run()
