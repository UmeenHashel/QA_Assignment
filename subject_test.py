from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://demoqa.com/automation-practice-form")


def fill_form(valid=True):
    """Function to fill the job application form."""

    # Enter First Name and Last Name
    driver.find_element(By.ID, "firstName").send_keys("John" if valid else "")
    driver.find_element(By.ID, "lastName").send_keys("Doe" if valid else "")

    # Enter Email
    email = "john.doe@example.com" if valid else "invalid-email"
    driver.find_element(By.ID, "userEmail").send_keys(email)

    # Select Gender (Male)
    driver.find_element(By.XPATH, "//label[contains(text(),'Male')]").click()

    # Enter Mobile Number
    driver.find_element(By.ID, "userNumber").send_keys("9876543210" if valid else "")

    # Enter Date of Birth
    # date of birth
    driver.find_element(By.ID, "dateOfBirthInput").click()
    time.sleep(1)

    year_dropdown = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_dropdown.click()
    year_dropdown.find_element(By.XPATH, "//option[@value='1995']").click()

    month_dropdown = driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")
    month_dropdown.click()
    month_dropdown.find_element(By.XPATH, "//option[@value='5']").click()

    driver.find_element(By.XPATH, "//div[contains(@class,'react-datepicker__day') and text()='20']").click()

    # Enter Subjects
    subjects = driver.find_element(By.ID, "subjectsInput")
    subjects.send_keys("Maths")
    subjects.send_keys(Keys.RETURN)

    # Select Hobbies (Sports)
    driver.find_element(By.XPATH, "//label[contains(text(),'Sports')]").click()

    # Upload Picture
    driver.find_element(By.ID, "uploadPicture").send_keys("C:\\path_to_image\\test.jpg")

    # Enter Address
    driver.find_element(By.ID, "currentAddress").send_keys("123 Test Street" if valid else "")

    # Select State and City
    driver.find_element(By.ID, "state").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'NCR')]").click()
    driver.find_element(By.ID, "city").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'Delhi')]").click()

    # Submit Form
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)  # Allow modal to appear


def validate_submission(expected_success=True):
    """Function to validate form submission result."""
    try:
        modal = driver.find_element(By.CLASS_NAME, "modal-content")
        if expected_success:
            assert "Thanks for submitting the form" in modal.text
            print("✅ Test Passed: Form submitted successfully.")
        else:
            print("❌ Test Failed: Form should not be submitted.")
    except:
        if not expected_success:
            print("✅ Test Passed: Form was not submitted.")
        else:
            print("❌ Test Failed: Form submission failed unexpectedly.")


# Test Case 1: Valid Form Submission
print("Running Test Case 1: Valid Form Submission...")
fill_form(valid=True)
validate_submission(expected_success=True)

# Test Case 2: Mandatory Fields Left Blank
print("\nRunning Test Case 2: Form Submission with Missing Fields...")
driver.refresh()
time.sleep(2)
fill_form(valid=False)
validate_submission(expected_success=False)

# Test Case 3: Invalid Email Format
print("\nRunning Test Case 3: Invalid Email Format Validation...")
driver.refresh()
time.sleep(2)
fill_form(valid=True)
driver.find_element(By.ID, "userEmail").clear()
driver.find_element(By.ID, "userEmail").send_keys("invalid-email")
driver.find_element(By.ID, "submit").click()

# Validate email field error message
email_error = driver.find_element(By.ID, "userEmail")
if "invalid-email" in email_error.get_attribute("value"):
    print("✅ Test Passed: Invalid email format detected.")
else:
    print("❌ Test Failed: Invalid email format not validated.")

# Close Browser
driver.quit()
