# coding: utf-8
from django.core import mail
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from .models import Subscription
from django.db import IntegrityError
from .forms import SubscriptionForm

'''
Testa a Rota
'''
class SubscriptionUrlTest(TestCase):
    def test_get_subscribe_page(self):
        response = self.client.get(reverse('subscriptions:subscribe'))
        self.assertEquals(200, response.status_code)

'''
Testa a View
'''
class SubscriptionViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse('subscriptions:subscribe'))

    def test_get(self):
        "Ao visitar /inscricao/ a página de inscricao é exibida."
        self.assertEquals(200, self.resp.status_code)

    def test_use_template(self):
        "A reposta dever renderizada por um template"
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        "A resposta deve ser o form de Inscricao"
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)

    def test_has_fields(self):
        "O formulario deve conter os campos: name, email, cpf e phone"
        form = self.resp.context['form']
        self.assertItemsEqual(['name', 'email', 'cpf', 'phone'], form.fields)

    def test_html(self):
        "O html deve conter os campos do formulário"
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 4)
        self.assertContains(self.resp, 'type="submit"')

'''
Testa o Modelo
'''
class SubscriptionModelTest(TestCase):
    def setUp(self):
        "O model deve ter: nome, cpf, email, phone, created_at"
        Subscription.objects.create(name = 'Joe Doe', cpf = '12345678900', email = 'joe@doe.com',
               phone = '99-9999-9999')


    def test_cpf_unique(self):
        "CPF deve ser unico."
        s = Subscription(name = 'Joe Doe2', cpf = '12345678900', email = 'joe1@doe.com',
            phone = '89-9999-9999'
        )

        self.assertRaises(IntegrityError, s.save)

    def test_email_unique(self):
        "O Email deve ser único"
        s = Subscription(name = 'Joe Do3e', cpf = '12345678901', email = 'joe@doe.com',
            phone = '79-9999-9999'
        )
        self.assertRaises(IntegrityError, s.save)


'''
Testa o Post'do formulário
'''
class SubscribeViewPostTest(TestCase):
    def setUp(self):
        data = dict(name = 'Joe Doe', cpf = '12345678900', email = 'joe@doe.com',
            phone = '99-9999-9999')
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)


    def test_redirects(self):
        "Post deve redirecionar para a pagina de sucesso."
        self.assertRedirects(self.resp, reverse('subscriptions:success', args=[1]))

    def test_save(self):
        "Post deve salvar a Inscrição no banco."
        self.assertTrue(Subscription.objects.exists())

    def test_email_sent(self):
        "Post deve notificar o visitante por email."
        self.assertEquals(1, len(mail.outbox))

'''
Testa os casos de posts invalidos
'''
class SubscribeViewInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name = 'Joe Doe', cpf = '123456789001', email = 'joe@doe.com',
            phone = '99-9999-9999')
        self.resp = self.client.post(reverse('subscriptions:subscribe'), data)

    def test_show_page(self):
        "Post invalido nao pode redirecionar."
        self.assertEqual(200, self.resp.status_code)

    def test_form_errors(self):
        "Form deve conter erros."
        self.assertTrue(self.resp.context['form'].errors)

    def test_must_not_save(self):
        "Dados nao devem ser salvos"
        self.assertFalse(Subscription.objects.exists())

'''
Testa a pagina de confirmação de inscrição
'''
class SuccessViewTest(TestCase):
    def setUp(self):
        s = Subscription.objects.create(name = 'Joe Doe', cpf = '12345678900', email = 'joe@doe.com',
            phone = '99-9999-9999')
        self.resp = self.client.get(reverse('subscriptions:success', args=[s.pk]))

    def test_get(self):
        "Verifica a existencia da página de sucesso"
        self.assertEquals(200, self.resp.status_code)

    def test_get(self):
        "Verifica o uso do template"
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        "Verifica se no contexto tem objeto de subscription"
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        "Pagina deve conter nome do cadastrado."
        self.assertContains(self.resp, 'Joe Doe')


'''
Confirma pagina de erro para cadastro inexistente
'''
class SuccessViewNotFound(TestCase):
    def test_not_found(self):
        "Acesso a inscrição não cadastrada deve retornar 404."
        response = self.client.get(reverse('subscriptions:success', args=[0]))
        self.assertEqual(404, response.status_code)
