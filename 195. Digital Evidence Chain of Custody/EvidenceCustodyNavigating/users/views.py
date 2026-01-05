# Create your views here.
from datetime import datetime, timedelta

from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from jose import JWTError, jwt
import csv
from .forms import UserRegistrationForm, OrgInputForm
from .models import UserRegistrationModel, TokenCountModel
from django.conf import settings
import pandas as pd
import random
import os

SECRET_KEY = "ce9941882f6e044f9809bcee90a2992b4d9d9c21235ab7c537ad56517050f26b"
ALGORITHM = "HS256"

import socket


def get_ipv4_address():
    try:
        # connect to an external host, doesn't send data
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error: {e}"


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return the generated token
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HttpResponse(
            status_code=HttpResponse(status=204),
            detail="Could not validate credentials",
        )


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            loginId = form.cleaned_data['loginid']
            TokenCountModel.objects.create(loginid=loginId, count=0)
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                data = {'loginid': loginid}
                token_jwt = create_access_token(data)
                request.session['token'] = token_jwt
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {'ip': get_ipv4_address()})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {'ip': get_ipv4_address()})


def viewDataset(request):
    folder_path = os.path.join(settings.MEDIA_ROOT)  # Put your folder inside the project root
    # Read all CSV files and collect their DataFrames
    dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(folder_path, file))
            # df['source_file'] = file  # Optional: track source
            dataframes.append(df)

    # Combine all dataframes (outer join to handle different columns)
    if dataframes:
        combined_df = pd.concat(dataframes, axis=0, ignore_index=True, sort=False)
    else:
        combined_df = pd.DataFrame()  # Empty

    # Convert to HTML for template
    html_table = combined_df.to_html(classes='table table-bordered table-striped', index=False, na_rep='-')

    return render(request, 'users/viewdataset.html', {'data': html_table})


def simulate_evidence_view(request):
    from .utility.DigitalEvidenceProcessImpl import DigitalEvidenceProcess
    csv_path = os.path.join(settings.MEDIA_ROOT, 'synthetic_evidence.csv')

    evidence_list = []
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            evidence_list.append({
                'id': row['id'],
                'type': row['type'],
                'description': row['description'],
                'source': row['source']
            })

    process = DigitalEvidenceProcess(tamper_chance=0.15, fail_chance=0.1)
    process.simulate_with_details(evidence_list)

    # Output directory
    output_dir = os.path.join(settings.MEDIA_ROOT, 'graphs')
    os.makedirs(output_dir, exist_ok=True)

    # Save graph images
    phase_path = os.path.join(output_dir, 'phase_counts.png')
    flow_path = os.path.join(output_dir, 'process_flow.png')
    types_path = os.path.join(output_dir, 'evidence_types.png')

    process.plot_phase_counts(phase_path)
    process.plot_process_flow(flow_path)
    process.plot_evidence_types(types_path)

    completed = len(
        set(eid for eid, phase, status in process.evidence_log if status == 'ok' and phase == process.PHASES[-1]))

    context = {
        'total': len(set(eid for eid, _, _ in process.evidence_log)),
        'tampered': len(process.tampered),
        'failed': len(process.failed),
        'completed': completed,
        'tampered_list': process.tampered,
        'failed_list': process.failed,
        'graphs': {
            'phase_counts': 'graphs/phase_counts.png',
            'process_flow': 'graphs/process_flow.png',
            'evidence_types': 'graphs/evidence_types.png',
        }
    }

    return render(request, 'users/simulate_results.html', context)


from .utility.DigitalEvidenceProcessImpl import DigitalEvidenceProcess  # Use your class here


def dynamic_input_form(request):
    return render(request, 'users/dynamic_input_form.html')


def dynamic_input_results(request):
    import matplotlib.pyplot as plt
    import uuid
    if request.method == 'POST':
        evidence_list = []
        total = int(request.POST.get('total', 1))
        for i in range(1, total + 1):
            evidence_id = request.POST.get(f'id_{i}')
            evidence_type = request.POST.get(f'type_{i}')
            description = request.POST.get(f'description_{i}')
            source = request.POST.get(f'source_{i}')
            evidence_list.append({
                'id': evidence_id,
                'type': evidence_type,
                'description': description,
                'source': source
            })

        # Run simulation
        process = DigitalEvidenceProcess()
        process.simulate_with_details(evidence_list)

        # Generate and save graphs to media
        graph_paths = {}
        graph_dir = os.path.join(settings.MEDIA_ROOT, 'usrgraphs')
        os.makedirs(graph_dir, exist_ok=True)

        def save_plot(plot_func, filename):
            path = os.path.join(graph_dir, filename)
            plt.clf()
            plot_func(path)
            plt.savefig(path)
            return f'graphs/{filename}'

        graph_paths['phase_counts'] = save_plot(process.plot_phase_counts, "phase_counts.png")
        graph_paths['process_flow'] = save_plot(process.plot_process_flow, "process_flow.png")
        graph_paths['evidence_types'] = save_plot(process.plot_evidence_types, "evidence_types.png")

        return render(request, 'users/dynamic_input_results.html', {
            'evidence_list': evidence_list,
            'results': {
                'tampered': process.tampered,
                'failed': process.failed,
                'completed': len(set(eid for eid, phase, status in process.evidence_log if
                                     status == 'ok' and phase == process.PHASES[-1]))
            },
            'graphs': graph_paths
        })

    return redirect('dynamic_input_form')
