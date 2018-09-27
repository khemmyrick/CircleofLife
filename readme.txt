# Steps completed:

1. Basic webapp runs with no errors.
2. Validators check for bio length and password complexity.
3. Custom CSS implemented.

# Next:
1. Upload to github for feedback and advice.
2. Create edit profile and change password routes.
2. pload to github after forms module is working.

User Profile with Django\
1. Use the supplied HTML/CSS to build and style the profile page and bio page.

2. Create a Django model for the user profile.[X]

3. Add routes to display a profile, edit a profile, and change the password.[X]

4. Create a “profile” view to display a user profile with the following fields: First Name, Last Name, Email, Date of Birth, Bio and Avatar. Include a link to edit the profile.[X?]

5. Create an “edit” view with the route “/profile/edit” that allows the user to edit the user profile with the following fields: First Name, Last Name, Email, Date of Birth, Confirm Email, Bio and Avatar.[]

6. Validate user input "Date of Birth" field: check for a proper date format (YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY)[]

7. Validate user input "Email" field: check that the email addresses match and are in a valid format.[]

8. Validate user input "Bio" field: check that the bio is 10 characters or longer and properly escapes HTML formatting.[]
- (am I using a filter to force it to display properly in html,
- or am I adding a validator to stop the field from accepting incorrectly formatted strings?)

9. Add the ability to upload and save a user’s avatar image.[]

10. Create “change-password” view with the route “/profile/change_password” that allows the user to update their password using User.set_password() and then User.save(). Form fields will be: current password, new password, confirm password[]

11. Validate user input "Password" fields: check that the old password is correct using User.check_password() and the new password matches the confirm password field and follows the following password policy.
must not be the same as the current password minimum password length of 14 characters. must use of both uppercase and lowercase letters must include one or more numerical digits must include one or more of special characters, such as @, #, $ cannot contain the user name or parts of the user’s full name, such as their first name[]

12. Use CSS to style headings, font, and form.[]


EC:
1. Add additional form fields to build a more complex form with additional options, such as city/state/country of residence, favorite animal or hobby,[]

2. JavaScript is utilized for a date dropdown for the Date of Birth validation feature.[]

3. JavaScript is utilized for text formatting for the Bio validation feature.[]

4. Add an online image editor to the avatar. Include the basic functionality: rotate, crop and flip. PNG mockup supplied.[]

5. A password strength “meter” is displayed when validating passwords.[]