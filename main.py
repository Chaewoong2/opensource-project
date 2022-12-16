from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.remoteok import extract_remoteok_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper") # app 변수 초기화

db = {} # 재 검색 시 가짜 db

@app.route("/") # reply to user -> ("/") 접속 시 아래 함수 실행
def home():
  return render_template("home.html") # html을 data 변수로 변환

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:  # 검색어 없이 접속 시 
    return redirect("/")  # go back home
  if keyword in db:
    jobs = db[keyword]
  else:
    indeed = extract_indeed_jobs(keyword)
    remoteok = extract_remoteok_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = indeed + remoteok + wwr
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export(): # 검색어 없이, 검색 과정 없이 접속 대응
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect("/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0") # app 실행 / replit -> web server ("0.0.0.0") 계속 실행