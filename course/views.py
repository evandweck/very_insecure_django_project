from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import connection
from course.forms import AddCourseReviewForm
from course.models import CourseReview, Course, Instructor
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#django.core.exceptions

def homepage(request):
    cursor = connection.cursor()
    #query = 'SELECT Course.courseNumber, Course.courseName, Instructor.firstName, Instructor.lastName, CourseReview.review FROM Course, Instructor, CourseReview WHERE Course.courseId = CourseReview.courseId AND Instructor.professorID = CourseReview.professorId'
    query = ''
    cursor.execute(query)
    reviews = cursor.fetchall()
    return render(request, 'homepage.html', {'reviews': reviews})

def about(request):
    return render(request, 'about.html')

def courses(request):
    cursor = connection.cursor()
    query = 'SELECT * FROM Course_Course'
    cursor.execute(query)
    courses = cursor.fetchall()
    return render(request, 'courses.html', {'courses':courses})

def course_reviews(request):
    cursor = connection.cursor()
    query = 'SELECT * FROM course_coursereview, course_instructor WHERE course_coursereview.instructorId = course_instructor.instructorId'
    #coursereviews = CourseReview.objects.filter(instructorId=1)
    #print(coursereviews.instructorFirstName)
    cursor.execute(query)
    course_reviews = cursor.fetchall()
    return render(request, 'course_reviews.html', {'course_reviews': course_reviews})

def add_course_review(request):
    if request.method == 'GET':
        form = AddCourseReviewForm()
    else:
        form = AddCourseReviewForm(request.POST)
        if form.is_valid():
            courseDept = form.cleaned_data['courseDepartment']
            courseNum = form.cleaned_data['courseNumber']
            instructorFirstName = form.cleaned_data['instructorFirstName']
            instructorLastName = form.cleaned_data['instructorLastName']
            avgRating = 0.0
            numRatings = 0

            # check if course already exists in database by querying
            course = Course.objects.filter(courseDepartment=courseDept,courseNumber=courseNum)

            # if the course doesn't exist...
            if not course.count():
                # create course
                new_course = Course.objects.create(courseDepartment=courseDept,courseNumber=courseNum,courseName='',averageRating=avgRating,numberOfRatings=numRatings)

                # create Instructor tuple if new instructor
                new_instructor = Instructor.objects.filter(firstName=instructorFirstName)

                # get the userId for the user leaving the review
                currentUser = request.user
                currentUserId = currentUser.id

                # find out the info needed to see if we need to create a new instructor
                instructorFirstName = form.cleaned_data['instructorFirstName']
                instructorLastName = form.cleaned_data['instructorLastName']

                try:
                    instructor = Instructor.objects.get(firstName=instructorFirstName,lastName=instructorLastName)
                    instructorId = instructor.instructorId
                except ObjectDoesNotExist:
                    # add new instructor 
                    newInstructor = Instructor.objects.create(
                        firstName=instructorFirstName,
                        lastName=instructorLastName
                        )
                    instructorId = newInstructor.instructorId

                # add the course review
                courseReview = CourseReview.objects.create(
                    courseDepartment = form.cleaned_data['courseDepartment'],
                    courseNumber = form.cleaned_data['courseNumber'],
                    instructorId = instructorId,
                    reviewerId = currentUserId,
                    review = form.cleaned_data['review'],
                    rating = form.cleaned_data['rating'],
                    reviewDate = form.cleaned_data['reviewDate']
                )
            else:
                # get the userId for the user leaving the review
                currentUser = request.user
                currentUserId = currentUser.id

                 # find out the info needed to see if we need to create a new instructor
                instructorFirstName = form.cleaned_data['instructorFirstName']
                instructorLastName = form.cleaned_data['instructorLastName']

                try:
                    instructor = Instructor.objects.get(firstName=instructorFirstName,lastName=instructorLastName)
                    instructorId = instructor.instructorId
                except ObjectDoesNotExist:
                    # add new instructor 
                    newInstructor = Instructor.objects.create(
                        firstName=instructorFirstName,
                        lastName=instructorLastName
                        )
                    instructorId = newInstructor.instructorId

                # if course exists, just add course on the id of the instructor from instructor table
                courseReview = CourseReview.objects.create(
                    courseDepartment = form.cleaned_data['courseDepartment'],
                    courseNumber = form.cleaned_data['courseNumber'],
                    instructorId = instructorId,
                    reviewerId=currentUserId,
                    review = form.cleaned_data['review'],
                    rating = form.cleaned_data['rating'],
                    reviewDate = form.cleaned_data['reviewDate']
                )

            #return redirect('thanks')
            return render(request, "submission.html")
    return render(request, "add_course_review.html", {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
