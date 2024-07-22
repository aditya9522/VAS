import base64
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from . models import Employee
import requests

def home(request):
    return render(request, "home.html")

def authenticate(sample, stored):
    api_url = 'https://speaker-verification1.p.rapidapi.com/Verification'
    api_key = 'd0ffc4913emsh8b30c0fbf3e55dap1963dbjsn6902e82e8dc3'

    voice_path = os.path.join(settings.MEDIA_ROOT, 'voice_samples')

    sound1_name = os.path.basename(sample)
    sound2_name = os.path.basename(stored)

    sound1_path = os.path.join(voice_path, sound1_name)
    sound2_path = os.path.join(voice_path, sound2_name)

    try:
        with open(sound1_path, 'rb') as sound1_file, open(sound2_path, 'rb') as sound2_file:
            files = {
                'sound1': (sound1_name, sound1_file, 'multipart/form-data'),
                'sound2': (sound2_name, sound2_file, 'multipart/form-data')
            }

            headers = {
                "x-rapidapi-host": "speaker-verification1.p.rapidapi.com",
                "x-rapidapi-key": api_key
            }

            response = requests.post(api_url, files=files, headers=headers)

            print(response.text)

            if response.status_code == 200:
                result = response.json()
                print(result)

                result = result['data']['resultMessage']
                status = True if result == "The two voices belong to the same person." else False
                return status
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return False

    except FileNotFoundError as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def login(request):
    if request.method == 'POST':
        employeeid = request.POST.get('employeeid')
        voice_sample_data = request.FILES.get('voice-sample')

        if not voice_sample_data:
            messages.error(request, 'Please provide a voice sample for authentication')
            return redirect('login')

        if not Employee.objects.filter(employeeid=employeeid).exists():
            messages.error(request, 'Employee ID does not exist')
            return redirect('login')

        try:
            file_name = f"{employeeid}.webm"
            file_path = os.path.join(settings.MEDIA_ROOT, 'voice_samples', file_name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as f:
                for chunk in voice_sample_data.chunks():
                    f.write(chunk)

            employee_data = Employee.objects.get(employeeid=employeeid)

            sample = file_path
            stored = employee_data.voice_sample

            res = authenticate(sample, stored)

            os.remove(file_path)

            print(res)

            if res:
                request.session['employee_data'] = {
                    'employeeid': employee_data.employeeid,
                    'name': employee_data.name,
                    'email': employee_data.email,
                }
                
                return redirect('dashboard')
            else:
                messages.error(request, 'Voice did not match, please try again.')
                return redirect('login')

        except Exception as e:
            messages.error(request, f'Something went wrong: {e}')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    messages.info(request, 'You have been successfully logged out.')
    return redirect('login')

def registerUser(request):
    if request.method == 'POST':
        employeeid = request.POST.get('employeeid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        voice_sample_data = request.FILES.get('voice-sample')

        if not voice_sample_data:
            messages.error(request, 'Please provide a voice sample for registration')
            return redirect('register') 

        if Employee.objects.filter(employeeid=employeeid).exists():
            messages.error(request, 'Employee ID already exists')
            return redirect('register')

        try:
            file_name = f"{employeeid}_{name}.webm"
            file_path = os.path.join(settings.MEDIA_ROOT, 'voice_samples', file_name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as f:
                for chunk in voice_sample_data.chunks():
                    f.write(chunk)

            employee = Employee(
                employeeid=employeeid,
                name=name,
                email=email,
                voice_sample=file_path,
            )
            employee.save()

            messages.success(request, 'Registration successful.')
            return redirect('register') 

        except Exception as e:
            messages.error(request, 'Please try again')
            return redirect('register')

    return render(request, 'register.html')

def dashboard(request):
    employee_data = request.session.get('employee_data', None)
    context = {
        'employee_data': employee_data
    }
    return render(request, 'dashboard.html', context)


