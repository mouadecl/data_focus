"""
Application: app.py
Description: Project assignment for Software Engineer ( Data focus )
Version: 1.0
Date: 16/03/2021
Author: Mouad ATTAQI
Modification Date: N/A
Modified by: N/A
"""

import io
from flask import Flask
import requests
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
	# initialise a dictionary in which the final result will be stored
	dicts = {}

	# the URLs of both external services
	url_service_a = 'https://run.mocky.io/v3/9a01a1b9-26e1-4c8a-84db-d534352e1461'
	url_service_b = 'https://run.mocky.io/v3/ba026992-281a-42a6-8447-ae1c8a04106e'

	# getting the result from both services
	response_a = requests.get(url_service_a)
	response_b = requests.get(url_service_b)

	# checking that both endpoints are working properly
	if response_a.ok and response_b.ok:
		# retrieving content of the results
		content_a = response_a.json()
		content_b = response_b.content

		# converting the contents to pandas dataframe
		df_a = pd.DataFrame.from_records(content_a)
		df_b = pd.read_csv(io.StringIO(content_b.decode('utf-8')), sep=",", header=0)

		# checking that the impression field does exit and contains numerical values for aggregations
		if ('impressions' in df_a.columns and 'impression' in df_b.columns) and (is_numeric_dtype(df_a['impressions']) and is_numeric_dtype(df_b['impression'])):
			# calculating sums of all impressions from both services separately
			total_a = df_a['impressions'].sum()
			total_b = df_b['impression'].sum()

			# calculating average of all impressions from both services separately
			average_a = df_a['impressions'].mean()
			average_b = df_b['impression'].mean()

			# aggregating results from both services
			dicts['sum'] = int(total_a) + int(total_b)
			dicts['mean'] = round((float(average_a) + float(average_b)) / 2, 2)

			return dicts
		else:
			return "One of all external services  doesn't contain the field impression(s) or the field doesn't contain numerical values"
	else:
		return "One of all external services  is not working"


if __name__ == "__main__":
	app.run(port=8000, debug=True)
