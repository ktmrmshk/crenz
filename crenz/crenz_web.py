from flask import Flask, render_template, Markup, request
import sys
from crenz.dns_tester import DnsTester

app=Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index.html')
def index():
  pagedata={'zone':'', 'authns':'', 'zonefile':''}
  pagedata['console']='get method'
  #pagedata['table']=[(True,2,3), (False,4,5)]
  pagedata['table']=[]
  pagedata['action'] = '/'
  return render_template('crenz.html', pd=pagedata)


@app.route('/', methods=['POST'])
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
  

if __name__ == "__main__":
  app.run(debug = True)


