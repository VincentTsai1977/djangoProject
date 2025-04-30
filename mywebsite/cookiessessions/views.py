from django.shortcuts import render, redirect
from django.http import HttpResponse
# import datetime
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

# Create your views here.
def set_cookie(request, key, value):
    response = HttpResponse("Cookie 設定成功")
    response.set_cookie(key, value)
    return response

def get_cookie(request, key):
    if key in request.COOKIES:
        value = request.COOKIES.get(key)
        return HttpResponse(f"Cookie {key} 的值是: {value}")
    else:
        return HttpResponse(f"Cookie {key} 不存在")

# 加入有效時間
def set_cookie2(request, key, value):
    response = HttpResponse("Cookie 設定成功，有效時間是1個小時")
    response.set_cookie(key, value, max_age=10)
    return response

def get_allcookies(request):
    # 判斷COOKIES是否有值
    if request.COOKIES != None:
        # 取得COOKIES的值
        strCookies = ""
        for key, value in request.COOKIES.items():
            strCookies += f"{key}: {value}" + "<br>"
        return HttpResponse(strCookies)
    else:
        return HttpResponse("COOKIES 沒有值")

def delete_cookie(request, key):
    if key in request.COOKIES:
        response = HttpResponse("Cookie 刪除成功: " + key)
        response.delete_cookie(key)
        return response
    else:
        return HttpResponse(f"Cookie {key} 不存在")

# session========================================
def set_session(request, key, value):
    response = HttpResponse("Session 設定成功")
    request.session[key] = value
    return response

def get_session(request, key):
    if key in request.session:
        value = request.session.get(key)
        return HttpResponse(f"Session {key} 的值是: {value}")
    else:
        return HttpResponse(f"Session 不存在")
    
def set_session2(request, key=None, value=None):
    response = HttpResponse("Session 設定成功")
    request.session(key, value)
    # 設定session有效時間為30秒
    request.session.set_expiry(30)
    return response

def get_allsessions(request):
    # 判斷COOKIES是否有值
    if request.session != None:
        # 取得COOKIES的值
        strSessions = ""
        for key, value in request.session.items():
            strSessions += f"{key}: {value}" + "<br>"
        return HttpResponse(strSessions)
    else:
        return HttpResponse("session 沒有值")

def delete_session(request, key):
    if key in request.session:
        response = HttpResponse("Session 刪除成功: " + key)
        response.delete_session(key)
        return response
    else:
        return HttpResponse(f"Session 不存在")

def cookie_session(request):
    if "counter" in request.COOKIES:
        # 取得COOKIES的值並轉成整數
        counter = int(request.COOKIES.get("counter"))
        counter += 1
    else:
        counter = 1
    response = HttpResponse("今天訪問次數: " + str(counter))
    #                目前系統時間       +  1天
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%Y-%m-%d %H:%M:%S GMT")
    # 設定COOKIES的值
    response.set_cookie("counter", counter, expires=expires)
    return response

def vote(request):
    if not "vote" in request.session:
        request.session["vote"] = True
        message = "謝謝您的投票"
    else:
        message = "您已經投過票"
    return HttpResponse(message)

def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        # 使用 Django 內建的使用者認證系統驗證
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 使用者驗證成功
            auth_login(request, user)
            request.session["username"] = username
            message = "登入成功！歡迎回來，" + username
            status = "login"
        else:
            # 使用者驗證失敗
            message = "帳號或密碼錯誤，請重新輸入"
            status = "logout"
    else:
        # 檢查是否已經通過Django驗證
        if request.user.is_authenticated:
            # 如果用戶已經通過驗證但還沒有session username
            if "username" not in request.session:
                request.session["username"] = request.user.username
            message = f"您已經成功登入系統，歡迎回來，{request.user.username}"
            status = "login"
        elif "username" in request.session:
            message = "您已經成功登入系統"
            status = "login"
        else:
            message = ""
            status = "logout"
    return render(request, "cookiessessions/login.html", locals())

def logout(request):
    if request.user.is_authenticated or "username" in request.session:
        if "username" in request.session:
            message = request.session["username"] + " 已成功登出系統"
            del request.session["username"]
        else:
            message = request.user.username + " 已成功登出系統"
        auth_logout(request)
    else:
        message = "您尚未登入系統"
    status = "logout"
    return render(request, "cookiessessions/login.html", locals())
