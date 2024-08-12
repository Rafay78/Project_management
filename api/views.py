from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm

@login_required
def project_list(request):
    projects = Project.objects.filter(is_deleted=False, created_by=request.user)
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_deleted=False, created_by=request.user)
    tasks = Task.objects.filter(project=project, is_deleted=False)
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, is_deleted=False, created_by=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, is_deleted=False, created_by=request.user)
    if request.method == 'POST':
        project.is_deleted = True
        project.save()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk, is_deleted=False, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project_pk)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, is_deleted=False, project__created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, is_deleted=False, project__created_by=request.user)
    if request.method == 'POST':
        task.is_deleted = True
        task.save()
        return redirect('project_detail', pk=task.project.pk)
    return render(request, 'task_confirm_delete.html', {'task': task})
