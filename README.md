# Django-Crowdfunding
##1. Overview
This is a web app that simulates the functionality of a Crowdfunding platform made using Django, where users can launch projects and donate to other users' projects, as well as rate and comment on their projects. The app makes use of a MySQL Database to store information about users, projects and donations. The projects consists of two main apps, one for users and another for projects. The users app contains all the functionality of user accounts, and handles account management and registration, while the projects app does the same for projects, as well as deletion.

##2. Users
Users can register their accounts in the database using email addresses that they have to confirm using an activation link that a mailserver sends automatically to their email inbox upon registration. After registration, the user can login, edit their profile, create projects, and donate to other projects created by other users, as well as rate, report, and comment on projects.

##3. Projects
Once registered and logged in, users can create projects for campaigns they wish to start. In addition to a project name and description, users can set the fundraising targets for their projects, and provide additional details like campaign start and end dates, as well as upload images to their profile page. Once a project has been launched, other users can donate to it, comment on it or report inappropriate content, be it the project itself or comments. The app also keeps track of individual rating for projects made by different users. Finally, users can view the donation progress for thier projects, and cancel projects that are below 25% of their target, which deletes them from the database entirely.

