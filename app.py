from flask import Flask, request, render_template
from collections import OrderedDict
from db_queries import *

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        surname = request.form['surname']
        firstname = request.form['firstname']
        studentnumber = request.form['studentnumber']
        rname = verify_input(surname, firstname, studentnumber)

        if not rname:
            return render_template('index.html', msg='Invalid input')

        scores_raw = scan_scores(rname)
        scores = OrderedDict()
        for score in scores_raw:
            exnums = [k for k in score.keys() if k[0].isdigit()]
            exnums.sort()
            l = [(k, score[k]) for k in exnums]
            l.append(('Group with', ', '.join(score['group'])))
            scores[score['sheetNumber']] = l
        return render_template('index.html', scores=scores)

    return render_template('index.html')


