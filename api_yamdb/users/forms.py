from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from users.models import MyUser


def get_generated_confirmation_code():
    """Генерирует код подтверждения - confirmation_code."""
    return get_random_string(25)


def send_confirmation_code(request):
    """Отправляет сгенерированный confirmation_code пользователю."""
    user = get_object_or_404(
        MyUser,
        username=request.data.get('username'),
    )
    user.confirmation_code = get_generated_confirmation_code()
    user.save()
    send_mail(
        subject='Код для получения токена',
        message=f'Код подтверждения {user.confirmation_code}',
        from_email='confirmation_code@yamdb.ru',
        recipient_list=[request.data.get('email')],
    )


class SignupView(APIView):
    """Вью для регистрации пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод POST."""
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)