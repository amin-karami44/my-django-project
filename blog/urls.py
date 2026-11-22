from django.urls import path
from . import views

app_name = 'blog'
urlpatterns=[
    path('',views.index ,name='index'),
    path('postlist/',views.postlist,name='post_list'),
    #path('postlist/',views.PostList.as_view(),name='post_list'),
    path('postdetail/<slug:slug>/<int:pk>/',views.postdetail,name='post_detail'),
    path('account-form/',views.UserAccount,name='account_form'),
    path('contact-us/',views.ContactUs,name='contact_us'),
    path('share-post/<int:post_id>/',views.SharePost,name='share_post'),
]
