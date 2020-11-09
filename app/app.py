import csv
from os import write
from flask import Flask, render_template, request, send_file
import pandas
import time
import requests as r
import json
from datetime import datetime
start = time.time()
app = Flask(__name__)
now = str(datetime.now())
file_name = "app/uploads/Tracking_Result"+now+".csv"
filename_1 = "uploads/Tracking_Result"+now+".csv"
#print(filename_1)
@app.route("/")
def index():
    return render_template("index.html")


track = []
jdata = []
rdict = { 'dateWithNoSuffix': '', 'deliveryStatus': '', 'origin': ''}


@app.route('/success-table', methods=['POST'])
def success_table():
    if request.method == "POST":
        file = request.files['file']

        try:
            df = pandas.read_csv(file, sep=",")
            for i in df:
                j=i
                str(i)
                track.append(i)

            for i in range(len(track)):

                i = track[i]
                url = "http://track.dtdc.com/ctbs-tracking/customerInterface.tr?submitName=getLoadMovementDetails&cnNo=" + \
                    str(i)
                try:
                    data = r.get(url)
                finally:
                    jdata = data.json()
                    jdata.reverse()
                    for jin in jdata:
                        for i in jin:
                            if i in rdict:
                                #k = int(float(i))
                                #rdict[0] = j
                                rdict[i] = jin[i]

                try:
                    with open(file_name, 'a') as csvfile:
                        #header = str(i)
                        csv_col = ['dateWithNoSuffix', 'deliveryStatus', 'origin']

                        writer = csv.DictWriter(csvfile, csv_col)
                        writer.writerow(rdict)
                except IOError:
                    print("I/O error")

            return render_template("index.html", btn='download.html')

        except Exception as e:
            return render_template("index.html", text=str(e))


@app.route("/download-file/")
def download():

    
    #print (filename_1)
    return send_file(filename_1, attachment_filename="Tracking_Result"+now+".csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
