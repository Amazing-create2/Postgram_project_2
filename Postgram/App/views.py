from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile , Post, Reels,Story
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.db.models import Q
 

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("Login")

    posts = Post.objects.filter(Q(profile__followers=request.user)& ~Q(likes=request.user))
    story = Story.objects.filter(profile__followers=request.user)
    context = {"posts":posts,'stories':story}
    return render(request,'index.html',context)

#LOGIN VIEW FOR USER
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            Login(request,user)
            return redirect("profile") 
    return render(request,'Login.html')

#CREATE PROFILE AND USER SIGNUP VIEW
def create_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['image']
        user = User.objects.create_user(username=username,password=password)
        profile = Profile.objects.create(user=user,profile_picture=image)
        if profile:
            messages.succes(request,'Profile Created Please Login')
            return redirect("logic")
    return render(request,'SignUp.html')

#FOR RENDERING THE PROFILE PAGE
def profile(request,id=None):
    if not request.user.is_authenticated:
        return redirect("Login")

    if id is not None:
        profile = profile.objects.get(id=id)
        posts = Post.objects.filter(profile=profile)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
    else:
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(user=request.user)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
        return render(request,'profile.html',{'profile':profile,'profileimage':profileimage,
        'profile_of_user':True,'posts':posts,'posts_num':posts_num})    



def Logout(request):
    logout(request)
    return redirect("Login")

def search(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile_id = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url      
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url       
    search = request.GET['username']
    #ICONTAINS IS USED TO MAKE OUR SERACH MORE CAPITAL OR SMALL LETTERS FAMILIER
    profiles = Profile.objects.filter(user__username__icontains=search) #THIS WILL GIVE US RESULT OF IUR SEARCH BY MACTING USERNAME WITH OUR SEARCH
    context = {'profiles':profiles,'username':search,"profileimage": profileimage}
    return render(request,'search.html', context)

#VIEW FOR FOLLOWING THE USER
def follow(request,id,username):
    profile = Profile.objects.get(id=id)
    login_profile = Profile.objects.get(user=request.user)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        login_profile.followings.remove(profile.user)
    else:
        profile.followers.add(request.user)
        login_profile.followings.add(profile.user)
    return redirect(f'/search?username={username}')

#FOR UPLOADING THE POST
def upload_post(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url      
    if request.method == 'POST':
        post = request.FILES['post']
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.create(user=request.user,image=post,profile=profile)
        if posts:
            messages.success(request,"POST Uploaded") 
    return render(request,'uploadposts.html',{'profileimage':profileimage })

#FUCTINS FOR LIKING THE POST
def like_post(request,id):
    post = Post.objects.filter(id=id)
    if request.user in post[0].likes.all():
        post[0].likes.remove(request.user)
    else:
        post[0].likes.add(request.user)    
    return redirect("index")

#FOR UPLOADING REEL
def upload_reel(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url      
    if request.method == 'POST':
        reel = request.FILES['reel']
        reels = Reels.objects.create(reel=reel)
        if reels:
            messages.success(request,'REEL UPLOADED')     
    return render(request,'uploadreels.html',{'profileimage':profileimage })

#FOR EXPLORING REELS
def reels(request):    
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url  
    reels = Reels.objects.all()
    return render(request,'reels.html',{'reels':reels,'profileimage':profileimage })

#FOR LIKING THE REEL
def like_reel(request):
    reel = Reels.objects.get(id=id)
    if request.user in reel.likes.all():
        reel.likes.remove(request.user)
    else:
        reel.likes.add(request.user)
    return redirect("reels")    

#FOR UPLOADING STORY
def upload_story(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == 'POST':
        story = request.FILES['story']
        profile = Profile.objects.get(user=request.user)
        story_upload = Story.objects.create(story=story,profile=profile)
        if story_upload:
            messages.success(request,"STORY UPLOADED")
    return render(request,'uploadStory.html',{'profileimage':profileimage})    






