from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import pymysql
import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
db = pymysql.connect(host='localhost',user='root',password='',database='dbitfest')
c = db.cursor()


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def studentreg(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        id = request.session['id']
        s = "select count(*) from tbl_student where semail='"+str(email)+"'"
        c.execute(s)
        msg = "Already Registered"
        i = c.fetchone()
        if(i[0] == 0):
            img = request.FILES["idproof"]
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
            uploaded_file_url = fs.url(filename)
            s = "insert into tbl_student (sname,saddress,scontact,semail,idproof,status, colid) values('"+str(
                name)+"','"+str(address)+"','"+str(contact)+"','"+str(email)+"','"+uploaded_file_url+"','0','"+str(id)+"')"
            c.execute(s)

            db.commit()
            s = "insert into tbl_login(username,password,usertype) values('" + \
                str(email)+"','"+str(contact)+"','Student')"
            c.execute(s)
            msg = "Regitration Successfull"
            db.commit()
    return render(request, "studentregistration.html", {"msg": msg})


def login(request):
    msg = ""
    if(request.POST):
        email = request.POST.get("username")
        password = request.POST.get("password")
        s = "select count(*) from tbl_login where username='" + \
            str(email)+"' and password='"+str(password)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] == 0):
            msg = "Invalid Credentials"
        else:
            s = "select * from tbl_login where username='" + \
                str(email)+"' and password='"+str(password)+"'"
            c.execute(s)
            y = c.fetchone()
            request.session['id'] = y[0]

            if y[3] == 'Admin':
                return HttpResponseRedirect("/adminhome")
            elif y[3] == 'Student':
                s = "select * from tbl_student where semail='"+str(email)+"' "

                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]

                return HttpResponseRedirect("/studenthome")
            elif y[3] == 'College':
                s = "select * from college where email='"+str(email)+"' "

                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]

                return HttpResponseRedirect("/collegehome")
            elif y[3] == 'Company':
                s = "select * from company where email='"+str(email)+"' "

                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]

                return HttpResponseRedirect("/companyhome")
            elif y[3] == 'Coordinator':
                s = "select * from tbl_coordinator where email='" + \
                    str(email)+"'"

                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]
                return HttpResponseRedirect("/coordinatorhome")
            elif y[3] == 'Judge':
                s = "select * from tbl_judge where email='"+str(email)+"'"
                print(s)
                c.execute(s)
                y = c.fetchone()
                request.session['id'] = y[0]
                return HttpResponseRedirect("/judgehome")
    return render(request, "login.html", {"msg": msg})


def adminhome(request):
    return render(request, "adminhome.html")


def studenthome(request):
    return render(request, "studenthome.html")


def judgehome(request):
    return render(request, "judgehome.html")


def coordinatorhome(request):
    return render(request, "coordinatorhome.html")


def collegehome(request):
    return render(request, "collegehome.html")


def companyhome(request):
    return render(request, "companyhome.html")


def approvestudents(request):
    c.execute(
        "SELECT * FROM `tbl_student` s, `college` c WHERE s.`colid` = c.`colid` AND s.`status` = '0'")
    j = c.fetchall()
    return render(request, "approvestudents.html", {"j": j})


def acceptstudent(request):
    id = request.GET.get("id")
    s = "update tbl_student set status='1' where id='"+str(id)+"'"
    c.execute(s)
    db.commit()
    return HttpResponseRedirect("/approvestudents")


def addcoordinator(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        place = request.POST.get("place")
        email = request.POST.get("email")
        password = request.POST.get("password")
        s = "select count(*) from tbl_coordinator where email='"+str(email)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] == 0):

            s = "insert into tbl_coordinator(name,address,contact,place,email,status) values('"+str(
                name)+"','"+str(address)+"','"+str(contact)+"','"+str(place)+"','"+str(email)+"','1')"
            c.execute(s)
            db.commit()
            s = "insert into tbl_login(username,password,usertype) values('" + \
                str(email)+"','"+str(password)+"','Coordinator')"
            c.execute(s)
            msg = "Coordinator Added"
            db.commit()
    return render(request, "addcoordinator.html", {"msg": msg})


def addjudge(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST.get("name")

        contact = request.POST.get("contact")
        place = request.POST.get("place")
        email = request.POST.get("email")
        password = request.POST.get("password")

        s = "select count(*) from tbl_judge where email='"+str(email)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] == 0):
            img = request.FILES["image"]
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
            uploaded_file_url = fs.url(filename)
            s = "insert into tbl_judge (name,contact,place,email,image,status) values('"+str(
                name)+"','"+str(contact)+"','"+str(place)+"','"+str(email)+"','"+uploaded_file_url+"','1')"
            c.execute(s)
            db.commit()
            s = "insert into tbl_login(username,password,usertype) values('" + \
                str(email)+"','"+str(password)+"','Judge')"
            msg = "Judge Added"
            c.execute(s)
            db.commit()
    return render(request, "addjudge.html", {"msg": msg})


def addevent(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST.get("eventname")
        edate = request.POST.get("eventdate")
        venue = request.POST.get("place")
        time = request.POST.get("time")
        cor = request.POST.get("cor")

        s = "select count(*) from tbl_event where ename='"+str(name)+"'"
        c.execute(s)
        i = c.fetchone()
        if(i[0] == 0):

            s = "insert into tbl_event(ename,edate,venue,etime, cid) values('"+str(
                name)+"','"+str(edate)+"','"+str(venue)+"','"+str(time)+"','"+str(cor)+"')"
            c.execute(s)
            msg = "Event Added"
            db.commit()
    qry = "SELECT * FROM `tbl_coordinator`"
    c.execute(qry)
    row = c.fetchall()
    context = {"msg": msg, "datas": row}
    return render(request, "addevent.html", context)


def viewevents(request):
    c.execute("select * from tbl_event")
    j = c.fetchall()
    print(j)
    return render(request, "viewevents.html", {"j": j})


def participate(request):
    s = ""

    participantid = request.session['id']
    eid = request.GET.get("id")
    participantid = request.session['id']
    s = "select count(*) from tbl_participants where eventid='" + \
        str(eid)+"' and pid='"+str(participantid)+"'"
    c.execute(s)
    msg = "Already Participated"
    i = c.fetchone()
    if(i[0] == 0):
        return HttpResponseRedirect("/participateevent?id="+eid)
    else:
        return HttpResponseRedirect("/viewevents")


def participateevent(request):
    eid = request.GET.get("id")
    participantid = request.session['id']
    if request.POST:
        img = request.FILES["txtfile"]
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        s = "insert into tbl_participants(pid,eventid,efile) values('"+str(
            participantid)+"','"+str(eid)+"','"+uploaded_file_url+"')"
        c.execute(s)
        db.commit()
        return HttpResponseRedirect("/viewevents")
    return render(request, "participate.html")


def selectjudge():
    data = ""
    c.execute("select * from tbl_judge")
    data = c.fetchall()
    return data


def selectevent(id):
    data = ""
    c.execute(f"SELECT * FROM `tbl_event` WHERE `cid` = '{id}'")
    data = c.fetchall()
    return data


def allocatejudge(request):
    m = ""
    msg = ""
    if(request.POST):

        eventid = request.POST.get("eventid")
        judgeid = request.POST.get("judgeid")
        m = "select count(*) count from tbl_allocation where eventid='" + \
            str(eventid)+"' and judgeid='"+str(judgeid)+"'"
        c.execute(m)
        msg = "Already Allocated"
        i = c.fetchone()
        if(i[0] == 0):
            m = "insert into tbl_allocation(eventid,judgeid) values('" + \
                str(eventid)+"','"+str(judgeid)+"')"
            c.execute(m)
            msg = "Allocated"
            db.commit()
    id = request.session['id']
    name = selectjudge()
    ename = selectevent(id)
    return render(request, "allocatejudge.html", {"m": m, "ename": ename, "name": name, "msg": msg})


def viewallocation(request):
    judgeid = request.session['id']
    c.execute("SELECT tbl_event.id, tbl_event.`ename`,tbl_event.`edate`,tbl_event.`etime`,tbl_event.`venue` FROM tbl_judge,tbl_event,tbl_allocation WHERE tbl_judge.id=tbl_allocation.`judgeid` AND tbl_event.`id`=tbl_allocation.`eventid` AND judgeid='"+str(judgeid)+"'")
    s = c.fetchall()
    print(s)
    return render(request, "viewallocation.html", {"s": s})
# def plist(request):
#     # plistid=request.GET.get("id")
#     # ename=request.GET.get("ename")
#     s="SELECT tbl_student.id,tbl_student.`sname`,tbl_student.`scontact`,tbl_student.`idproof`,tbl_event.`ename` FROM tbl_student,tbl_event,tbl_participants WHERE tbl_student.`id`=tbl_participants.`pid` AND tbl_event.`id`=tbl_participants.`eventid`"
#     c.execute(s)
#     j=c.fetchall()
#     print(j)
#     return render(request,"plist.html",{"j":j})


def viewparticipants(request):
    c.execute("SELECT tbl_student.`sname`,tbl_student.`semail`,tbl_student.`idproof`,tbl_event.`ename` FROM tbl_student,tbl_event,tbl_participants WHERE tbl_student.`id`=tbl_participants.`pid` AND tbl_event.`id`=tbl_participants.`eventid`")
    j = c.fetchall()
    print(j)
    return render(request, "viewparticipant.html", {"j": j})


def viewwinner(request):
    return render(request, "viewwinner.html")


def viewmarks(request):
    studid = request.session['id']
    c.execute("SELECT tbl_mark.`eventid`,tbl_mark.`score` FROM tbl_mark,tbl_student WHERE tbl_mark.pid=tbl_student.`id`AND tbl_student.`id`='"+str(studid)+"'")
    j = c.fetchall()
    print(j)
    return render(request, "viewmarks.html", {"j": j})
# def viewwinnersstud(request):
#     c.execute("SELECT tbl_student.`sname`,winner.ename,winner.score FROM tbl_student,winner WHERE tbl_student.`id`=winner.pid")
#     j=c.fetchall()
#     print(j)
#     return(request,"viewwinnersstud.html",{"j":j})


def addmarks(request):
    judgeid = request.session['id']
    m = "SELECT tbl_event.`id`,tbl_event.`ename` FROM tbl_allocation,tbl_event WHERE tbl_event.id=tbl_allocation.`eventid` and tbl_allocation.judgeid='" + \
        str(judgeid)+"'"
    c.execute(m)
    # c.execute("SELECT tbl_student.`id`, tbl_student.`sname`,tbl_student.`idproof` ,tbl_event.`ename` FROM tbl_student,tbl_event,tbl_participants,tbl_allocation  WHERE tbl_student.`id`=tbl_participants.`pid` AND tbl_event.`id`=tbl_participants.`eventid` AND tbl_event.`ename`='Campzotica' AND tbl_allocation.`judgeid`='"+str(judgeid)+"'")
    j = c.fetchall()
    print(j)
    return render(request, "addmarks.html", {"j": j})


def plist(request):
    id = request.GET.get("id")
    # ename=request.GET.get("ename")
    c.execute("SELECT tbl_participants.pid,tbl_event.`ename`,tbl_student.`sname`,tbl_student.`idproof`,tbl_student.`scontact` FROM tbl_student,tbl_participants,tbl_event WHERE tbl_event.id=tbl_participants.`eventid` AND tbl_participants.pid=tbl_student.`id` and tbl_participants.eventid='"+str(id)+"'")
    j = c.fetchall()
    print(j)
    return render(request, "plist.html", {"j": j})


def addmarksjudge(request):
    msg = ""
    pid = request.GET.get("id")
    eventname = request.GET.get("eid")
    judgeid = request.session['id']
    s = "select id from tbl_event where ename='"+eventname+"'"
    c.execute(s)
    d = c.fetchone()
    eid = d[0]
    s = "select * from tbl_participants where eventid='" + \
        str(eid) + "' and pid='"+str(pid)+"'"
    c.execute(s)
    d = c.fetchone()
    img = d[3]
    if(request.POST):

        tscore = request.POST.get("tscore")
        s = "select count(*) from tbl_mark where pid='" + \
            str(pid)+"' and eventname='"+str(eventname)+"'"
        c.execute(s)
        msg = "Already mark Added"
        i = c.fetchone()
        if(i[0] == 0):

            s = "insert into tbl_mark(pid,eventname,judgeid,score) values('"+str(
                pid)+"','"+str(eventname)+"','"+str(judgeid)+"','"+str(tscore)+"')"
            c.execute(s)
            msg = "Mark Added"
            db.commit()
    return render(request, "addmarksjudge.html", {"msg": msg, "img": img})


def addwinner(request):
    c.execute("SELECT DISTINCT tbl_participants.`pid`,tbl_student.`sname`,tbl_student.`scontact`,tbl_mark.eventname,tbl_judge.`name` AS judgename,tbl_mark.`score` FROM tbl_participants,tbl_mark,tbl_judge,tbl_student WHERE tbl_student.`id`=tbl_participants.`pid` and tbl_mark.pid=tbl_participants.`pid` AND tbl_mark.`judgeid`=tbl_judge.`id` and tbl_mark.eventname not in(select ename from winner)")
    j = c.fetchall()
    print(j)
    return render(request, "addwinner.html", {"j": j})


def winner(request):
    pid = request.GET.get("id")
    ename = request.GET.get("ename")
    score = request.GET.get("score")
    s = "select count(*) from winner where pid='" + \
        str(pid)+"' and ename='"+str(ename)+"'"
    c.execute(s)
    msg = "Already Added"
    i = c.fetchone()
    if(i[0] == 0):

        s = "insert into winner(pid,ename,score) values('" + \
            str(pid)+"','"+str(ename)+"','"+str(score)+"')"
        c.execute(s)
        msg = "Winner..."
        db.commit()
    return render(request, "addwinner.html", {"msg": msg})


def addfeedback(request):
    s = ""
    msg = ""
    if(request.POST):
        studentid = request.session['id']
        feedback = request.POST.get("feedback")

        s = "insert into tbl_feedback(studentid,feedback) values('" + \
            str(studentid)+"','"+str(feedback)+"')"
        msg = "Feedback Added"
        c.execute(s)
        db.commit()
    return render(request, "addfeedback.html", {"msg": msg})


def viewfeedback(request):
    c.execute("SELECT tbl_student.`sname`,tbl_feedback.feedback FROM tbl_student,tbl_feedback WHERE tbl_student.id=tbl_feedback.studentid")
    j = c.fetchall()
    print(j)
    return render(request, "viewfeedback.html", {"j": j})


def viewwinnerstudent(request):
    c.execute("SELECT tbl_student.`sname`,winner.ename,winner.score FROM tbl_student,winner WHERE tbl_student.`id`=winner.pid")
    j = c.fetchall()
    print(j)
    return render(request, "viewwinnersstud.html", {"j": j})


def studentviewrecruit(request):
    id = request.session['id']
    c.execute(
        f"SELECT * FROM `recruitment` r, `tbl_student` s, `company` c WHERE r.`comid`=c.`comid` AND s.`id`=r.`sid` AND r.`sid`='{id}'")
    j = c.fetchall()
    print(j)
    return render(request, "studentviewrecruit.html", {"j": j})


def judviewwinnerstudent(request):
    c.execute("SELECT tbl_student.`sname`,winner.ename,winner.score FROM tbl_student,winner WHERE tbl_student.`id`=winner.pid")
    j = c.fetchall()
    print(j)
    return render(request, "judviewwinnersstud.html", {"j": j})


def colviewwinners(request):
    c.execute("SELECT tbl_student.`sname`,winner.ename,winner.score FROM tbl_student,winner WHERE tbl_student.`id`=winner.pid")
    j = c.fetchall()
    print(j)
    return render(request, "colviewwinners.html", {"j": j})


def comviewwinners(request):
    c.execute("SELECT tbl_student.`sname`,winner.ename,winner.score, tbl_student.`id` FROM tbl_student,winner WHERE tbl_student.`id`=winner.pid")
    j = c.fetchall()
    print(j)
    return render(request, "comviewwinners.html", {"j": j})


def comViewRecruit(request):
    comid = request.session['id']

    c.execute(
        f"SELECT * FROM `recruitment` r, `tbl_student` s, `company` c WHERE r.`comid`='{comid}' AND s.`id`=r.`sid` AND c.`comid`=r.`comid`")
    j = c.fetchall()
    print(j)
    return render(request, "comViewRecruit.html", {"j": j})


def recruit(request):
    sid = request.GET.get("id")
    comid = request.session['id']
    today = date.today()
    s = "select count(*) from recruitment where sid='" + \
        str(sid)+"' and comid='"+str(comid)+"'"
    c.execute(s)
    msg = "Already Send"
    i = c.fetchone()
    if(i[0] == 0):
        s = f"INSERT INTO `recruitment` (`sid`,`comid`,`date`) VALUES ('{sid}','{comid}','{today}')"
        c.execute(s)
        msg = "Recruitment send..."
        db.commit()
    return redirect("comViewRecruit")


def collegereg(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        desc = request.POST['desc']
        password = request.POST['password']
        s = f"select count(*) from college where email='{email}'"
        c.execute(s)
        msg = "Already Registered"
        i = c.fetchone()
        if(i[0] == 0):
            s = f"INSERT INTO `college`(`name`,`email`,`contact`,`address`,`desc`) VALUES ('{name}','{email}','{contact}','{address}','{desc}')"
            c.execute(s)

            db.commit()
            s = f"insert into tbl_login(username,password,usertype) values('{email}','{password}','College')"
            c.execute(s)
            msg = "Regitration Successfull"
            db.commit()

        msg = "Registration Successful..."
        c.execute(s)
        db.commit()
    return render(request, "collegeregistration.html", {"msg": msg})


def companyreg(request):
    s = ""
    msg = ""
    if(request.POST):
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        desc = request.POST['desc']
        password = request.POST['password']

        s = f"select count(*) from company where email='{email}'"
        c.execute(s)
        msg = "Already Registered"
        i = c.fetchone()
        if(i[0] == 0):
            s = f"INSERT INTO `company`(`name`,`email`,`contact`,`address`,`desc`) VALUES ('{name}','{email}','{contact}','{address}','{desc}')"
            c.execute(s)

            db.commit()
            s = f"insert into tbl_login(username,password,usertype) values('{email}','{password}','Company')"
            c.execute(s)
            msg = "Regitration Successfull"
            db.commit()

        msg = "Registration Successful..."
    return render(request, "companyregistration.html", {"msg": msg})
# Create your views here.
