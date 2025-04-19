# Study Tracker

## Introduction
Study Tracker is a simple task management web application built using Flask. It allows users to add, update, and track tasks in a dynamic and user-friendly interface. This project implements key web development concepts, including form handling, user authentication, and database integration.

## Video Demo
[Study Tracker](https://youtu.be/5Lp7fTeKa2g)

## Main Features
- **Task Management:**
  - Add new tasks with details
  - Update task status
  - View tasks in a dynamic table
- **Timer Function:**
   - Study or work on completing tasks with an adjustable pomodoro timer
- **User Authentication:**
  - User authentication for unique usernames and secure passwords
  - Password hashing for secure authentication
- **Session Management:**
  - Persistent or temporary user sessions based on login preferences
- **Database Integration:**
  - Task and user information stored in an SQL database

## Usage
1. Register for a new account
2. Log in with your credentials
3. Add, edit, or update tasks as needed

## Project Structure
```
project_root/
|
├── app.py                    
├── templates/               
│   ├── index.html      
│   ├── login.html          
│   ├── register.html    
│   ├── layout.html            
│   ├── timer.html            
│   └── changePassword.html 
├── static/                
│   └── styles.css            
├── flask_session/         
├── study-tracker-env/        
├── README.md                 
└── requirements.txt          
```

## Implementation
### Purpose and Inspiration
I have previously worked on three projects that were focused on web development. The first was a collaborative project I worked on with a team, and I mainly contributed towards the static performance of the website. The second project was a submission for Week 8 of CS50, in which I gained some basic understanding of dynamic webpages through JavaScript. The third project was another submission for CS50, specifically the Finance project for Week 9. It was the most complex and interesting out of the three. With these experiences, I decided to create a web app from scratch using Flask as my Backend, HTML, CSS, and JavaScript as my Frontend, and phpMyAdmin as my database. 

For the topic, I chose to make a study tracker web app. As a college student majoring in computer science, there are many assignments, meetings, and deadlines that I must keep track of. I also wanted something that will help me study and stay focused. Thus was born the Study Tracker, which features both a task manager and a pomodoro timer for studying.

### study-tracker-env
* To start off, I made a virtual environment called study-tracker-env to install all the necessary dependencies through pip. By the end of the project, I had also exported all the imports into a requirements.txt. 

### app.py
* Main Python file of the application, acting as the backend and controller
* Utilizes Flask to render HTML templates and process user requests
* Handles routing, user authentication, and database interactions
* Implements user login, registration, task tracking, password management, and timer functionality
* Provides JSON responses for frontend interactions via AJAX
* Implements password hashing using bcrypt to securely store and validate user passwords, ensuring that sensitive information is not stored in plain text
* Allows users to remain logged in between sessions if the "Remember Me" button is selected
   * This feature sets session persistence by toggling between permanent (30 days) and temporary (expires on browser close) session lifetimes
* Tracks and identifies logged-in users using session variables (user_id)

### index.html
* Renders the homepage of the web app
* Displays a dynamic table through Jinja with rows of tasks fetched from the database
* Allows users to add and update tasks by marking it as completed
* Includes interactive elements
   * Checkboxes for task completion
   * A pomodoro timer
   * Toggle buttons to show completed and uncompleted tasks with respective columns, such as due date and date completed
* Integrates JavaScript to dynamically handle task updates and display data
   * Event listeners for checkboxes and buttons
   * Using the Fetch API to interact with Flask backend
   * Handling responses, parsing JSON, and Error handling

### login.html
* Renders the login page for users to access their accounts
* Includes a form to collect the username, password, and a "Remember me" checkbox
   * "Remember me" checkbox allows users to remain logged in between session
* Displays flash messages for authentication errors (e.g., invalid username or password)
* Provides a link to the registration page for new users

### register.html
* Renders the registration page for new users to create an account
* Includes a form to input a username, password, and password confirmation
* Ensures validation for unique usernames and matching passwords
* Calls a function in app.py that validates the strength of the password by ensuring the following criteria:
   * At least one letter
   * At least one digit
   * At least one special character
   * Minimum length of 8 characters
* Displays flash messages for errors (e.g., username taken or invalid password confirmation)

### layout.html
* Serves as the base template for the app, using Flask's template inheritance
* Includes common elements like navigation, header, and footer
* Provides placeholders for dynamic content from child templates using HTML and Jinja 
* Links together CSS file and Bootstrap for the templates

### timer.html
* Renders timer page to feature a pomdoro timer for task-focused activities
* Displays timer on the left and tasks table on the right to allow users to dedicate time to specific tasks
* Tasks table can be interacted with to mark tasks as completed
* Allows users to set a timer duration, start, pause, and reset it
* Alert will be sent when timer is up
* Enhances productivity by encouraging focused work sessions
* Uses JavaScript to implement the timer functionality dynamically

### changePassword.html
* Renders the change password page for logged-in users
* Includes a form to collect the username, current password, new password, and password confirmation
* Validates the username
* Validates the current password and ensures the new password meets criteria
* Displays flash messages for errors (e.g., mismatched confirmation)

### styles.css
* Contains the app's styling, ensuring a consistent and visually appealing design
* Defines the layout, colors, typography, and responsive behavior for all HTML templates
* Customizes the appearance of interactive elements like checkboxes, forms, and tables
* Enhances the user experience with hover effects, spacing, and alignment adjustments
* Maintains consistency across app by utilizing CSS  to define a color scheme
* Utilizes Flexbox to create a visually cohesive, organized, and minimalistic design

### helpers.py
* Implements a decorator function used to restrict access to certain routes unless a user is logged in
* Checks if a user_id is stored in the session, and redirects the user to the login page if not stored
* Helps secure routes and ensures that only authenticated users can access specific features
* Inspired by Flask's official documentation for view decorators

## Technologies Used
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python, Flask, Jinja, bcrypt, SQL
- **Database:** MySQL, phpMyAdmin
- **Tools and Utilities:** XAMPP, pip, VSCode, ChatGPT
- **Testing and Debugging:** Microsoft Edge

## Future Enhancements
- Add email verification for account creation
- Implement API endpoints for mobile or third-party integrations
- Add more task management features, such as categories and priorities
- Improve UI design and responsiveness

## Acknowledgments
* **CS50 Team:** For providing the course framework and guidance.
* **Bootstrap Documentation:** For reference and guidance on implementing responsive design and prebuilt components.
* **Flask Documentation:** For understanding Flask's routing, session management, and other features.
* **bcrypt Documentation:** For understanding and implementing secure password hashing.
* **MySQL Documentation:** For learning database operations and queries.
* **W3Schools:** For tutorials and examples on HTML, CSS, JavaScript, and other web development concepts.
* **ChatGPT:** For assistance with debugging, feature implementation, and drafting project documentation.
