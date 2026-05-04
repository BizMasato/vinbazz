# views.py
from admin_apps.user.models import CustomUser
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout, get_user
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.conf import settings
from .utils import account_activation_token
import json

# 開発環境用
import smtplib
import ssl
from email.mime.text import MIMEText

@csrf_exempt  # TODO CSRFトークンを無効にする（開発中のみ推奨）
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # ユーザーが既に存在しているかをチェック
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'このメールアドレスは既に使用されています。'}, status=400)

        # 新しいユーザーを作成
        user = CustomUser.objects.create_user(email=email, password=password)
        user.is_active = False  # 認証されるまで無効化
        user.save()

        # 認証メールを送信
        current_site = get_current_site(request)
        mail_subject = '【vinbazz】アカウントの認証をお願いします'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        # メールテンプレート
        email_template_name = 'activation_email.html'

        message = render_to_string(email_template_name, {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })

        if __debug__:
            # 開発環境用
            send_mail_with_ssl_disabled(
                mail_subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
        else:
            # 本番環境用
            send_mail(
                mail_subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        return JsonResponse({'message': 'ユーザー登録が成功しました。確認メールを送信しました。'})
    
    return JsonResponse({'error': '無効なリクエストです。'}, status=400)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    # ユーザーがNoneの場合、有効化不可のため即時エラー
    if user is None:
        return redirect('http://localhost:3000/activation_expired?message=isvalid')
    else:
        # トークンが有効かを確認
        if not account_activation_token.check_token(user, token):
            user.delete()
            return redirect('http://localhost:3000/activation_expired?message=isvalid')

        # トークンの有効期限を先にチェック
        if not account_activation_token.check_token_expiration(token):
            user.delete()
            return redirect('http://localhost:3000/activation_expired')


        # アカウントを有効化
        user.is_active = True
        user.save()
        return redirect('http://localhost:3000/activation_complete')  # フロントの認証完了ページにリダイレクト


# 開発環境用
def send_mail_with_ssl_disabled(subject, message, from_email, recipient_list):
    # SSLの検証を無効にするためのコンテキストを作成
    context = ssl._create_unverified_context()
    
    # メールの件名と本文をMIMETextで作成
    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.ehlo()
        server.starttls(context=context)  # SSLを無効にして接続
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(from_email, recipient_list, msg.as_string())  # MIMETextを使って送信


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600)  # 2週間
            request.session.cycle_key()  # 新しいセッションキーを生成
            response = JsonResponse({"message": "ログイン成功"}, status=200)
            return response
        else:
            return JsonResponse({"error": "メールアドレス、またはパスワードが違います。再度確認して入力してください。"}, status=400)
    return JsonResponse({"error": "POSTリクエストのみ許可されています"}, status=405)


@csrf_exempt
def user_logout(request):
    logout(request)
    response = JsonResponse({"message": "ログアウト成功成功"}, status=200)
    return response


def check_session(request):
    # ユーザーの認証状態と名前を返す
    user = get_user(request)
    if user.is_authenticated:
        return JsonResponse({'isAuthenticated': True, 'username': user.username})
    else:
        return JsonResponse({'isAuthenticated': False})
