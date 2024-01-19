

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course

# def test_example():
#     assert True, "Just test example"

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user('admin')

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


# проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_first_course(client, course_factory):
    # Arrange
    curs = course_factory(_quantity= 10)

    #  Act
    response = client.get('/api/v1/courses/3/')
    
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == curs[2].name

# проверка получения списка курсов (list-логика):
@pytest.mark.django_db
def test_list_course(client, course_factory):
    # Arrange
    curs = course_factory(_quantity= 10)

    #  Act
    response = client.get('/api/v1/courses/')
    
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(curs)
    for ind, one_course in enumerate(data):
        assert one_course['name'] == curs[ind].name

# проверка фильтрации списка курсов по `id`:
@pytest.mark.django_db
def test_list_course_filter_id(client, course_factory):
    # Arrange
    curs = course_factory(_quantity= 10)
    curs_id = curs[2].id
    #  Act
    response = client.get(f'/api/v1/courses/', {'id': curs_id} )
    
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == curs_id

# - проверка фильтрации списка курсов по `name`;
@pytest.mark.django_db
def test_list_course_filter_name(client, course_factory):
    # Arrange
    Course.objects.create(name='match')
    curs = course_factory(_quantity= 10)

    #  Act
    response = client.get('/api/v1/courses/', {'name': 'match'})
    
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == 'match'

# - тест успешного создания курса:
@pytest.mark.django_db
def test_create_course(client):
    # Arrange

    #  Act
    response = client.post('/api/v1/courses/', data= {'name': 'match'})
    
    # Assert
    assert response.status_code == 201


# - тест успешного обновления курса:
@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    curs = course_factory(_quantity= 5)
    cours_id = curs[1].id
    #  Act
    response = client.patch(f'/api/v1/courses/{cours_id}/', data={'name': 'match'})
    
    # Assert
    datas = response.json()
    assert response.status_code == 200
    assert datas['name'] == 'match'


# тест успешного удаления курса.
@pytest.mark.django_db
def test_dalete_course(client, course_factory):
    # Arrange
    curs = course_factory(_quantity= 1)
    cours_id = curs[0].id
    #  Act
    response = client.delete(f'/api/v1/courses/{cours_id}/')
    
    # Assert
    assert response.status_code == 204



