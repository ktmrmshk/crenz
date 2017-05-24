from flask import Flask, render_template, Markup, request
import sys
import json
from crenz.dns_tester import DnsTester
import time

app=Flask(__name__)

def index():
  pagedata={'zone':'', 'authns':'', 'zonefile':''}
  pagedata['console']='get method'
  #pagedata['table']=[(True,2,3), (False,4,5)]
  pagedata['table']=[]
  pagedata['action'] = '/'
  return render_template('crenz.html', pd=pagedata)


#@app.route('/', methods=['POST'])
def recv_post():
  pagedata={}
  pagedata['authns']=request.form['authns']
  pagedata['zone']=request.form['zone']
  pagedata['zonefile']=request.form['zonefile']
  pagedata['action'] = '/'
  
  with open('dump.dat', 'w') as f:
    f.write(request.form['zonefile'])

  try:
    zonename=None
    if request.form['zone'] != '':
      zonename = request.form['zone']
    print(zonename)
    dt = DnsTester( request.form['authns'], zonename)
    dt.load_txt( pagedata['zonefile'].replace('\r\n', '\n') )
    pagedata['console']='done'
    ret = dt.zone_check()
  except Exception as err:
    pagedata['console']= 'err: {}\n{}'.format(err, sys.exc_info())
    
    ret = []

  pagedata['table']=ret
  #pagedata['table']=[(True,2,3), (False,4,5)]
  return render_template('crenz.html', pd=pagedata)
 
@app.route('/api/hello/')
def apidemo():
  ret={}
  ret['name']='Masa'
  ret['age']=12345
  return json.dumps(ret)

@app.route('/', methods=['GET'])
@app.route('/index.html')
@app.route('/test/')
def index2():
  pagedata={'zone':'', 'authns':'', 'zonefile':''}
  pagedata['console']='get method'
  #pagedata['table']=[(True,2,3), (False,4,5)]
  pagedata['table']=[]
  pagedata['action'] = '/'
  return render_template('crenz_ajax.html', pd=pagedata)


@app.route('/', methods=['POST'])
@app.route('/test/', methods=['POST'])
def post2():
  pagedata={}
  pagedata['authns']=request.form['authns'].strip()
  pagedata['zone']=request.form['zone'].strip()
  pagedata['zonefile']=request.form['zonefile']
  pagedata['action'] = '/'
  
  try:
    zonename=None
    if pagedata['zone'] != '':
      zonename = pagedata['zone']
    dt = DnsTester( request.form['authns'], zonename)
    dt.load_txt( pagedata['zonefile'].replace('\r\n', '\n') )
    #pagedata['console']='done'
    ret = dt.zone_check()
  except Exception as err:
    pagedata['console']= 'err: {}\n{}'.format(err, sys.exc_info())  
    ret = []

  pagedata['table']=ret
  #return render_template('crenz.html', pd=pagedata)
  #time.sleep(1)
  #return json.dumps(request.form)
  return json.dumps(pagedata)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000,debug = True)


