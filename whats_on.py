
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10487697
#    Student name: Lachlan Gilbert
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  What's On?: Online Entertainment Planning Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for planning an entertainment schedule.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.  You may import other widgets
# from the Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed one day).
from sqlite3 import *

#
import webbrowser
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it as a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

#define the website URLs
movies_URL = 'https://www.blueroomcinebar.com/movies/now-showing/'
radio_URL = 'https://www.abc.net.au/radionational/guide/'
gabba_URL = 'https://thegabba.com.au/what-s-on.aspx'

#define variable to be used such as lists of records or global variables
movies_avalable =[]
movie_poster=[]
radio_avalable=[]
radio_time=[]
events_avalable =[]
event_dates =[]
gabba_images=[]
click_count=0
db_click_count = 0
print_code = '''<!doctype html>
<html>
<head>
	<title>Your Selected Entertainment</title>
</head>
<body>
	<h1 style="text-align:center;">Your Entertainment Guide</h1>
	<p style="text-align:center;"><img src="https://lennoxwave.com/wp-content/uploads/2018/02/whats_on_sml.png"></p>'''

#define variables to store results to add to database
events_for_db =[]
times_for_db=[]

#make funtion to detemine to run offline or online
def times_clicked():
    global click_count, movies_avalable, movie_posters,radio_avalable, radio_time, events_avalable, event_dates, gabba_images
    click_count +=1
    movies_avalable =[]
    movie_posters=[]
    radio_avalable=[]
    radio_time=[]
    events_avalable =[]
    event_dates =[]
    gabba_images=[]
    
#make function
def db_save():
    global db_click_count
    db_click_count +=1
    events_for_db=[]
    times_for_db=[]
#-H-O-M-E------P-A-G-E----------------------------------------------------------
# Name of the planner file. To simplify marking, your program should
# generate its entertainment planner using this file name.
planner_file = 'planner.html'

#create home page
home = Tk()
home.title("What's on")
home['bg'] = 'blue'

#add label for Title
title = Label(home, text = "WHAT'S HAPPENING\n AROUND TOWN"
              ,font = ("Arial", 30, "bold"),fg = 'white', bg = 'blue')
title.grid(row =0, column = 0, columnspan = 2, rowspan =2, padx = 20)

#create the offline checkbox
offline = Checkbutton(home, text = 'Offline', state = ACTIVE
                      ,command = times_clicked,fg = 'black', bg = 'white',bd=1)
offline.grid(row=0,column = 2, padx = 10)

#create the db checkbox
add_to_db = Checkbutton(home, text = 'Save Selection to database',state = ACTIVE
                        ,command = db_save, fg='black',bg='white')
add_to_db.grid(row=1,column = 2, padx = 10)

#function to download what movies are playing
def get_movies_online():
    #opens the blue room cinibar website for reading
    movies_page = urlopen(movies_URL)
    #extract the content of the blue room website
    movies_CODE = movies_page.read().decode('UTF-8')
    #close page blue room connection
    movies_page.close()
    #define what the opening tag is for begining of HTML
    movie_title_indicator = '<h4 class="movie-title">'
    #define the closing tag
    end_movie_title_indicator = '</h4>'
    #define the starting position
    movie_start = movies_CODE.find(movie_title_indicator)
    #define the end position
    movie_end = movies_CODE.find(end_movie_title_indicator)
    #find the first 6 movies
    for movies_showing in range(6):
        #detect potional if you can find
        if movie_start == -1 or movie_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add movies to list
            movies_avalable.append(movies_CODE[movie_start + len(movie_title_indicator) : movie_end])
            #define new start position
            movie_start = movies_CODE.find(movie_title_indicator,movie_end)
            #define new end position
            movie_end = movies_CODE.find(end_movie_title_indicator,movie_start)

#define function to get movie poster
def get_poster_online():
    #opens the blue room cinibar website for reading
    movies_page = urlopen(movies_URL)
    #extract the content of the blue room website
    movies_CODE = movies_page.read().decode('UTF-8')
    #close page blue room connection
    movies_page.close()
    #define what the opening tag is for begining of HTML
    movie_title_indicator = '<div class="poster" style="background-image: url('
    #define the closing tag
    end_movie_title_indicator = ')">'
    #define the starting position
    movie_start = movies_CODE.find(movie_title_indicator)
    #define the end position
    movie_end = movies_CODE.find(end_movie_title_indicator)
    #find the first 6 movies
    for movies_showing in range(6):
        #detect potional if you can find
        if movie_start == -1 or movie_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add movies to list
            movie_poster.append(movies_CODE[movie_start + len(movie_title_indicator) : movie_end])
            #define new start position
            movie_start = movies_CODE.find(movie_title_indicator,movie_end)
            #define new end position
            movie_end = movies_CODE.find(end_movie_title_indicator,movie_start)
            
#function for when offline is selected
def get_movies_offline():
    #read text within the document
    movie_file = open('blue_room_cinebar.txt').read()
    #define what the opening tag is for begining of HTML
    movie_title_indicator = '<h4 class="movie-title">'
    #define the closing tag
    end_movie_title_indicator = '</h4>'
    #define the starting position
    movie_start = movie_file.find(movie_title_indicator)
    #define the end position
    movie_end = movie_file.find(end_movie_title_indicator)
    #find the first 6 movies
    for movies_showing in range(6):
        #detect potional if you can find
        if movie_start == -1 or movie_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add movies to list
            movies_avalable.append(movie_file[movie_start + len(movie_title_indicator) : movie_end])
            #define new start position
            movie_start = movie_file.find(movie_title_indicator,movie_end)
            #define new end position
            movie_end = movie_file.find(end_movie_title_indicator,movie_start)

#define a function to retrive the poster file while offline
def get_poster_offline():
    #read text within the document
    movie_file = open('blue_room_cinebar.txt').read()
    #define what the opening tag is for begining of HTML
    movie_title_indicator = '<div class="poster" style="background-image: url('
    #define the closing tag
    end_movie_title_indicator = '")>'
    #define the starting position
    movie_start = movie_file.find(movie_title_indicator)
    #define the end position
    movie_end = movie_file.find(end_movie_title_indicator)
    #find the first 6 movies
    for movies_showing in range(6):
        #detect potional if you can find
        if movie_start == -1 or movie_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add movies to list
            movie_poster.append(movie_file[movie_start + len(movie_title_indicator) : movie_end])
            #define new start position
            movie_start = movie_file.find(movie_title_indicator,movie_end)
            #define new end position
            movie_end = movie_file.find(end_movie_title_indicator,movie_start)

#define fuction which will be used to add to the code when items are selected from the movie page
def add_movies1():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[0]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[0]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[0])
    times_for_db.append("Multiple Screening Times")
def add_movies2():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[1]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[1]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[1])
    times_for_db.append("Multiple Screening Times")
def add_movies3():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[2]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[2]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[2])
    times_for_db.append("Multiple Screening Times")
def add_movies4():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[3]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[3]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[3])
    times_for_db.append("Multiple Screening Times")
def add_movies5():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[4]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[4]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[4])
    times_for_db.append("Multiple Screening Times")
def add_movies6():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+movie_poster[5]+'''"></p>
                                <h2 style="text-align:center;">'''+movies_avalable[5]+'''</h2>
                                <p style="text-align:center;">Check Blue Room website for Screening Times</p>'''
    events_for_db.append(movies_avalable[5])
    times_for_db.append("Multiple Screening Times")
    
#create function to open movies page
def open_movies():
    #if click count is odd then perform offline functions
    if click_count%2 == 1:
        get_movies_offline()
        get_poster_offline()
    #if click count is even then perform online functions
    elif click_count%2 ==0:
        get_movies_online()
        get_poster_online()
    #-M-O-V-I-E-----P-A-G-E--------------------------------------------------------------------
    #add page for movies
    movies = Tk()
    movies.title("What's playing in Cinema's")
    movies['bg'] = 'red'

    #add label to movies page to hold the title
    movies_title = Label(movies, text = 'What is Currently Playing in Cinemas',
                        font = ('Arial', 20, 'bold'), bg = 'red', fg = 'white')
    movies_title.pack()

    #add first checkbutton for movies
    movies_select_one = Checkbutton(movies, text = ('1:',movies_avalable[0],"Multiple Screening Times"),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies1)
    movies_select_one.pack()

    #add second checkbutton for movies
    movies_select_two = Checkbutton(movies, text = ('2:',movies_avalable[1],"Multiple Screening Times"),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies2)
    movies_select_two.pack()

    #add third checkbutto for movies
    movies_select_three = Checkbutton(movies, text = ('3:',movies_avalable[2],"Multiple Screening Times"),font = ('Arial', 15)
                                      ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies3)
    movies_select_three.pack()

    #add fourth checkbutton for movies
    movies_select_four = Checkbutton(movies, text = ('4:',movies_avalable[3],"Multiple Screening Times"),font = ('Arial', 15)
                                     ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies4)
    movies_select_four.pack()

    #add fifth checkbutton for movies
    movies_select_five = Checkbutton(movies, text = ('5:',movies_avalable[4],"Multiple Screening Times"),font = ('Arial', 15)
                                     ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies5)
    movies_select_five.pack()

    #add sixth checkbutton for movies
    movies_select_six = Checkbutton(movies, text = ('6:',movies_avalable[5],"Multiple Screening Times"),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command = add_movies6)
    movies_select_six.pack()

    #show site which information was gathered from
    movies_site = Label(movies,text= movies_URL
                        ,bg = 'red', fg = 'white')
    movies_site.pack()

#add a button for Movies
now_playing = Button(home, text = 'Movies in Cinamas', command=open_movies)
now_playing.grid(row=2,column = 0,padx = 20)

#function to download stations
def get_radio_online():
    #opens the radio realease date website for reading
    radio_page = urlopen(radio_URL)
    #extract the content of the radio realease date website
    radio_CODE = radio_page.read().decode('UTF-8')
    #close radio realease date connection
    radio_page.close()
    #define what the opening tag is for begining of HTML
    radio_title_indicator = 'title=""><strong>'
    #define the closing tag
    end_radio_title_indicator = '</strong>'
    #define the starting position
    radio_start = radio_CODE.find(radio_title_indicator)
    #define the end position
    radio_end = radio_CODE.find(end_radio_title_indicator)
    #find the first 6 radios
    for radio_coming_soon in range(7):
        #detect potional if you can find
        if radio_start == -1 or radio_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add radio to list
            radio_avalable.append(radio_CODE[radio_start + len(radio_title_indicator) : radio_end])
            #define new start position
            radio_start = radio_CODE.find(radio_title_indicator,radio_end)
            #define new end position
            radio_end = radio_CODE.find(end_radio_title_indicator,radio_start)

#define function to find prices of radio
def radio_time_online():
    #opens the radio realease date website for reading
    radio_page = urlopen(radio_URL)
    #extract the content of the radio realease date website
    radio_CODE = radio_page.read().decode('UTF-8')
    #close radio realease date connection
    radio_page.close()
    #define what the opening tag is for begining of HTML
    radio_title_indicator = '</strong>('
    #define the closing tag
    end_radio_title_indicator = ')</p>'
    #define the starting position
    radio_start = radio_CODE.find(radio_title_indicator)
    #define the end position
    radio_end = radio_CODE.find(end_radio_title_indicator)
    #find the first 6 radios
    for radio_coming_soon in range(6):
        #detect potional if you can find
        if radio_start == -1 or radio_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add radio to list
            radio_time.append(radio_CODE[radio_start + len(radio_title_indicator) : radio_end])
            #define new start position
            radio_start = radio_CODE.find(radio_title_indicator,radio_end)
            #define new end position
            radio_end = radio_CODE.find(end_radio_title_indicator,radio_start)


    
#create function for radio realeases when offline
def get_radio_offline():
    #read text within the document
    radio_file = open('radio.txt').read()
    #define what the opening tag is for begining of HTML
    radio_title_indicator = 'title=""><strong>'
    #define the closing tag
    end_radio_title_indicator = '</strong>'
    #define the starting position
    radio_start = radio_file.find(radio_title_indicator)
    #define the end position
    radio_end = radio_file.find(end_radio_title_indicator)
    #find the first 6 radios
    for radio_coming_soon in range(7):
        #detect potional if you can find
        if radio_start == -1 or radio_end == -1:  
            print('Error: Unable to find price')
        else:
            #add radio to list
            radio_avalable.append(radio_file[radio_start + len(radio_title_indicator) : radio_end])
            #define new start position
            radio_start = radio_file.find(radio_title_indicator,radio_end)
            #define new end position
            radio_end = radio_file.find(end_radio_title_indicator,radio_start)

#define function to find price of radio when offline
def radio_time_offline():
    #read text within the document
    radio_file = open('radio.txt').read()
    #define what the opening tag is for begining of HTML
    radio_title_indicator = '</strong>('
    #define the closing tag
    end_radio_title_indicator = ')</p>'
    #define the starting position
    radio_start = radio_file.find(radio_title_indicator)
    #define the end position
    radio_end = radio_file.find(end_radio_title_indicator)
    #find the first 6 radios
    for radio_coming_soon in range(6):
        #detect potional if you can find
        if radio_start == -1 or radio_end == -1:  
            print('Error: Unable to find price')
        else:
            #add radio to list
            radio_time.append(radio_file[radio_start + len(radio_title_indicator) : radio_end])
            #define new start position
            radio_start = radio_file.find(radio_title_indicator,radio_end)
            #define new end position
            radio_end = radio_file.find(end_radio_title_indicator,radio_start)



#create functions to add radio to code
def add_radio1():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[1]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[0]+'''</p>'''
    events_for_db.append(radio_avalable[1])
    times_for_db.append(radio_time[0])
def add_radio2():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[2]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[1]+'''</p>'''
    events_for_db.append(radio_avalable[2])
    times_for_db.append(radio_time[1])
def add_radio3():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[3]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[2]+'''</p>'''
    events_for_db.append(radio_avalable[3])
    times_for_db.append(radio_time[2])
def add_radio4():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[4]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[3]+'''</p>'''
    events_for_db.append(radio_avalable[4])
    times_for_db.append(radio_time[3])
def add_radio5():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[5]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[4]+'''</p>'''
    events_for_db.append(radio_avalable[5])
    times_for_db.append(radio_time[4])
def add_radio6():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="https://png.pngtree.com/png_detail/18/09/10/pngtree-cartoon-radio-png-clipart_1294953.jpg"></p>
                                <h2 style="text-align:center;">'''+radio_avalable[6]+'''</h2>
                                <p style="text-align:center;">'''+radio_time[5]+'''</p>'''
    events_for_db.append(radio_avalable[6])
    times_for_db.append(radio_time[5])



#create function to radios games page
def open_radio():
    #if click count is odd then perform offline functions
    if click_count%2 == 1:
        get_radio_offline()
        radio_time_offline()
    #if click count is even then perform online functions
    elif click_count%2 ==0:
        get_radio_online()
        radio_time_online()
    #-D-V-D------P-A-G-E-------------------------------------------------------------------
    #add page for game releases
    radio = Tk()
    radio.title("Radio Stations")
    radio['bg'] = 'orange'

    #add label to game page to hold the title
    radio_title = Label(radio, text = 'Upcoming radio Releases',
                        font = ('Arial', 20, 'bold'), bg = 'orange', fg = 'white')
    radio_title.pack()

    #add first checkbutton for games
    radio_select_one = Checkbutton(radio, text = ('1:',radio_avalable[1], '$' +' '+radio_time[0]),font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio1)
    radio_select_one.pack()

    #add second checkbutton for games
    radio_select_two = Checkbutton(radio, text = ('2:',radio_avalable[2], '$' +' '+radio_time[1]),font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio2)
    radio_select_two.pack()

    #add third checkbutto for games
    radio_select_three = Checkbutton(radio, text = ('3:',radio_avalable[3], '$' +' '+radio_time[2]),font = ('Arial', 15)
                                     ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio3)
    radio_select_three.pack()

    #add fourth checkbutton for games
    radio_select_four = Checkbutton(radio, text = ('4:',radio_avalable[4], '$' +' '+radio_time[3]),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio4)
    radio_select_four.pack()

    #add fifth checkbutton for games
    radio_select_five = Checkbutton(radio, text = ('5:',radio_avalable[5], '$' +' '+radio_time[4]),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio5)
    radio_select_five.pack()

    #add sixth checkbutton for games
    radio_select_six = Checkbutton(radio, text = ('6:',radio_avalable[6], '$' +' '+radio_time[5]),font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command = add_radio6)
    radio_select_six.pack()

    #show site which information was gathered from
    radio_site = Label(radio, text = 'https://www.abc.net.au/radionational/guide/'
                       ,bg='orange',fg='white')
    radio_site.pack()


#add a button for game releases
radio_releases = Button(home, text = 'Radio stations',command=open_radio)
radio_releases.grid(row=2,column = 1,padx = 20)

#function to download upcoming events at the gabba release
def get_gabba_online():
    #opens the gabba website for reading
    gabba_page = urlopen(gabba_URL)
    #extract the content of the gabba website
    gabba_CODE = gabba_page.read().decode('UTF-8')
    #close gabba connection
    gabba_page.close()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<h6 class="event-title">'
    #define the closing tag
    end_gabba_title_indicator = '</h6>'
    #define the starting position
    gabba_start = gabba_CODE.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_CODE.find(end_gabba_title_indicator)
    #find the first 6 events
    for gabba_coming_soon in range(6):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add event to list
            events_avalable.append(gabba_CODE[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_CODE.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_CODE.find(end_gabba_title_indicator,gabba_start)

#define funchtion to get the date of event
def gabba_dates_online():
    #opens the gabba website for reading
    gabba_page = urlopen(gabba_URL)
    #extract the content of the gabba website
    gabba_CODE = gabba_page.read().decode('UTF-8')
    #close gabba connection
    gabba_page.close()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<h7 class="event-date text-uppercase">'
    #define the closing tag
    end_gabba_title_indicator = '</h7>'
    #define the starting position
    gabba_start = gabba_CODE.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_CODE.find(end_gabba_title_indicator)
    #find the first 6 events
    for dates in range(7):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add date to list
            event_dates.append(gabba_CODE[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_CODE.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_CODE.find(end_gabba_title_indicator,gabba_start)    

#define function to retrieve image
def gabba_images_online():
    #opens the gabba website for reading
    gabba_page = urlopen(gabba_URL)
    #extract the content of the gabba website
    gabba_CODE = gabba_page.read().decode('UTF-8')
    #close gabba connection
    gabba_page.close()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<img src="'
    #define the closing tag
    end_gabba_title_indicator = '"'
    #define the starting position
    gabba_start = gabba_CODE.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_CODE.find(end_gabba_title_indicator)
    #find the first 6 events
    for dates in range(7):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add date to list
            gabba_images.append(gabba_CODE[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_CODE.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_CODE.find(end_gabba_title_indicator,gabba_start)

#define function to get the events when offline
def get_gabba_offline():
    #read text within the document
    gabba_file = open('gabba.txt').read()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<h6 class="event-title">'
    #define the closing tag
    end_gabba_title_indicator = '</h6>'
    #define the starting position
    gabba_start = gabba_file.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_file.find(end_gabba_title_indicator)
    #find the first 6 events
    for gabba_coming_soon in range(6):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add event to list
            events_avalable.append(gabba_file[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_file.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_file.find(end_gabba_title_indicator,gabba_start)
            
#define function to get the dates of events when offline
def gabba_dates_offline():
    #read text within the document
    gabba_file = open('gabba.txt').read()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<h7 class="event-date text-uppercase">'
    #define the closing tag
    end_gabba_title_indicator = '</h7>'
    #define the starting position
    gabba_start = gabba_file.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_file.find(end_gabba_title_indicator)
    #find the first 6 events
    for dates in range(7):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add date to list
            event_dates.append(gabba_file[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_file.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_file.find(end_gabba_title_indicator,gabba_start)

#define function to find image when offline
def gabba_images_offline():
    #read text within the document
    gabba_file = open('gabba.txt').read()
    #define what the opening tag is for begining of HTML
    gabba_title_indicator = '<img src="'
    #define the closing tag
    end_gabba_title_indicator = '"'
    #define the starting position
    gabba_start = gabba_file.find(gabba_title_indicator)
    #define the end position
    gabba_end = gabba_file.find(end_gabba_title_indicator)
    #find the first 6 events
    for dates in range(7):
        #detect potional if you can find
        if gabba_start == -1 or gabba_end == -1:  
            print('Error: Unable to find page title')
        else:
            #add date to list
            gabba_images.append(gabba_file[gabba_start + len(gabba_title_indicator) : gabba_end])
            #define new start position
            gabba_start = gabba_file.find(gabba_title_indicator,gabba_end)
            #define new end position
            gabba_end = gabba_file.find(end_gabba_title_indicator,gabba_start)

#events_avalable =[]
#event_dates =[]
#gabba_images=[]
#define functions to add events to code
def add_gabba1():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[0]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[0]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[1]+'''</p>'''
    events_for_db.append(events_avalable[0])
    times_for_db.append(event_dates[1])
def add_gabba2():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[1]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[1]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[2]+'''</p>'''
    events_for_db.append(events_avalable[1])
    times_for_db.append(event_dates[2])
def add_gabba3():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[2]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[2]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[3]+'''</p>'''
    events_for_db.append(events_avalable[2])
    times_for_db.append(event_dates[3])
def add_gabba4():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[3]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[3]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[4]+'''</p>'''
    events_for_db.append(events_avalable[3])
    times_for_db.append(event_dates[4])
def add_gabba5():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[4]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[4]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[5]+'''</p>'''
    events_for_db.append(events_avalable[4])
    times_for_db.append(event_dates[5])
def add_gabba6():
    global print_code
    print_code =  print_code + '''<p style="text-align:center;"><img src="'''+gabba_images[5]+'''"></p>
                                <h2 style="text-align:center;">'''+events_avalable[5]+'''</h2>
                                <p style="text-align:center;">Event is on the '''+event_dates[6]+'''</p>'''
    events_for_db.append(events_avalable[5])
    times_for_db.append(event_dates[6])
            
#create function to open movies page
def open_gabba():
    #if click count is odd then perform offline functions
    if click_count%2 == 1:
        get_gabba_offline()
        gabba_dates_offline()
        gabba_images_offline()
    #if click count is even then perform online functions
    elif click_count%2==0:
        get_gabba_online()
        gabba_dates_online()
        gabba_images_online()
    #-G-A-B-B-A-----P-A-G-E-------------------------------------------------------------------
    #add page for events on at the gabba
    gabba = Tk()
    gabba.title("Upcoming events at the Gabba")
    gabba['bg'] = 'green'

    #add label to gabba page to hold the title
    gabba_title = Label(gabba, text = 'Upcoming Events at the Gabba',
                        font = ('Arial', 20, 'bold'), bg = 'green', fg = 'white'
                        )
    gabba_title.pack()

    #add first checkbutton for gabba
    gabba_select_one = Checkbutton(gabba, text = ('1:',events_avalable[0],event_dates[1]),font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba1)
    gabba_select_one.pack()

    #add second checkbutton for gabba
    gabba_select_two = Checkbutton(gabba, text = ('2:',events_avalable[1],event_dates[2]), font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba2)
    gabba_select_two.pack()

    #add third checkbutto for gabba
    gabba_select_three = Checkbutton(gabba, text = ('3:',events_avalable[2],event_dates[3]), font = ('Arial', 15)
                                     ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba3)
    gabba_select_three.pack()

    #add fourth checkbutton for gabba
    gabba_select_four = Checkbutton(gabba, text = ('4:',events_avalable[3],event_dates[4]),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba4)
    gabba_select_four.pack()

    #add fifth checkbutton for gabba
    gabba_select_five = Checkbutton(gabba, text = ('5:',events_avalable[4],event_dates[5]),font = ('Arial', 15)
                                    ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba5)
    gabba_select_five.pack()

    #add sixth checkbutton for gabba
    gabba_select_six = Checkbutton(gabba, text = ('6:',events_avalable[5],event_dates[6]),font = ('Arial', 15)
                                   ,fg = 'black', bg = 'white',state = ACTIVE, command=add_gabba6)
    gabba_select_six.pack()

    #show site which information was gathered from
    gabba_site = Label(gabba, text = 'https://thegabba.com.au/what-s-on.aspx',
                       bg = 'green', fg = 'white')
    gabba_site.pack()

#add a button for upcoming events at the gabba
at_gabba = Button(home, text = "What's on at the Gabba", command=open_gabba)
at_gabba.grid(row=2,column =2,padx = 20)
#https://thegabba.com.au/what-s-on.aspx


print_code = print_code+'''<p>Sourced from:</p>
                <p><a href="https://www.blueroomcinebar.com/movies/now-showing/">Blue Room Cinebar</a></p>
                <p><a href="https://www.abc.net.au/radionational/guide/">Radio Stations</a></p>
                <p><a href="https://thegabba.com.au/what-s-on.aspx">Events at the Gabba</a></p>
                </body>
                </html>'''

#define print function
def print_items_selected():
    global print_code
    #create html file
    guide_file = open('guide.html','w', encoding = 'UTF-8')
    #print selected events into file
    guide_file.write(str(print_code))
    #close file
    guide_file.close()
    url = 'file:///C:/Users/lachl/OneDrive/Documents/University/First%20Year/Semester%20One/IFB104/Assignment%202/guide.html'
    webbrowser.open(url, new=2)  
    print_code ='''<!doctype html>
                <html>
                <head>
                <title>Your Selected Entertainment</title>
                </head>
                <body>
                <h1 style="text-align:center;">Your Entertainment Guide</h1>
                <p style="text-align:center;"><img src="https://lennoxwave.com/wp-content/uploads/2018/02/whats_on_sml.png"></p>
                '''
    #if the commit to DB click number is odd then add the sources selected to the DB
    if db_click_count%2 == 1:
        #connect to db
        #establish connection to the database
        connection = connect(database= 'entertainment_planner.db')
        #enter the database
        entertainment_db=connection.cursor()
        #use delete query  to  clear all pre existing data from the database
        entertainment_db.execute('''DELETE FROM events''')
        #create a list to add combined values into
        full_details=[]
        #create for loop to append all details into the DB
        for entry_num in range(len(events_for_db)):       
            details=events_for_db[entry_num],times_for_db[entry_num]
            full_details.append(details)
        #create start of SQL insert query
        query = 'INSERT INTO events VALUES '
        #create for loop to add contents of full_details into the query
        for values in range(len(full_details)):
            #if it is the first value don't but a comma infront
            if values == 0:
                query = query + str(full_details[0])
            #for the rest add a comma infront
            else: query = query + ","+str(full_details[values])
        #run Query
        entertainment_db.execute(query)
        #save query outcome to the DB
        connection.commit()
        #close link
        entertainment_db.close()
        #close connection to DB
        connection.close()

#print
print_selected = Button(home, text = 'Print Planner', command = print_items_selected)
print_selected.grid(row =3, column =1, pady =5)

mainloop()
