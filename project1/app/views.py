from django.shortcuts import render,redirect
import io
from .models import Articles
from django.views.generic import ListView, DetailView, CreateView
from .forms import ArticleForm, AuthUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.conf import settings
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def home(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_excel(file)
        print(df)
        df1 = df[['Гумус']]
        df = df[['red color', 'green color', 'blue color', "8 канал", "7 канал","6 канал","5 канал","4 канал","3 канал","2 канал","1 канал", ]]
        predicted_humus_concentration = 42  # Пример предсказанной концентрации гумуса
        print(df)
        df2=df[69:70]

        print(df2)

        df=df[0:69]
        soil_data = np.array(df)
        df1=df1[0:69]
        # print(df)
        # print(len(df))

        
        # soil_data = ([[0.5, 0.6, 0.3] , [0.8, 0.3, 0.9], [1, 0.3, 10], [2, 0.3, 20]])t
        
        # Шаг 1: Загрузка обучающей выборки
        # Предположим, что у вас есть массив данных soil_data, содержащий значения цветовых каналов и концентрацию гумуса

        # Шаг 2: Нормализация значений цветовых каналов
        normalized_data = (soil_data - np.min(soil_data, axis=0)) / (np.max(soil_data, axis=0) - np.min(soil_data, axis=0))
        # normalized_data =  normalized_data.fillna()
        # normalized_data
        # Шаг 3: Выбор количества кластеров k
        k = 65  # например, выбираем 3 кластера

        # Шаг 4: Инициализация центроидов
        kmeans = KMeans(n_clusters=k, init='random')

        # Шаг 5: Обучение модели методом k-средних
        kmeans.fit(normalized_data)
        known_humus_concentration = df1
        plt.scatter(normalized_data[:, 0], normalized_data[:, 1], c=kmeans.labels_, cmap='viridis')
        centers = kmeans.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
        # Шаг 6: Получение концентрации гумуса для каждого кластера
        # Предположим, что у вас есть массив known_humus_concentration, содержащий известные значения концентрации гумуса
        cluster_labels = kmeans.predict(normalized_data)
        cluster_humus_concentration = [np.mean(known_humus_concentration[cluster_labels == i]) for i in range(k)]

        # Шаг 7: Предсказание концентрации гумуса для новых значений цветовых каналов

        new_data = np.array([[58,43, 36, 2034, 1807,1702,1614,1568,1431,1350,1323]])
        new_data = np.array(df2) # пример новых значений цветовых каналов
        new_normalized_data = (new_data - np.min(soil_data, axis=0)) / (np.max(soil_data, axis=0) - np.min(soil_data, axis=0))
        predicted_cluster = kmeans.predict(new_normalized_data)
        predicted_humus_concentration = float(cluster_humus_concentration[predicted_cluster[0]])
        fig, ax = plt.subplots()
        ax.scatter(normalized_data[:, 0], normalized_data[:, 1], c=kmeans.labels_, cmap='viridis')
        centers = kmeans.cluster_centers_
        ax.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        # Преобразуйте изображение в base64 строку
        graphic = base64.b64encode(image_png).decode('utf-8')
        print(graphic)
        print("Предсказанная концентрация гумуса:", predicted_humus_concentration)
        print(new_data[0][0])
        # print(cluster_humus_concentration[predicted_cluster])
        return render(request, 'edit_page.html', {'nd' : new_data[0], 'graphic': graphic,'humus_concentration': predicted_humus_concentration})
    
    return render(request, 'home.html')

# class HomeListView(ListView):
#     model = Articles
#     template_name = 'index.html'
#     context_object_name = 'list_articles'


class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Пользователь успешно создан'
    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username,password=password)
        login(self.request, aut_user)
        return form_valid

class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('edit_page')

class HomeDetailView(DetailView):
    model = Articles
    template_name = 'detail.html'
    context_object_name = 'get_article'

def edit_page(request):
    success = False
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
    
    template = 'edit_page.html'
    context = {
        'list_articles': Articles.objects.all().order_by('-id'),
        'form':ArticleForm(),
        'success':success
    }
    return render(request,template,context)
    
    
def update_page(request,id):
    success_update = False
    get_article = Articles.objects.get(pk=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST,instance = get_article)
        if form.is_valid():
            form.save()
            success_update = True
    template = 'edit_page.html'
    context = {
        'get_article': get_article,
        'update':True,
        'form':ArticleForm(instance = get_article),
        'success_update':success_update
        
    }
    dal="user2"
    login = str(request.user)
    print(type(str(request.user)))
   
    if login== "user22":
            return redirect(reverse('edit_page'))
    
    return render(request, template, context)
   
        

def delete_page(request,id):
    
    get_article = Articles.objects.get(pk=id)
    get_article.delete()
    
    return redirect(reverse('edit_page'))
